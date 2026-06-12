import pytest
from src.parsers.file_parser import FileParser

def test_parse_valid_file(tmp_path):
    d = tmp_path / "test.txt"
    d.write_text("1,2\n3,4\n")
    points = FileParser.parse(str(d))
    assert len(points) == 2
    assert points[0].x == 1 and points[0].y == 2
    assert points[1].x == 3 and points[1].y == 4

def test_parse_invalid_file(tmp_path):
    d = tmp_path / "test.txt"
    d.write_text("1,2\n3,a\n")
    with pytest.raises(ValueError):
        FileParser.parse(str(d))
