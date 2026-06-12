from voronoi.application.voronoi_algorithm import VoronoiAlgorithm
from voronoi.domain.point import Point


def test_voronoi_two_points():
    points = [Point(0, 0), Point(10, 0)]

    algorithm = VoronoiAlgorithm()
    regions = algorithm.compute(points)

    assert len(regions) == 2
    assert all(len(region.vertices) >= 3 for region in regions)