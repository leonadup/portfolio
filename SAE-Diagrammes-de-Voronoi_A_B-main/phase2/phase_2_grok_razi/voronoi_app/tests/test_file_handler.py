
# tests/test_file_handler.py
import pytest
from pathlib import Path
from src.io.file_handler import FileHandler
from src.models.point import Point

@pytest.fixture
def temp_points_file(tmp_path: Path) -> Path:
    """Crée un fichier temporaire avec 4 points."""
    content = """2,4
5.3,4.5
18,29
12.5,23.7
"""
    file_path = tmp_path / "points.txt"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_read_points_nominal(temp_points_file: Path):
    points = FileHandler.read_points(temp_points_file)
    assert len(points) == 4
    assert points[0] == Point(2.0, 4.0)
    assert points[1] == Point(5.3, 4.5)
    assert points[2] == Point(18.0, 29.0)
    assert points[3] == Point(12.5, 23.7)


def test_read_points_with_empty_lines_and_comments(tmp_path: Path):
    content = """
# Tête de fichier commentée

2,4
   5.3 , 4.5   # point avec espaces et commentaire
18 ,  29      # autre commentaire

# ligne vide ci-dessous intentionnelle

12.5,23.7
"""
    file_path = tmp_path / "comments.txt"
    file_path.write_text(content, encoding="utf-8")

    points = FileHandler.read_points(file_path)
    
    assert len(points) == 4
    
    # On compare avec des floats
    assert points[0] == Point(2.0, 4.0)
    assert points[1] == Point(5.3, 4.5)
    assert points[2] == Point(18.0, 29.0)
    assert points[3] == Point(12.5, 23.7)
    
    # Ou bien (plus robuste) :
    expected = [
        Point(2.0, 4.0),
        Point(5.3, 4.5),
        Point(18.0, 29.0),
        Point(12.5, 23.7)
    ]
    assert points == expected


def test_read_points_file_not_found():
    with pytest.raises(FileNotFoundError):
        FileHandler.read_points("ce_fichier_nexiste_pas.txt")


def test_read_points_invalid_format(tmp_path: Path):
    content = """2,4
abc,def
18,29"""
    file_path = tmp_path / "invalid.txt"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        FileHandler.read_points(file_path)

    error_msg = str(exc_info.value)
    assert "ligne 2" in error_msg
    assert "parsing" in error_msg.lower()
    assert "abc,def" in error_msg
    assert "float" in error_msg.lower()   # ou "could not convert"


def test_read_points_too_few_points(tmp_path: Path):
    content = """1,2"""
    file_path = tmp_path / "one_point.txt"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="au moins 2 points"):
        FileHandler.read_points(file_path)