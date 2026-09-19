# Forest Trees

An interactive knowledge graph extracted from a dense forest photograph, showing how OpenGraph AI decomposes a heavily wooded scene into individual objects, scene classification, and visual attributes.

## Source data

- **Image:** ["Forest trees"](https://unsplash.com/photos/forest-trees-jFCViYFYcus) by [Lukasz Szmigiel](https://unsplash.com/@szmigieldesign) on Unsplash
- **License:** [Unsplash License](https://unsplash.com/license) — free to use, no attribution legally required (credited here as good practice)

## Graph stats

- **Nodes:** 19
- **Edges:** 40

## Generated with

`opengraph-image==0.1.2`

Regenerate with:
```bash
python regenerate.py
```

## Things to notice

- This photo has the highest edge-to-node ratio of the four examples — a dense, repetitive scene (many trees) produces more `related_to` connections between similar objects than a sparse one.
- Hover any `object` node to see its detection confidence — repeated tree trunks often show clustered, similar confidence scores.
- Compare this graph's shape to `park-bench` or `trail-sign` — fewer distinct object *types*, but more instances and relationships between them.
