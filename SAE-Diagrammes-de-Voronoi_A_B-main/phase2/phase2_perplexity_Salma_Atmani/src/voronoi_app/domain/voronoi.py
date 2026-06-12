from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Sequence, Tuple

from .geometry import (
    Point, Polygon, HalfPlane,
    compute_bounding_box, bounding_box_polygon,
    bisector_half_plane, clip_polygon_with_half_plane,
    ensure_ccw,
)

@dataclass(frozen=True)
class VoronoiCell:
    """One Voronoi cell polygon for a site."""
    site: Point
    polygon: Polygon

@dataclass
class VoronoiDiagram:
    """Voronoi diagram: mapping site -> cell."""
    cells: Dict[Tuple[float, float], VoronoiCell]

def compute_voronoi_diagram(points: Sequence[Point]) -> VoronoiDiagram:
    """Half-plane intersection Voronoi clipped to bbox."""
    if len(points) < 2:
        raise ValueError("Voronoi diagram requires at least two points.")
    bottom_left, top_right = compute_bounding_box(points, margin_ratio=0.1)
    bbox_poly = bounding_box_polygon(bottom_left, top_right)

    cells: Dict[Tuple[float, float], VoronoiCell] = {}
    for i, p in enumerate(points):
        poly: Polygon = bbox_poly[:]
        for j, q in enumerate(points):
            if i == j:
                continue
            hp: HalfPlane = bisector_half_plane(p, q)
            poly = clip_polygon_with_half_plane(poly, hp)
            if not poly:
                break
        poly = ensure_ccw(poly)
        cells[p.as_tuple()] = VoronoiCell(site=p, polygon=poly)
    return VoronoiDiagram(cells=cells)
