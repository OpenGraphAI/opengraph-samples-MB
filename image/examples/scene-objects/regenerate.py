"""
Regenerate graph.json and graph.html for this example.

Usage:
    python regenerate.py
"""
from pathlib import Path

from dotenv import load_dotenv
from opengraph_image.graph import build_graph_from_folder

load_dotenv(override=True)

# build_graph_from_folder extracts every image in source/, builds the graph,
# writes graph.json, and also writes graph.html alongside it automatically.
build_graph_from_folder(
    folder=Path("source"),
    output=Path("graph.json"),
)
