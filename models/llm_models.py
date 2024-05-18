from langchain_community.chat_models import ChatOllama

local_llm = 'llama3:8b'
llama3 = ChatOllama(model=local_llm, temperature=0, base_url='http://192.168.68.171:11434')
llama3_json = ChatOllama(model=local_llm, format='json', temperature=0, base_url='http://192.168.68.171:11434')
