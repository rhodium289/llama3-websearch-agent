import os

def set_environment_variables():
    os.environ['LANGCHAIN_TRACING_V2'] = 'false'
    os.environ["LANGCHAIN_PROJECT"] = "L3 Research Agent"
