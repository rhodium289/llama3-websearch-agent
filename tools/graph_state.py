from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Graph State
class GraphState(TypedDict):
    question: str
    generation: str
    search_query: str
    context: str
    status: str
    commands: str