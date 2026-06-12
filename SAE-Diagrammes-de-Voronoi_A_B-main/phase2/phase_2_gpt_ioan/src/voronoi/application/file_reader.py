from typing import List
from voronoi.domain.point import Point


class FileFormatError(Exception):
    """Raised when input file format is invalid."""
    pass


class PointFileReader:
    """
    Reads a file containing points formatted as 'x,y' per line.
    """

    def read(self, filepath: str) -> List[Point]:
        points = []

        with open(filepath, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    x_str, y_str = line.split(",")
                    point = Point(float(x_str), float(y_str))
                    points.append(point)
                except ValueError:
                    raise FileFormatError(
                        f"Invalid format at line {line_number}: '{line}'"
                    )

        if len(points) < 2:
            raise ValueError("At least two points are required.")

        return points