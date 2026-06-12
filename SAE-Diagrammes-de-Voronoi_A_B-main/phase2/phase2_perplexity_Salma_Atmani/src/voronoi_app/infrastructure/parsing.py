from __future__ import annotations
from typing import List, TextIO
from ..domain.geometry import Point

class PointParseError(Exception):
    """Raised when a point file contains invalid data."""

def parse_points_stream(stream: TextIO) -> List[Point]:
    """Parse lines 'x,y' into a list of unique finite points."""
    points: List[Point] = []
    seen = set()
    for line_no, raw in enumerate(stream, start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 2:
            raise PointParseError(f"Line {line_no}: expected 'x,y', got '{line}'.")
        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
        except ValueError as exc:
            raise PointParseError(f"Line {line_no}: invalid float values in '{line}'.") from exc

        if not (float("-inf") < x < float("inf")) or not (float("-inf") < y < float("inf")):
            raise PointParseError(f"Line {line_no}: non-finite coordinates in '{line}'.")

        key = (x, y)
        if key in seen:
            raise PointParseError(f"Line {line_no}: duplicate point '{line}'.")
        seen.add(key)
        points.append(Point(x, y))

    if len(points) < 2:
        raise PointParseError("Need at least two distinct points.")
    return points

def parse_points_file(path: str) -> List[Point]:
    """Parse a file path into points."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return parse_points_stream(f)
    except FileNotFoundError as exc:
        raise PointParseError(f"Input file '{path}' not found.") from exc
