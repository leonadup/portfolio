from typing import List
from .point import Point


class Polygon:
    """
    Represents a polygon defined by a list of points.
    """

    def __init__(self, vertices: List[Point]):
        self._vertices = vertices

    @property
    def vertices(self) -> List[Point]:
        return self._vertices