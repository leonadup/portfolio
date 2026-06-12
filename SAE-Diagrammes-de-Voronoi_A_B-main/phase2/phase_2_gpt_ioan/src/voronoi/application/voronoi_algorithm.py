import math
from typing import List
from voronoi.domain.point import Point
from voronoi.domain.polygon import Polygon
from .bounding_box import BoundingBox


class VoronoiAlgorithm:
    """
    Naive O(n^3) Voronoï diagram construction using half-plane intersections.
    """

    def compute(self, points: List[Point]) -> List[Polygon]:
        bbox = BoundingBox(points)
        regions = []

        for site in points:
            region = self._initial_rectangle(bbox)

            for other in points:
                if site == other:
                    continue
                region = self._clip_with_bisector(region, site, other)

            regions.append(Polygon(region))

        return regions

    def _initial_rectangle(self, bbox: BoundingBox) -> List[Point]:
        return [
            Point(bbox.min_x, bbox.min_y),
            Point(bbox.max_x, bbox.min_y),
            Point(bbox.max_x, bbox.max_y),
            Point(bbox.min_x, bbox.max_y),
        ]

    def _clip_with_bisector(
        self,
        polygon: List[Point],
        p1: Point,
        p2: Point
    ) -> List[Point]:
        """
        Clips polygon by perpendicular bisector between p1 and p2.
        """
        def is_inside(point: Point) -> bool:
            return point.distance_to(p1) <= point.distance_to(p2)

        new_polygon = []
        for i in range(len(polygon)):
            current = polygon[i]
            next_point = polygon[(i + 1) % len(polygon)]

            if is_inside(current):
                new_polygon.append(current)

            if is_inside(current) != is_inside(next_point):
                intersection = self._compute_intersection(current, next_point, p1, p2)
                if intersection:
                    new_polygon.append(intersection)

        return new_polygon

    def _compute_intersection(
        self,
        a: Point,
        b: Point,
        p1: Point,
        p2: Point
    ) -> Point:
        """
        Computes intersection between segment AB and bisector of p1,p2.
        """
        mid_x = (p1.x + p2.x) / 2
        mid_y = (p1.y + p2.y) / 2

        dx = p2.x - p1.x
        dy = p2.y - p1.y

        A = dx
        B = dy
        C = -(A * mid_x + B * mid_y)

        denom = A * (b.x - a.x) + B * (b.y - a.y)
        if denom == 0:
            return None

        t = -(A * a.x + B * a.y + C) / denom

        if 0 <= t <= 1:
            return Point(a.x + t * (b.x - a.x), a.y + t * (b.y - a.y))

        return None