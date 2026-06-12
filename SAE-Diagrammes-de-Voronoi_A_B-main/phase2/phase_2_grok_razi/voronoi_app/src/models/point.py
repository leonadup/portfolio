from dataclasses import dataclass
import math
from typing import Tuple

EPS = 1e-6

@dataclass(frozen=True)
class Point:
    """Représente un point 2D du plan."""
    x: float
    y: float

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (abs(self.x - other.x) < EPS and
                abs(self.y - other.y) < EPS)

    def distance_to(self, other: 'Point') -> float:
        """Distance euclidienne."""
        return math.hypot(self.x - other.x, self.y - other.y)