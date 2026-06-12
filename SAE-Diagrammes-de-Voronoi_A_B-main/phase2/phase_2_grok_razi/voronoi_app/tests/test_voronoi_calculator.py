import pytest
from src.algorithms.voronoi_calculator import VoronoiCalculator
from src.models.point import Point


@pytest.fixture
def three_points():
    return [Point(0,0), Point(4,0), Point(2,3)]


def test_3_points_triangle(three_points):
    calc = VoronoiCalculator()
    diagram = calc.compute(three_points)
    assert len(diagram.vertices) == 1               # un sommet Voronoï
    assert len(diagram.edges) == 3                   # 1 arête finie + 2 rayons
    assert len(diagram.sites) == 3