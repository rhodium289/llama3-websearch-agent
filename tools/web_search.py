from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)
