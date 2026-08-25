#%% packages
import asyncio

import wikipedia
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

# %% wikipedia tools
# Name, Beschreibung und Parameter-Schema des Tools leitet das SDK
# aus Funktionsname, Docstring und Type Hints ab
@function_tool
def search_wikipedia(query: str) -> list[str]:
    """Search for Wikipedia articles.

    Args:
        query: The search term to look for.
    """
    return wikipedia.search(query)


@function_tool
def get_wikipedia_summary(title: str) -> str:
    """Get the summary of a Wikipedia article.

    Args:
        title: The exact title of the article, e.g. from search_wikipedia.
    """
    try:
        return wikipedia.page(title, auto_suggest=False).summary
    except wikipedia.DisambiguationError as e:
        # der Titel ist mehrdeutig - der Agent bekommt die Alternativen zurueck
        return f"'{title}' is ambiguous. Try one of these titles: {e.options[:10]}"
    except wikipedia.PageError:
        return f"No Wikipedia article found for '{title}'."


# %% Wikipedia Agent
wikipedia_agent = Agent(
    name="Wikipedia Agent",
    instructions="""
    You are a helpful assistant that can answer questions about Wikipedia by finding and analyzing the content of Wikipedia articles.
    You follow these steps:
    1. Find out what the user is interested in
    2. extract keywords
    3. Search for the keywords in Wikipedia using search_wikipedia
    4. From the results list, pick the most relevant article and search with get_wikipedia_summary
    5. If you find an answer, stop and answer. If not, continue with step 3 with a different keyword.
    """,
    tools=[search_wikipedia, get_wikipedia_summary],
    model="gpt-5.6-luna",
)

# %% run the agent
response = asyncio.run(
    Runner.run(wikipedia_agent, input="Was ist Superintelligenz?")
)

# %% fetch the agent response
print(response.final_output)

# %% which tools were called?
for item in response.new_items:
    print(item.type)

#%%
response.raw_responses

# %%
