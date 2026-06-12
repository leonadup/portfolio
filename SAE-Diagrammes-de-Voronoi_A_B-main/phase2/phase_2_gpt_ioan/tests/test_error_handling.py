import pytest
from voronoi.application.file_reader import PointFileReader


def test_not_enough_points(tmp_path):
    file = tmp_path / "one_point.txt"
    file.write_text("1,2\n")

    reader = PointFileReader()

    with pytest.raises(ValueError):
        reader.read(str(file))