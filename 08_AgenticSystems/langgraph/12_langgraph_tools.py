#%% packages
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()
#%% LLM 
llm = ChatOpenRouter(model="mistralai/mixtral-8x22b-instruct")

# %% Tools
def count_characters_in_word(word: str, character: str) -> str:
    """Count the number of times a character appears in a word."""
    cnt = word.count(character)
    return f"Das Wort {word} hat {cnt} {character}s."


# %% TEST
count_characters_in_word(word="LOLLAPALOOZA", character="L")
# %% LLM with tools
llm_with_tools = llm.bind_tools([count_characters_in_word])

# %%
llm_with_tools.invoke(["user", "Zähle die L in LOLLAPALOOZA."])
# %% Tool Call
tool_call = llm_with_tools.invoke("Wie viele Ls sind in LOLLAPALOOZA?")

# %%
from pprint import pprint
pprint(tool_call)

#%% graph
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.prebuilt import ToolNode, tools_condition


class MessagesState(TypedDict):
    messages: list[AnyMessage]
    
# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([count_characters_in_word]))
builder.add_edge(START, "tool_calling_llm")
# builder.add_edge("tool_calling_llm", "tools")
builder.add_conditional_edges("tool_calling_llm", 
                              # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition)
builder.add_edge("tools", END)
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

# %% use messages as state
# messages = [HumanMessage(content="Hallo, wie geht es dir?")]
messages = [HumanMessage(content="Zähle die Ls in LOLLAPALOOZA.")]
messages = graph.invoke({"messages": messages})
for m in messages["messages"]:
    print(m.pretty_print())

# %%
