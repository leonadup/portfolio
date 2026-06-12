from dataclasses import dataclass
from .point import Point


@dataclass
class Edge:
    """
    Represents a line segment between two points.
    """
    start: Point
    end: Point