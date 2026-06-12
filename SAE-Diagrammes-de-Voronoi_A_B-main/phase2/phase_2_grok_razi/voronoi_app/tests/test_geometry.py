import math
import pytest
from src.utils.geometry import circumcenter
from src.models.point import Point


def test_circumcenter_equilateral():
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(0.5, math.sqrt(3)/2)
    c = circumcenter(p1, p2, p3)
    assert c is not None
    assert abs(c.x - 0.5) < 1e-6
    assert abs(c.y - math.sqrt(3)/6) < 1e-6


def test_circumcenter_collinear():
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    p3 = Point(2, 2)
    assert circumcenter(p1, p2, p3) is None