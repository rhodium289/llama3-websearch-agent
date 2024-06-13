from langchain_community.chat_models import ChatOllama
from config.config import local_llm, local_llm_base_url

<<<<<<< HEAD
local_llm = 'llama3:8b'
llama3 = ChatOllama(model=local_llm, temperature=0, base_url='http://192.168.68.171:11434')
llama3_json = ChatOllama(model=local_llm, format='json', temperature=0, base_url='http://192.168.68.171:11434')
#llama3 = ChatOllama(model=local_llm, temperature=0, base_url='http://localhost:11434')
#llama3_json = ChatOllama(model=local_llm, format='json', temperature=0, base_url='http://localhost:11434')
=======
llama3 = ChatOllama(model=local_llm, temperature=0, base_url=local_llm_base_url)
llama3_json = ChatOllama(model=local_llm, format='json', temperature=0, base_url=local_llm_base_url)
>>>>>>> dfea80a4a10aa85bf1f6f9279ae3ed709f71c251
