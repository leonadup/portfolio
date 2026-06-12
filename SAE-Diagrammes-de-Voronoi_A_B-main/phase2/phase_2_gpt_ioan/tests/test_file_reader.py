import pytest
from voronoi.application.file_reader import PointFileReader, FileFormatError


def test_read_valid_file(tmp_path):
    file = tmp_path / "points.txt"
    file.write_text("1,2\n3,4\n")

    reader = PointFileReader()
    points = reader.read(str(file))

    assert len(points) == 2
    assert points[0].x == 1
    assert points[0].y == 2


def test_invalid_format(tmp_path):
    file = tmp_path / "invalid.txt"
    file.write_text("invalid_line\n")

    reader = PointFileReader()

    with pytest.raises(FileFormatError):
        reader.read(str(file))