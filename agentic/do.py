# Displaying final output format
from IPython.display import display, Markdown, Latex
# LangChain Dependencies
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langgraph.graph import END, StateGraph
# For State Graph 
from typing_extensions import TypedDict
import os

# Environment Variables
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ["LANGCHAIN_PROJECT"] = "L3 Research Agent"

# Defining LLM
local_llm = 'llama3:8b'
llama3 = ChatOllama(model=local_llm, temperature=0)
llama3_json = ChatOllama(model=local_llm, format='json', temperature=0)

# Web Search Tool

wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)

# Test Run
# resp = web_search_tool.invoke("home depot news")
# resp

# Generation Prompt

generate_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an AI assistant for Research Question Tasks, that synthesizes web search results. 
    Strictly use the following pieces of web search context to answer the question. If you don't know the answer, just say that you don't know. 
    keep the answer concise, but provide all of the details you can in the form of a research report. 
    Only make direct references to material if provided in the context.
    
    <|eot_id|>
    
    <|start_header_id|>user<|end_header_id|>
    
    Question: {question} 
    Web Search Context: {context} 
    Answer: 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)

# Chain
generate_chain = generate_prompt | llama3 | StrOutputParser()

# Test Run
# question = "How are you?"
# context = ""
# generation = generate_chain.invoke({"context": context, "question": question})
# print(generation)

# Router

router_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|>
    
    You are an expert at routing a user question to either the generation stage or web search. 
    Use the web search for questions that require more context for a better answer, or recent events.
    Otherwise, you can skip and go straight to the generation phase to respond.
    You do not need to be stringent with the keywords in the question related to these topics.
    Give a binary choice 'web_search' or 'generate' based on the question. 
    Return the JSON with a single key 'choice' with no premable or explanation. 
    
    Question to route: {question} 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    
    """,
    input_variables=["question"],
)

# Chain
question_router = router_prompt | llama3_json | JsonOutputParser()

# Test Run
question = "What's up?"
print(question_router.invoke({"question": question}))

# Query Transformation

query_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an expert at crafting web search queries for research questions.
    More often than not, a user will ask a basic question that they wish to learn more about, however it might not be in the best format. 
    Reword their query to be the most effective web search string possible.
    Return the JSON with a single key 'query' with no premable or explanation. 
    
    Question to transform: {question} 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    
    """,
    input_variables=["question"],
)

# Chain
query_chain = query_prompt | llama3_json | JsonOutputParser()

# Test Run
question = "What's happened recently with Macom?"
print(query_chain.invoke({"question": question}))

# Graph State
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        search_query: revised question for web search
        context: web_search result
    """
    question : str
    generation : str
    search_query : str
    context : str

# Node - Generate

def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    
    print("Step: Generating Final Response")
    question = state["question"]
    context = state["context"]

    # Answer Generation
    generation = generate_chain.invoke({"context": context, "question": question})
    return {"generation": generation}

# Node - Query Transformation

def transform_query(state):
    """
    Transform user question to web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended search query
    """
    
    print("Step: Optimizing Query for Web Search")
    question = state['question']
    gen_query = query_chain.invoke({"question": question})
    search_query = gen_query["query"]
    return {"search_query": search_query}


# Node - Web Search

def web_search(state):
    """
    Web search based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to context
    """

    search_query = state['search_query']
    print(f'Step: Searching the Web for: "{search_query}"')
    
    # Web search tool call
    search_result = web_search_tool.invoke(search_query)
    return {"context": search_result}


# Conditional Edge, Routing

def route_question(state):
    """
    route question to web search or generation.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("Step: Routing Query")
    question = state['question']
    output = question_router.invoke({"question": question})
    if output['choice'] == "web_search":
        print("Step: Routing Query to Web Search")
        return "websearch"
    elif output['choice'] == 'generate':
        print("Step: Routing Query to Generation")
        return "generate"
    
    # Build the nodes
workflow = StateGraph(GraphState)
workflow.add_node("websearch", web_search)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)

# Build the edges
workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "websearch")
workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", END)

## show the graph if possible
from IPython.display import Image, display
from exceptiongroup import catch


    
# Compile the workflow
local_agent = workflow.compile()

from PIL import Image as PILImage
import io

try:
    image_data = io.BytesIO(local_agent.get_graph(xray=True).draw_mermaid_png())
    pil_image = PILImage.open(image_data)
    pil_image.save("graph.png")
    pil_image.show()
# catch the exception and print the error message
except Exception as e:
    print(e)

from rich.console import Console as RichConsole
from rich.markdown import Markdown as RichMarkdown

def run_agent(query):
    output = local_agent.invoke({"question": query})
    print("=======")
    markdown_content = Markdown(output["generation"])
    display(markdown_content)
    # Create a console object
    console = RichConsole()
    # Create a Markdown object
    markdown = RichMarkdown(output["generation"])
    # Render the Markdown in the terminal
    console.print(markdown)


# Test it out!
#run_agent("Tell me about the histore of ACE and Vivace the IT arm of the Home Office in partnership with Qinetic, and what is the relationship with becrypt for the SOC services? Is becrypt related to Qiinetic in anyway at all?")
#run_agent("Whats the best way for me to generate docx files from templates that have standard sections, the content for which will be provided in json format?")
#run_agent("I'd like to use DocRaptor but unformtunately it is a paid service. Is there an opensource alternative that I can use to generate docx files json based on templates using python? Also do any othese solution support having a web dashboard for managing the templates and an API for generating the docx files?")
run_agent("Produce me a taxonomy of the different types of AI models and their use cases. Also provide me with a list of the most popular AI models and their use cases.")



