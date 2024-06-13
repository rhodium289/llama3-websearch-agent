from tools.web_search import web_search_tool

# Node - Perform Web Search
def perform_web_search(state):
    search_query = state['search_query']
    print(f'Step: Searching the Web for: "{search_query}"')
    search_result = web_search_tool.invoke(search_query)
    return {"context": search_result}