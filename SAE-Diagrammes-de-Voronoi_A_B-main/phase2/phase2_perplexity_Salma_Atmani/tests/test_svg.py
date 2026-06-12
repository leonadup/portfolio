from voronoi_app.domain.geometry import Point
from voronoi_app.domain.voronoi import compute_voronoi_diagram
from voronoi_app.infrastructure.svg_renderer import render_voronoi_to_svg

def test_svg_tags():
    d = compute_voronoi_diagram([Point(0,0), Point(10,0), Point(0,10)])
    svg = render_voronoi_to_svg(d)
    assert "<svg" in svg and "<polygon" in svg and "<circle" in svg
