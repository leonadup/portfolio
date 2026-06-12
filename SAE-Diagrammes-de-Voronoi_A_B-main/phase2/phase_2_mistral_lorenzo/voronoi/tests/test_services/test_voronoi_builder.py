import pytest
from src.models.point import Point
from src.models.voronoi import VoronoiDiagram

def test_voronoi_builder():
    points = [Point(0, 0), Point(1, 0), Point(0, 1)]
    diagram = VoronoiDiagram(points)
    diagram.build()
    edges = diagram.get_edges()
    assert len(edges) > 0
