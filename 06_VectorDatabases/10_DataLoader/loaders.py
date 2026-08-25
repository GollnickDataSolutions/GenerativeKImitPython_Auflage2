#%% Packages
from collections.abc import Iterator
from pathlib import Path

import requests
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

#%% TextLoader
class TextLoader(BaseLoader):
    """Laedt eine einzelne Textdatei als LangChain-Document.

    Nur lazy_load() muss implementiert werden. Die Methoden load(), aload()
    und load_and_split() erbt die Klasse von BaseLoader.
    """

    def __init__(self, file_path: str | Path, encoding: str = "utf-8"):
        self.file_path = Path(file_path)
        self.encoding = encoding

    def lazy_load(self) -> Iterator[Document]:
        yield Document(
            page_content=self.file_path.read_text(encoding=self.encoding),
            metadata={"source": str(self.file_path)},
        )

#%% WebLoader
class WebLoader(BaseLoader):
    """Laedt eine Textdatei von einer URL als LangChain-Document.

    Der TextLoader arbeitet mit Path und kann deshalb nur lokale Dateien lesen.
    Fuer Quellen aus dem Netz (z. B. Project Gutenberg) ist diese Klasse zustaendig.
    """

    def __init__(self, url: str, encoding: str = "utf-8"):
        self.url = url
        self.encoding = encoding

    def lazy_load(self) -> Iterator[Document]:
        response = requests.get(self.url, timeout=30)
        # bei HTTP-Fehlern (404, 500, ...) eine Exception ausloesen
        response.raise_for_status()
        response.encoding = self.encoding
        yield Document(
            page_content=response.text,
            metadata={"source": self.url},
        )

#%% DirectoryLoader
class DirectoryLoader(BaseLoader):
    """Laedt alle passenden Dateien eines Verzeichnisses als LangChain-Documents.

    Die eigentliche Arbeit uebernimmt pro Datei ein anderer Loader (loader_cls),
    dessen lazy_load() hier nur durchgereicht wird. Die Signatur entspricht der
    von langchain.document_loaders.DirectoryLoader.
    """

    def __init__(
        self,
        path: str | Path,
        glob: str = "**/*.txt",
        loader_cls: type[BaseLoader] = TextLoader,
        loader_kwargs: dict | None = None,
    ):
        self.path = Path(path)
        self.glob = glob
        self.loader_cls = loader_cls
        # kein veraenderliches Default-Argument verwenden
        self.loader_kwargs = loader_kwargs or {}

    def lazy_load(self) -> Iterator[Document]:
        # sorted() sorgt fuer eine reproduzierbare Reihenfolge der Dokumente
        for file_path in sorted(self.path.glob(self.glob)):
            if file_path.is_file():
                yield from self.loader_cls(file_path, **self.loader_kwargs).lazy_load()

#%% WikipediaLoader
API_URL = "https://{lang}.wikipedia.org/w/api.php"

class WikipediaLoader(BaseLoader):
    """Laedt Wikipedia-Artikel als LangChain-Documents.

    Spricht die MediaWiki-API direkt mit requests an. Damit kommt der Loader
    ohne langchain_community aus, dessen WikipediaLoader sonst noetig waere.
    Die Signatur entspricht der des Community-Loaders, damit vorhandener Code
    unveraendert weiterlaeuft.
    """

    def __init__(
        self,
        query: str,
        load_max_docs: int = 25,
        doc_content_chars_max: int = 4000,
        load_all_available_meta: bool = False,
        lang: str = "en",
    ):
        self.query = query
        self.load_max_docs = load_max_docs
        self.doc_content_chars_max = doc_content_chars_max
        self.load_all_available_meta = load_all_available_meta
        self.api_url = API_URL.format(lang=lang)

    def _get(self, params: dict) -> dict:
        """Ruft die API auf und gibt die Antwort als Dictionary zurueck."""
        response = requests.get(
            self.api_url,
            params={"action": "query", "format": "json", **params},
            # die API verlangt einen aussagekraeftigen User-Agent
            headers={"User-Agent": "GenerativeKI-Buch/1.0 (Lernbeispiel)"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def _search_titles(self) -> list[str]:
        """Sucht zur Anfrage passende Artikel und gibt deren Titel zurueck."""
        data = self._get({
            "list": "search",
            "srsearch": self.query.replace("_", " "),
            "srlimit": self.load_max_docs,
        })
        return [hit["title"] for hit in data["query"]["search"]]

    def lazy_load(self) -> Iterator[Document]:
        for title in self._search_titles():
            data = self._get({
                "titles": title,
                "prop": "extracts|info|categories",
                "explaintext": 1,  # Klartext statt HTML
                "exlimit": 1,      # Volltext gibt es nur fuer eine Seite je Aufruf
                "inprop": "url",
                "cllimit": "max",
            })
            page = next(iter(data["query"]["pages"].values()))
            extract = page.get("extract", "")

            metadata = {
                "title": page["title"],
                "source": page["fullurl"],
                # der erste Absatz des Artikels dient als Zusammenfassung
                "summary": extract.split("\n", 1)[0],
            }
            if self.load_all_available_meta:
                metadata.update({
                    "pageid": page["pageid"],
                    "lastrevid": page["lastrevid"],
                    "categories": [c["title"] for c in page.get("categories", [])],
                })

            yield Document(
                page_content=extract[: self.doc_content_chars_max],
                metadata=metadata,
            )
# %%
