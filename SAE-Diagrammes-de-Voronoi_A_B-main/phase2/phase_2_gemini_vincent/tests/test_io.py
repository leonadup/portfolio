import pytest
import os
from src.io_handler import FileHandler
from src.models import Point

def test_read_valid_file(tmp_path):
    """Vérifie la lecture correcte d'un fichier bien formaté."""
    d = tmp_path / "data"
    d.mkdir()
    f = d / "points.txt"
    f.write_text("10,20\n30 40\n15.5,25.5")
    
    points = FileHandler.read_points_from_file(str(f))
    
    assert len(points) == 3
    assert points[0].x == 10.0
    assert points[2].y == 25.5

def test_file_not_found():
    """Vérifie la levée d'exception si le fichier n'existe pas."""
    with pytest.raises(FileNotFoundError):
        FileHandler.read_points_from_file("unexisting_file.txt")

def test_invalid_format_skips_line(tmp_path, capsys):
    """Vérifie que les lignes malformées sont signalées sans arrêter le programme."""
    f = tmp_path / "corrupt.txt"
    f.write_text("10,20\nCeciEstUneErreur\n30,40")
    
    points = FileHandler.read_points_from_file(str(f))
    captured = capsys.readouterr()
    
    assert len(points) == 2
    assert "Erreur de parsing" in captured.out