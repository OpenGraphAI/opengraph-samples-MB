# Park Bench

An interactive knowledge graph extracted from a photo of a park bench in a grassy, tree-lined field — showing how OpenGraph AI connects a human-made object (the bench) with its natural surroundings.

## Source data

- **Image:** ["A park bench in a green grassy field with trees"](https://unsplash.com/photos/a-park-bench-in-a-green-grassy-field-with-trees-uaPc8sBVdlA) by [Ben Kupke](https://unsplash.com/@benkupke) on Unsplash
- **License:** [Unsplash License](https://unsplash.com/license) — free to use, no attribution legally required (credited here as good practice)

## Graph stats

- **Nodes:** 22
- **Edges:** 31

## Generated with

`opengraph-image==0.1.2`

Regenerate with:
```bash
python regenerate.py
```

## Things to notice

- This example has the most nodes of the four — the scene mixes natural elements (grass, trees) with a human-made object (the bench), giving the extractor more distinct entities to identify.
- Look for `has_attribute` edges connecting the bench to descriptive attributes like material or color.
- Compare the `in_scene` edges here to `forest-trees` — a park setting typically produces a different scene classification than dense forest.
