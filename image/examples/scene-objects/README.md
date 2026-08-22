# Scene Objects

An interactive knowledge graph extracted from a single outdoor nature photograph, showing how OpenGraph AI decomposes an image into its constituent objects, scene context, visual attributes, and any embedded text — then connects them into a queryable graph.

## Source data

- **Image:** ["Tree in Nicaragua"](https://unsplash.com/photos/tGTVxeOr_Rs) by [niko photos](https://unsplash.com/@niko_photos) on Unsplash
- **License:** [Unsplash License](https://unsplash.com/license) — free to use, no attribution legally required (credited here as good practice)

## Graph stats

- **Nodes:** 19
- **Edges:** 23

## Generated with

`opengraph-image==0.1.2`

Regenerate with:
```bash
python regenerate.py
```

## Things to notice

- Nodes are typed (`image`, `object`, `scene`, `attribute`, `text_span`) — hover any node to see its type and confidence score.
- Edges carry semantic labels (`contains`, `in_scene`, `has_attribute`, `has_text`) rather than generic links, so you can trace *why* two nodes are connected, not just *that* they are.
- Click a node to focus and zoom in on it, then hover its neighbors to trace its full set of relationships.
- Some nodes carry confidence scores from the extraction model — lower-confidence nodes are worth comparing against the source image to see where automated extraction is more or less certain.

