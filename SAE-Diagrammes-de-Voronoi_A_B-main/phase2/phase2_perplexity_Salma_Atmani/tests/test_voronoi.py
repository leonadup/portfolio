from voronoi_app.domain.geometry import Point
from voronoi_app.domain.voronoi import compute_voronoi_diagram

def test_voronoi_non_empty():
    d = compute_voronoi_diagram([Point(0,0), Point(10,0), Point(0,10)])
    assert len(d.cells) == 3
    assert all(cell.polygon for cell in d.cells.values())
