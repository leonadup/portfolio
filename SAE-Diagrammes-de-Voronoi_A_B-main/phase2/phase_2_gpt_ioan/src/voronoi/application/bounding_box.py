from typing import List
from voronoi.domain.point import Point


class BoundingBox:
    """
    Defines a bounding box to clip infinite Voronoï regions.
    """

    def __init__(self, points: List[Point], margin: float = 10.0):
        xs = [p.x for p in points]
        ys = [p.y for p in points]

        self.min_x = min(xs) - margin
        self.max_x = max(xs) + margin
        self.min_y = min(ys) - margin
        self.max_y = max(ys) + margin