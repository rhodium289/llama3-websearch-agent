import os

os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ["LANGCHAIN_PROJECT"] = "L3 Research Agent"

local_llm = 'llama3:8b'
local_llm_base_url = 'http://192.168.68.171:11434'

# Neo4j connection details
neo4j_uri = "bolt://192.168.68.150:7687"
neo4j_user = "neo4j"
neo4j_password = "TlpV4kEYUI8gMDkE"