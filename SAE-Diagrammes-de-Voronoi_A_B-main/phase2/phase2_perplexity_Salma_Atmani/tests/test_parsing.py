import io
import pytest
from voronoi_app.infrastructure.parsing import parse_points_stream, PointParseError

def test_parse_ok():
    pts = parse_points_stream(io.StringIO("0,0\n1,1\n"))
    assert len(pts) == 2

def test_parse_bad():
    with pytest.raises(PointParseError):
        parse_points_stream(io.StringIO("0,0\nbad\n"))
