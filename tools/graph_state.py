from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from models.llm_models import llama3, llama3_json
from prompts.generate_prompt import generate_prompt_template
from prompts.router_prompt import router_prompt_template
from prompts.query_prompt import query_prompt_template
from prompts.validation_prompt import validation_prompt_template
from tools.web_search import web_search_tool
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Graph State
class GraphState(TypedDict):
    question: str
    generation: str
    search_query: str
    context: str
    status: str

# Node - Route Question
def route_question(state):
    print("Step: Routing Query")
    question = state['question']
    question_router = router_prompt_template | llama3_json | JsonOutputParser()
    output = question_router.invoke({"question": question})
    if output['choice'] == "web_search":
        print("Step: Routing Query to Web Search")
        return "web_search"
    elif output['choice'] == 'generate':
        print("Step: Routing Query to Generation")
        return "generate_answer"
    else:
        raise ValueError("Invalid choice")
    
# Node - Transform Query
def transform_query(state):
    print("Step: Optimizing Query for Web Search")
    question = state['question']
    query_chain = query_prompt_template | llama3_json | JsonOutputParser()
    gen_query = query_chain.invoke({"question": question})
    search_query = gen_query["query"]
    return {"search_query": search_query}

# Node - Perform Web Search
def perform_web_search(state):
    search_query = state['search_query']
    print(f'Step: Searching the Web for: "{search_query}"')
    search_result = web_search_tool.invoke(search_query)
    return {"context": search_result}

# define a global first time flag
first_time = True

# Node - Validate Search Results
def validate_search_results(state):
    global first_time
    print("Step: Validating Search Results")
    context = state['context']
    validation_chain = validation_prompt_template | llama3_json | JsonOutputParser()
    validation_result = validation_chain.invoke({"results": context})
    # fail the first time then use validatrion_result["status"]
    if first_time:
        first_time = False
        print("Step: Forcing Validation Failure")
        return {"status": "invalid"}
    else:
        return {"status": validation_result["status"]}

# Node - Generate Answer
def generate_answer(state):
    print("Step: Generating Final Response")
    question = state["question"]
    context = state["context"]
    generate_chain = generate_prompt_template | llama3 | StrOutputParser()
    generation = generate_chain.invoke({"context": context, "question": question})
    return {"generation": generation}

# Conditional Routing Function
def conditional_routing(state):
    status = state["status"]
    if status == "valid":
        return "generate_answer"
    elif status == "invalid":
        return "transform_query"
    else:
        raise ValueError("Invalid status")
    
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

workflow.add_edge("transform_query", "web_search")
workflow.add_edge("web_search", "validate_search_results")
workflow.add_conditional_edges("validate_search_results", conditional_routing, ["generate_answer", "transform_query"])
workflow.add_edge("generate_answer", END)

# Compile the workflow
local_agent = workflow.compile()
