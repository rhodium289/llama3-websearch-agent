from prompts.query_prompt import query_prompt_template
from models.llm_models import llama3, llama3_json
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Node - Transform Query
def transform_query(state):
    print("Step: Optimizing Query for Web Search")
    question = state['question']
    query_chain = query_prompt_template | llama3_json | JsonOutputParser()
    gen_query = query_chain.invoke({"question": question})
    search_query = gen_query["query"]
    return {"search_query": search_query}