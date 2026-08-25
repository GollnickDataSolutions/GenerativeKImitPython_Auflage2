#%% packages
import os
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
load_dotenv()
# %%
# Model overview: https://console.groq.com/docs/models
MODEL_NAME = '~deepseek/deepseek-v4-flash-latest'
model = ChatOpenRouter(model_name=MODEL_NAME,
                   temperature=0.5, # controls creativity
                   api_key=os.getenv('OPENROUTER_API_KEY'))

# %% Run the model
res = model.invoke("Was ist HuggingFace?")
# %% find out what is in the result
res.model_dump()
# %% only print content
print(res.content)
