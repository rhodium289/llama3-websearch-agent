from rich.console import Console
from rich.markdown import Markdown

console = Console()

def display_markdown_output(output):
    # Render the Markdown output using Rich
    markdown = Markdown(output)
    console.print(markdown)