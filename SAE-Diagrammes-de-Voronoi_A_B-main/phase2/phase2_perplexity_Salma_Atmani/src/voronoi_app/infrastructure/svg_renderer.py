from __future__ import annotations
from ..domain.geometry import Point, Polygon
from ..domain.voronoi import VoronoiDiagram

def _polygon_to_svg_points(poly: Polygon) -> str:
    return " ".join(f"{p.x},{p.y}" for p in poly)

def bounding_box_from_cells(diagram: VoronoiDiagram) -> tuple[Point, Point]:
    xs, ys = [], []
    for cell in diagram.cells.values():
        for p in cell.polygon:
            xs.append(p.x); ys.append(p.y)
    if not xs:
        raise ValueError("Empty diagram.")
    return Point(min(xs), min(ys)), Point(max(xs), max(ys))

def render_voronoi_to_svg(diagram: VoronoiDiagram) -> str:
    (min_pt, max_pt) = bounding_box_from_cells(diagram)
    width = max_pt.x - min_pt.x
    height = max_pt.y - min_pt.y
    elems: list[str] = []
    elems.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_pt.x} {min_pt.y} {width} {height}">')
    elems.append(f'<rect x="{min_pt.x}" y="{min_pt.y}" width="{width}" height="{height}" stroke="black" fill="none" stroke-width="0.5"/>')
    for cell in diagram.cells.values():
        if not cell.polygon:
            continue
        pts = _polygon_to_svg_points(cell.polygon)
        elems.append(f'<polygon points="{pts}" stroke="black" fill="#dddddd" fill-opacity="0.35" stroke-width="0.5"/>')
    radius = 0.5 * min(width, height) * 0.01 if width > 0 and height > 0 else 1.0
    for cell in diagram.cells.values():
        p = cell.site
        elems.append(f'<circle cx="{p.x}" cy="{p.y}" r="{radius}" stroke="black" fill="black" stroke-width="0.2"/>')
    elems.append("</svg>")
    return "\n".join(elems)

def save_svg(diagram: VoronoiDiagram, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_voronoi_to_svg(diagram))
