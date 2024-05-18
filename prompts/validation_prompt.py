from langchain.prompts import PromptTemplate

validation_prompt_template = PromptTemplate(
    template="""
 
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|>
    
    You are an expert at evaluating the quality of web search results.
    Given the search results, determine if the information is sufficient and accurate to answer the user's question.
    If the search results are adequate, respond with 'valid'.
    If the search results are insufficient or inaccurate, respond with 'invalid'.
    Return the JSON with a single key 'status' with no preamble or explanation.
    
    Search Results: {results}
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    
    """,
    input_variables=["results"],
)
