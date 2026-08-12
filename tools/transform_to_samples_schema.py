#!/usr/bin/env python3
"""
transform_to_samples_schema.py

Converts the raw NetworkX node_link_data graph.json produced by
`opengraph-image build` into the OpenGraph Samples schema:
  - Node IDs are snake_case
  - Node IDs use type prefixes: entity_, concept_, event_, attr_
  - Top-level key is "edges" (not "links")

Type mapping:
  image, object -> entity_
  scene         -> concept_
  attribute     -> attr_
  text_span     -> attr_

Usage:
    python3 transform_to_samples_schema.py path/to/raw_graph.json path/to/graph.json "Example Title"
"""

import json
import re
import sys

TYPE_PREFIX = {
    "image": "entity",
    "object": "entity",
    "scene": "concept",
    "attribute": "attr",
    "text_span": "attr",
}

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(raw_id: str) -> str:
    s = raw_id.lower()
    s = SLUG_RE.sub("_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "node"


def transform(raw_path: str, out_path: str, title: str) -> None:
    with open(raw_path) as f:
        raw = json.load(f)

    raw_nodes = raw.get("nodes", [])
    raw_links = raw.get("links", raw.get("edges", []))

    id_map = {}
    used_ids = set()
    out_nodes = []

    for node in raw_nodes:
        raw_id = str(node.get("id"))
        node_type = node.get("type", "object")
        prefix = TYPE_PREFIX.get(node_type, "entity")

        # Build a label to slugify from -- prefer label/key+value/text, fall back to raw id
        if node_type == "attribute":
            base = f"{node.get('key', '')}_{node.get('value', '')}"
        elif node_type == "text_span":
            base = node.get("text", raw_id)
        else:
            base = node.get("label", raw_id)

        slug = slugify(base)
        new_id = f"{prefix}_{slug}"

        # De-duplicate
        final_id = new_id
        counter = 2
        while final_id in used_ids:
            final_id = f"{new_id}_{counter}"
            counter += 1
        used_ids.add(final_id)

        id_map[raw_id] = final_id

        label = node.get("label") or node.get("text") or node.get("value") or slug.replace("_", " ")

        out_nodes.append({
            "id": final_id,
            "label": label,
            "description": _describe(node),
        })

    out_edges = []
    for link in raw_links:
        src = id_map.get(str(link.get("source")))
        tgt = id_map.get(str(link.get("target")))
        if not src or not tgt:
            continue
        out_edges.append({
            "source": src,
            "target": tgt,
            "label": link.get("relation", "related_to"),
        })

    result = {
        "title": title,
        "nodes": out_nodes,
        "edges": out_edges,
    }

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Wrote {out_path}: {len(out_nodes)} nodes, {len(out_edges)} edges")


def _describe(node: dict) -> str:
    node_type = node.get("type", "")
    if node_type == "image":
        return f"Source image ({node.get('width')}x{node.get('height')} {node.get('format', '')})"
    if node_type == "object":
        return f"Detected object, confidence {node.get('confidence', 'n/a')}"
    if node_type == "scene":
        return f"Scene classification, confidence {node.get('confidence', 'n/a')}"
    if node_type == "attribute":
        return f"{node.get('key', 'attribute')}: {node.get('value', '')}"
    if node_type == "text_span":
        return f"Detected text: {node.get('text', '')}"
    return ""


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python3 transform_to_samples_schema.py path/to/raw_graph.json path/to/graph.json "Title"')
        sys.exit(1)

    transform(sys.argv[1], sys.argv[2], sys.argv[3])
