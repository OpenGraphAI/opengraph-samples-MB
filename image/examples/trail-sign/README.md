# Trail Sign

An interactive knowledge graph extracted from a photo of a wooden trail sign in a forest — the only example in this set with readable text in the source image, showing how OpenGraph AI extracts and connects `text_span` nodes.

## Source data

- **Image:** ["A wooden trail sign in the middle of a forest"](https://unsplash.com/photos/Ai2EjJIOunw) by Roger Starnes Sr on Unsplash
- **License:** [Unsplash License](https://unsplash.com/license) — free to use, no attribution legally required (credited here as good practice)

## Graph stats

- **Nodes:** 19
- **Edges:** 27

## Generated with

`opengraph-image==0.1.2`

Regenerate with:
```bash
python regenerate.py
```

## Things to notice

- This is the only example with `text_span` nodes — look for `has_text` edges connecting the sign object to the text detected on it.
- Compare extraction confidence on the text node versus the object nodes; text recognition on weathered/carved wood signage is often a different confidence range than object detection.
- The sign itself is a `has_attribute`-linked object — check what material/attributes got attached to it.
