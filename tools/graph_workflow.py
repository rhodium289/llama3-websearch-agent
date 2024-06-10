from langgraph.graph import END, StateGraph
from tools.graph_state import GraphState
from nodes.routing import route_question
from nodes.perform_websearch import perform_web_search
from nodes.validate_websearch_results import validate_search_results
from nodes.generate_answer import generate_answer
from nodes.initial_routing import conditional_routing
from nodes.optimise_for_websearch import transform_query   
from nodes.extract_enriched_data import extract_enriched_data 
from nodes.populate_neo4j import populate_neo4j
    
# Build the nodes
workflow = StateGraph(GraphState)

# Build the edges
workflow.set_conditional_entry_point(
    route_question,
    {
        "web_search": "transform_query",
        "generate_answer": "generate_answer",
    },
)

workflow.add_node("transform_query", transform_query)
workflow.add_node("web_search", perform_web_search)
workflow.add_node("validate_search_results", validate_search_results)
workflow.add_node("generate_answer", generate_answer)
workflow.add_node("extract_enriched_data", extract_enriched_data)
workflow.add_node("populate_neo4j", populate_neo4j)

workflow.add_edge("transform_query", "web_search")
workflow.add_edge("web_search", "validate_search_results")
workflow.add_conditional_edges("validate_search_results", conditional_routing, ["extract_enriched_data", "transform_query"])
workflow.add_edge("extract_enriched_data", "populate_neo4j")
workflow.add_edge("populate_neo4j", "generate_answer")
workflow.add_edge("generate_answer", END)

# Compile the workflow
local_agent = workflow.compile()
