from langchain_community.chat_models import ChatOllama
from config.config import local_llm, local_llm_base_url

llama3 = ChatOllama(model=local_llm, temperature=0, base_url=local_llm_base_url)
llama3_json = ChatOllama(model=local_llm, format='json', temperature=0, base_url=local_llm_base_url)
