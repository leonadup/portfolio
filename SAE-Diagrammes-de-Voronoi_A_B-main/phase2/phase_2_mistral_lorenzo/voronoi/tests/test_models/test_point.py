import pytest
from src.models.point import Point

def test_point_distance():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert p1.distance_to(p2) == 5
