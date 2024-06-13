from prompts.router_prompt import router_prompt_template
from models.llm_models import llama3, llama3_json
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

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