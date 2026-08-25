"""Minimal loader for the original word2vec binary format.

Replaces `gensim.downloader`, which has no wheels for Python 3.14.
Only NumPy is required.

The file GoogleNews-vectors-negative300.bin contains 3,000,000 words
(3.6 GB) sorted by frequency. Because of that ordering we can fetch just
the first megabytes via an HTTP range request and still get all common
words.

File format:
    header:  b"3000000 300\n"
    record:  word bytes, then b" ", then 300 little-endian float32
"""

import struct  # Package for reading binary data
import urllib.request  # Package for the HTTP range request
from pathlib import Path  # Package for handling file paths

import numpy as np  # Package for numerical operations

URL = (
    "https://huggingface.co/NathaNn1111/word2vec-google-news-negative-300-bin"
    "/resolve/main/GoogleNews-vectors-negative300.bin"
)
CACHE_DIR = Path.home() / ".cache" / "word2vec"
BYTES_PER_WORD = 1215  # 300 floats * 4 bytes + ~15 bytes for the word itself


class WordVectors:
    """Word vectors with the subset of the gensim KeyedVectors API we need."""

    def __init__(self, words: list[str], vectors: np.ndarray):
        self.index_to_key = words
        self.key_to_index = {word: i for i, word in enumerate(words)}
        self.vectors = vectors
        # unit-length copies, so cosine similarity is a simple dot product
        self._unit = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    def __len__(self) -> int:
        return len(self.index_to_key)

    def __contains__(self, word: str) -> bool:
        return word in self.key_to_index

    def __getitem__(self, word: str) -> np.ndarray:
        return self.vectors[self.key_to_index[word]]

    def most_similar(self, positive=None, negative=None, topn: int = 10):
        """Return the topn words closest to sum(positive) - sum(negative)."""
        if isinstance(positive, str):
            positive = [positive]
        positive = list(positive or [])
        negative = list(negative or [])

        query = np.zeros(self.vectors.shape[1], dtype=np.float32)
        for word in positive:
            query += self._unit[self.key_to_index[word]]
        for word in negative:
            query -= self._unit[self.key_to_index[word]]
        query /= np.linalg.norm(query)

        scores = self._unit @ query
        # the input words themselves are never interesting as a result
        for word in positive + negative:
            scores[self.key_to_index[word]] = -np.inf

        best = np.argpartition(-scores, topn)[:topn]
        best = best[np.argsort(-scores[best])]
        return [(self.index_to_key[i], float(scores[i])) for i in best]


def _download(num_bytes: int, path: Path) -> None:
    """Fetch the first num_bytes of the vector file into path.

    The download is written to a *.part file and only renamed once it is
    complete, so an aborted transfer is never mistaken for a valid cache.
    A dropped connection is resumed with a new range request.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(".part")
    done = part.stat().st_size if part.exists() else 0
    print(f"Downloading {num_bytes / 1e6:.0f} MB from Hugging Face ...")

    for _ in range(10):  # retry budget for dropped connections
        if done >= num_bytes:
            break
        headers = {"Range": f"bytes={done}-{num_bytes - 1}"}
        request = urllib.request.Request(URL, headers=headers)
        with urllib.request.urlopen(request) as response, open(part, "ab") as file:
            while chunk := response.read(1 << 20):
                file.write(chunk)
                done += len(chunk)
                print(f"\r  {done / 1e6:7.0f} / {num_bytes / 1e6:.0f} MB", end="")
    print()

    if done < num_bytes:
        raise OSError(f"download incomplete: {done} of {num_bytes} bytes, kept {part}")
    part.replace(path)


def load_word2vec(limit: int = 50_000) -> WordVectors:
    """Load the limit most frequent word2vec vectors, downloading if needed."""
    path = CACHE_DIR / f"GoogleNews-{limit}.bin"
    if not path.exists():
        _download(64 + limit * BYTES_PER_WORD, path)

    words, vectors = [], []
    with open(path, "rb") as file:
        _, dim = (int(x) for x in file.readline().split())
        record = 4 * dim
        while len(words) < limit:
            word = bytearray()
            while (char := file.read(1)) not in (b" ", b""):
                if char != b"\n":  # some writers separate records by newline
                    word += char
            payload = file.read(record)
            if len(payload) < record:  # truncated last record of the range
                break
            words.append(word.decode("utf-8", errors="replace"))
            vectors.append(struct.unpack(f"<{dim}f", payload))

    return WordVectors(words, np.array(vectors, dtype=np.float32))
