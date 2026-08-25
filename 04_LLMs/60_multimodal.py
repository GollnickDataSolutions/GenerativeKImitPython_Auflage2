#%% packages
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv, find_dotenv
load_dotenv()
import base64
# %%
MODEL = "google/gemini-2.5-flash"
IMAGE_PATH = "sample_image.png"
USER_PROMPT = "Was ist in diesem Bild zu sehen? Antworte in einem Satz."
# %%
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(IMAGE_PATH)
#%% message with text and image side by side
message = HumanMessage(content=[
    {"type": "text", "text": USER_PROMPT},
    {"type": "image", "base64": base64_image, "mime_type": "image/png"},
])
#%% send it to the model
model = ChatOpenRouter(model_name=MODEL)
res = model.invoke([message])
#%% analyze the output
res.model_dump()
#%% only print content
print(res.content)
# %%
