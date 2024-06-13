from prompts.validation_prompt import validation_prompt_template
from models.llm_models import llama3, llama3_json
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Node - Validate Search Results
def validate_search_results(state):
    print("Step: Validating Search Results")
    context = state['context']
    validation_chain = validation_prompt_template | llama3_json | JsonOutputParser()
    validation_result = validation_chain.invoke({"results": context})
    return {"status": validation_result["status"]}