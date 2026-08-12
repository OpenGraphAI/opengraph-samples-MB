#!/usr/bin/env python3
"""
render_graph.py

Renders a graph.json file into a self-contained, interactive graph.html
(pan, zoom, hover, click) styled to match the OpenGraph Samples site.

The graph data is embedded directly into the HTML (not fetched at runtime),
so graph.html works when opened directly via double-click -- no local
server required.

Usage:
    python3 render_graph.py path/to/graph.json path/to/graph.html
"""

import json
import sys

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — OpenGraph Samples</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
  <style>
    :root {{
      --bg: #0B0E14;
      --surface: #131722;
      --surface-border: #232A3A;
      --text: #E8EAF0;
      --text-muted: #8B93A7;
      --accent: #5EEAD4;
      --accent-2: #F0B849;
      --font-display: 'Space Grotesk', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-display);
      overflow: hidden;
    }}
    header {{
      position: fixed;
      top: 0; left: 0; right: 0;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1rem 1.5rem;
      background: linear-gradient(to bottom, var(--bg) 60%, transparent);
      pointer-events: none;
    }}
    header a {{
      pointer-events: auto;
      color: var(--text-muted);
      text-decoration: none;
      font-family: var(--font-mono);
      font-size: 0.8rem;
    }}
    header a:hover {{ color: var(--accent); }}
    header h1 {{
      font-size: 1rem;
      margin: 0;
      font-weight: 600;
    }}
    svg {{ display: block; width: 100vw; height: 100vh; cursor: grab; }}
    svg:active {{ cursor: grabbing; }}
    .link {{
      stroke: var(--surface-border);
      stroke-width: 1.5px;
    }}
    .link.is-highlighted {{
      stroke: var(--accent);
      stroke-width: 2px;
    }}
    .node circle {{
      stroke: var(--bg);
      stroke-width: 2px;
      cursor: pointer;
      transition: r 0.12s ease;
    }}
    .node:hover circle {{
      filter: drop-shadow(0 0 6px var(--accent));
    }}
    .node text {{
      font-family: var(--font-mono);
      font-size: 10px;
      fill: var(--text-muted);
      pointer-events: none;
      user-select: none;
    }}
    .node.is-selected circle {{
      stroke: var(--accent-2);
      stroke-width: 3px;
    }}

    #tooltip {{
      position: fixed;
      pointer-events: none;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 6px;
      padding: 0.6rem 0.8rem;
      font-size: 0.8rem;
      max-width: 260px;
      opacity: 0;
      transition: opacity 0.1s ease;
      z-index: 20;
    }}
    #tooltip .tt-type {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.25rem;
      display: block;
    }}

    #legend {{
      position: fixed;
      bottom: 1.25rem;
      left: 1.25rem;
      z-index: 10;
      display: flex;
      gap: 1rem;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--text-muted);
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 6px;
      padding: 0.6rem 0.9rem;
    }}
    #legend span {{ display: flex; align-items: center; gap: 0.4rem; }}
    #legend i {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <a href="../../../index.html">← Back to OpenGraph Samples</a>
  </header>

  <svg id="graph"></svg>
  <div id="tooltip"></div>
  <div id="legend"></div>

  <script>
    const graphData = {graph_json};

    const typeColors = {{
      entity: '#5EEAD4',
      concept: '#F0B849',
      event: '#EF6461',
      attr: '#8B93A7'
    }};

    function nodeType(id) {{
      const prefix = id.split('_')[0];
      return typeColors[prefix] ? prefix : 'entity';
    }}

    const svg = d3.select('#graph');
    const width = window.innerWidth;
    const height = window.innerHeight;

    const container = svg.append('g');

    svg.call(
      d3.zoom()
        .scaleExtent([0.2, 4])
        .on('zoom', (event) => container.attr('transform', event.transform))
    );

    const nodesById = new Map(graphData.nodes.map(n => [n.id, n]));

    const simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(90))
      .force('charge', d3.forceManyBody().strength(-220))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide().radius(28));

    const link = container.append('g')
      .selectAll('line')
      .data(graphData.edges)
      .join('line')
      .attr('class', 'link');

    const node = container.append('g')
      .selectAll('g')
      .data(graphData.nodes)
      .join('g')
      .attr('class', 'node')
      .call(
        d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      );

    node.append('circle')
      .attr('r', 9)
      .attr('fill', d => typeColors[nodeType(d.id)]);

    node.append('text')
      .attr('dy', 20)
      .attr('text-anchor', 'middle')
      .text(d => d.label || d.id);

    const tooltip = d3.select('#tooltip');

    node
      .on('mouseover', (event, d) => {{
        tooltip
          .style('opacity', 1)
          .html(
            '<span class="tt-type">' + nodeType(d.id) + '</span>' +
            '<strong>' + (d.label || d.id) + '</strong>' +
            (d.description ? '<div>' + d.description + '</div>' : '')
          );
        link.classed('is-highlighted', l => l.source.id === d.id || l.target.id === d.id);
      }})
      .on('mousemove', (event) => {{
        tooltip
          .style('left', (event.clientX + 14) + 'px')
          .style('top', (event.clientY + 14) + 'px');
      }})
      .on('mouseout', () => {{
        tooltip.style('opacity', 0);
        link.classed('is-highlighted', false);
      }})
      .on('click', (event, d) => {{
        node.classed('is-selected', n => n.id === d.id);
      }});

    simulation.on('tick', () => {{
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
    }});

    function dragstarted(event, d) {{
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x; d.fy = d.y;
    }}
    function dragged(event, d) {{
      d.fx = event.x; d.fy = event.y;
    }}
    function dragended(event, d) {{
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null; d.fy = null;
    }}

    // Legend, built from the types actually present in this graph
    const presentTypes = [...new Set(graphData.nodes.map(n => nodeType(n.id)))];
    d3.select('#legend')
      .selectAll('span')
      .data(presentTypes)
      .join('span')
      .html(d => `<i style="background:${{typeColors[d]}}"></i>${{d}}`);
  </script>
</body>
</html>
"""


def render(graph_json_path: str, out_html_path: str) -> None:
    with open(graph_json_path) as f:
        graph = json.load(f)

    title = graph.get("title", "Graph Example")
    html = TEMPLATE.format(title=title, graph_json=json.dumps(graph))

    with open(out_html_path, "w") as f:
        f.write(html)

    print(f"Rendered {out_html_path} ({len(graph.get('nodes', []))} nodes, "
          f"{len(graph.get('edges', []))} edges)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 render_graph.py path/to/graph.json path/to/graph.html")
        sys.exit(1)

    render(sys.argv[1], sys.argv[2])
