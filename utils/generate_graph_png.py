import io
from PIL import Image as PILImage

def generate_graph_png(graph, output_path="graph.png"):
    """
    Generates a PNG image of the given graph and saves it to the specified output path.

    Args:
        graph: The graph object to generate the image from.
        output_path (str): The file path to save the PNG image to.
    """
    try:
        image_data = io.BytesIO(graph.get_graph(xray=True).draw_mermaid_png())
        pil_image = PILImage.open(image_data)
        pil_image.save(output_path)
        print(f"Graph saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while generating the graph image: {e}")
