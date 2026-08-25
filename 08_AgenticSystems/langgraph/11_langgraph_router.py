#%% packages
from typing_extensions import TypedDict
import random
from langgraph.graph import StateGraph, START, END
from langchain_openrouter import ChatOpenRouter
from IPython.display import Image, display
from rich.console import Console
from rich.markdown import Markdown
console = Console()
from dotenv import load_dotenv
load_dotenv()
#%% LLM
llm = ChatOpenRouter(model="google/gemini-2.5-flash")

# State with graph_state
class State(TypedDict):
    graph_state: dict[str, str | dict[str, str | str]]

# Nodes
def node_router(state: State):
    # Retrieve the user-provided topic
    topic = state["graph_state"].get("topic", "Kein Thema angegeben")
    
    # Update the graph_state with any additional information if needed
    state["graph_state"]["processed_topic"] = topic  # Example of updating graph_state

    print(f"Vom Nutzer angegebenes Thema: {topic}")
    return {"graph_state": state["graph_state"]}

def node_pro(state: State):
    topic = state["graph_state"]["topic"]
    pro_args = llm.invoke(f"Erzeuge Argumente für: {topic}. Antworte in Stichpunkten. Maximal 5 Wörter pro Stichpunkt.")
    state["graph_state"]["result"] = {"side": "pro", "arguments": pro_args}
    return {"graph_state": state["graph_state"]}

def node_contra(state: State):
    topic = state["graph_state"]["topic"]
    contra_args = llm.invoke(f"Erzeuge Argumente gegen: {topic}")
    state["graph_state"]["result"] = {"side": "contra", "arguments": contra_args}
    return {"graph_state": state["graph_state"]}

# Edges
def edge_pro_or_contra(state: State):
    decision = random.choice(["node_pro", "node_contra"])
    state["graph_state"]["decision"] = decision
    print(f"Weiterleitung an: {decision}")
    return decision

# Create graph
builder = StateGraph(State)
builder.add_node("node_router", node_router)
builder.add_node("node_pro", node_pro)
builder.add_node("node_contra", node_contra)

builder.add_edge(START, "node_router")
builder.add_conditional_edges(
    "node_router",
    edge_pro_or_contra,
    {"node_contra": "node_contra", "node_pro": "node_pro"},
)
builder.add_edge("node_pro", END)
builder.add_edge("node_contra", END)

graph = builder.compile()

# Invoke the graph with a specific topic

# %%
display(Image(graph.get_graph().draw_mermaid_png()))
# %% Invokation
initial_state = {"graph_state": {"topic": "Sollten Hunde Kleidung tragen?Zeige, ob du Argumente pro oder contra hast. Antworte deutsch und in Stichpunkten mit maximal 5 Wörtern pro Stichpunkt."}}
result = graph.invoke(initial_state)

# %%
console.print(Markdown(result["graph_state"]['result']['arguments'].model_dump()['content']))
# %%