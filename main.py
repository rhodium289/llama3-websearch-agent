from utils.display import display_markdown_output
from tools.graph_state import local_agent
from utils.generate_graph_png import generate_graph_png

def run_agent(query):
    output = local_agent.invoke({"question": query})
    print("=======")
    display_markdown_output(output["generation"])

if __name__ == "__main__":
    # Generate the graph PNG
    generate_graph_png(local_agent, "graph.png")
    run_agent("What are the Wikipedia details for Henry Ford?")