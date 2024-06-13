from prompts.generate_enr import generate_enr_prompt_template
from models.llm_models import llama3, llama3_json
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Node - Generate Answer
def extract_enriched_data(state):
    print("Step: Extracting enriched data")
    question = state["question"]
    context = state["context"]
    generate_enr_chain = generate_enr_prompt_template | llama3_json | JsonOutputParser()
    enr_result = generate_enr_chain.invoke({"context": context, "question": question})
    return {"commands": enr_result["commands"]}