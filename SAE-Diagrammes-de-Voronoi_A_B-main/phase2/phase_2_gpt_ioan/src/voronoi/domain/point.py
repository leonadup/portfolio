from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Point:
    """
    Represents a point in a 2D plane.

    Attributes:
        x (float): X coordinate.
        y (float): Y coordinate.
    """
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """
        Computes Euclidean distance to another point.
        """
        return math.hypot(self.x - other.x, self.y - other.y)