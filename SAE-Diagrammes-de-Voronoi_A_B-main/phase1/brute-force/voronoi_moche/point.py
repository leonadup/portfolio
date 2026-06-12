from typing import Any


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self._x = x
        self._y = y
    
    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y
    
    def distance_to(self, point: 'Point') -> float:
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5
    
    def __str__(self) -> str:
        return f"{self.x}, {self.y}"