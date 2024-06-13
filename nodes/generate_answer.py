from prompts.generate_prompt import generate_prompt_template
from models.llm_models import llama3, llama3_json
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# Node - Generate Answer
def generate_answer(state):
    print("Step: Generating Final Response")
    question = state["question"]
    context = state["context"]
    generate_chain = generate_prompt_template | llama3 | StrOutputParser()
    generation = generate_chain.invoke({"context": context, "question": question})
    return {"generation": generation}