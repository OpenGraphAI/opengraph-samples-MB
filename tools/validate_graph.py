#!/usr/bin/env python3
"""
validate_graph.py

Checks a graph.json against the OpenGraph Samples schema rules:
  - Node IDs are snake_case
  - Node IDs use correct type prefixes: entity_, concept_, event_, attr_
  - No duplicate node IDs

Usage:
    python3 validate_graph.py path/to/graph.json
"""

import json
import re
import sys

VALID_PREFIXES = ("entity_", "concept_", "event_", "attr_")
SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")


def validate(graph_path: str) -> bool:
    with open(graph_path) as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    errors = []
    seen_ids = set()
    node_ids = set()

    for i, node in enumerate(nodes):
        node_id = node.get("id", "")
        node_ids.add(node_id)

        if not node_id:
            errors.append(f"Node at index {i} is missing an 'id' field")
            continue

        if node_id in seen_ids:
            errors.append(f"Duplicate node ID: '{node_id}'")
        seen_ids.add(node_id)

        if not node_id.startswith(VALID_PREFIXES):
            errors.append(
                f"Node '{node_id}' does not start with a valid prefix "
                f"({', '.join(VALID_PREFIXES)})"
            )

        if not SNAKE_CASE_RE.match(node_id):
            errors.append(f"Node '{node_id}' is not valid snake_case")

    # Sanity-check edges reference real nodes
    for i, edge in enumerate(edges):
        src = edge.get("source")
        tgt = edge.get("target")
        if src not in node_ids:
            errors.append(f"Edge at index {i} references unknown source node '{src}'")
        if tgt not in node_ids:
            errors.append(f"Edge at index {i} references unknown target node '{tgt}'")

    print(f"Checked {len(nodes)} nodes, {len(edges)} edges.")

    if errors:
        print(f"\n{len(errors)} problem(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        return False

    print("All checks passed.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 validate_graph.py path/to/graph.json")
        sys.exit(1)

    ok = validate(sys.argv[1])
    sys.exit(0 if ok else 1)
