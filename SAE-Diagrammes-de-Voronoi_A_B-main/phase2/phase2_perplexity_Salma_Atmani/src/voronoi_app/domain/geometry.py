from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence, Tuple

Number = float

@dataclass(frozen=True)
class Point:
    """2D point."""
    x: Number
    y: Number
    def as_tuple(self) -> Tuple[Number, Number]:
        return (self.x, self.y)

@dataclass(frozen=True)
class Segment:
    """Segment between two points."""
    p1: Point
    p2: Point

@dataclass(frozen=True)
class HalfPlane:
    """
    Half-plane ax + by + c <= 0 kept side.
    """
    a: Number
    b: Number
    c: Number

    def signed_distance(self, p: Point) -> Number:
        return self.a * p.x + self.b * p.y + self.c

    def is_inside(self, p: Point, eps: Number = 1e-9) -> bool:
        return self.signed_distance(p) <= eps

Polygon = List[Point]

def compute_bounding_box(points: Sequence[Point], margin_ratio: float = 0.1) -> Tuple[Point, Point]:
    """Axis-aligned bbox expanded by margin_ratio."""
    if not points:
        raise ValueError("Cannot compute bounding box of empty point set.")
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x
    height = max_y - min_y
    if width == 0:
        width = 1.0
    if height == 0:
        height = 1.0
    dx = width * margin_ratio
    dy = height * margin_ratio
    return (Point(min_x - dx, min_y - dy), Point(max_x + dx, max_y + dy))

def bounding_box_polygon(bottom_left: Point, top_right: Point) -> Polygon:
    """Rectangle polygon (CCW)."""
    return [
        Point(bottom_left.x, bottom_left.y),
        Point(top_right.x, bottom_left.y),
        Point(top_right.x, top_right.y),
        Point(bottom_left.x, top_right.y),
    ]

def bisector_half_plane(p: Point, q: Point) -> HalfPlane:
    """Half-plane of points closer to p than q."""
    mx = 0.5 * (p.x + q.x)
    my = 0.5 * (p.y + q.y)
    nx = q.x - p.x
    ny = q.y - p.y
    c = -(nx * mx + ny * my)
    hp = HalfPlane(a=nx, b=ny, c=c)
    if hp.signed_distance(p) > 0:
        hp = HalfPlane(a=-hp.a, b=-hp.b, c=-hp.c)
    return hp

def segment_intersection_with_half_plane(seg: Segment, hp: HalfPlane, eps: Number = 1e-9):
    """Intersection with the supporting line of hp."""
    d1 = hp.signed_distance(seg.p1)
    d2 = hp.signed_distance(seg.p2)
    denom = d1 - d2
    if abs(denom) < eps:
        return False, None
    t = d1 / denom
    if t < -eps or t > 1 + eps:
        return False, None
    x = seg.p1.x + t * (seg.p2.x - seg.p1.x)
    y = seg.p1.y + t * (seg.p2.y - seg.p1.y)
    return True, Point(x, y)

def clip_polygon_with_half_plane(polygon: Polygon, hp: HalfPlane, eps: Number = 1e-9) -> Polygon:
    """Sutherland–Hodgman clipping against one half-plane."""
    if not polygon:
        return []
    output: Polygon = []
    n = len(polygon)
    for i in range(n):
        current = polygon[i]
        prev = polygon[(i - 1) % n]
        current_inside = hp.is_inside(current, eps)
        prev_inside = hp.is_inside(prev, eps)

        if current_inside:
            if not prev_inside:
                hit, inter = segment_intersection_with_half_plane(Segment(prev, current), hp, eps)
                if hit and inter is not None:
                    output.append(inter)
            output.append(current)
        else:
            if prev_inside:
                hit, inter = segment_intersection_with_half_plane(Segment(prev, current), hp, eps)
                if hit and inter is not None:
                    output.append(inter)
    return output

def polygon_area(polygon: Polygon) -> Number:
    """Signed area (shoelace)."""
    if len(polygon) < 3:
        return 0.0
    s = 0.0
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i].as_tuple()
        x2, y2 = polygon[(i + 1) % n].as_tuple()
        s += x1 * y2 - x2 * y1
    return 0.5 * s

def ensure_ccw(polygon: Polygon) -> Polygon:
    """Ensure CCW ordering."""
    return list(reversed(polygon)) if polygon_area(polygon) < 0 else polygon
