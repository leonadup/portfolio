"""
Tests unitaires pour le service FileReader.

Ces tests vérifient la lecture de fichiers de points
selon les principes du TDD.
"""

import pytest
import os
import tempfile
from src.services.file_reader import FileReader, FileReaderError, InvalidFileFormatError
from src.domain.point import Point


class TestFileReaderValidFiles:
    """Tests de lecture de fichiers valides."""
    
    def test_read_simple_file(self, tmp_path):
        """Test : Lire un fichier simple avec quelques points."""
        # Créer un fichier temporaire
        file_path = tmp_path / "points.txt"
        file_path.write_text("2,4\n5.3,4.5\n18,29\n")
        
        reader = FileReader()
        points = reader.read_points_from_file(str(file_path))
        
        assert len(points) == 3
        assert points[0] == Point(2, 4)
        assert points[1] == Point(5.3, 4.5)
        assert points[2] == Point(18, 29)
    
    def test_read_file_with_negative_coordinates(self, tmp_path):
        """Test : Lire un fichier avec des coordonnées négatives."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("-5.5,10.2\n3,-7\n")
        
        reader = FileReader()
        points = reader.read_points_from_file(str(file_path))
        
        assert len(points) == 2
        assert points[0] == Point(-5.5, 10.2)
        assert points[1] == Point(3, -7)
    
    def test_read_file_with_whitespace(self, tmp_path):
        """Test : Lire un fichier avec des espaces."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("  2 , 4  \n5.3,  4.5\n")
        
        reader = FileReader()
        points = reader.read_points_from_file(str(file_path))
        
        assert len(points) == 2
        assert points[0] == Point(2, 4)
    
    def test_read_file_with_empty_lines(self, tmp_path):
        """Test : Lire un fichier avec des lignes vides."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("2,4\n\n5,10\n\n\n18,29\n")
        
        reader = FileReader()
        points = reader.read_points_from_file(str(file_path))
        
        assert len(points) == 3
    
    def test_read_file_with_comments(self, tmp_path):
        """Test : Lire un fichier avec des commentaires."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("# Ceci est un commentaire\n2,4\n# Autre commentaire\n5,10\n")
        
        reader = FileReader()
        points = reader.read_points_from_file(str(file_path))
        
        assert len(points) == 2
    
    def test_read_csv_file(self, tmp_path):
        """Test : Lire un fichier CSV."""
        file_path = tmp_path / "points.csv"
        file_path.write_text("2,4\n5,10\n")
        
        reader = FileReader()
        points = reader.read_points_from_file(str(file_path))
        
        assert len(points) == 2


class TestFileReaderInvalidFiles:
    """Tests de lecture de fichiers invalides."""
    
    def test_read_nonexistent_file_raises_error(self):
        """Test : Lire un fichier inexistant lève une erreur."""
        reader = FileReader()
        with pytest.raises(FileReaderError) as exc_info:
            reader.read_points_from_file("nonexistent.txt")
        
        assert "n'existe pas" in str(exc_info.value)
    
    def test_read_directory_raises_error(self, tmp_path):
        """Test : Lire un répertoire lève une erreur."""
        reader = FileReader()
        with pytest.raises(FileReaderError) as exc_info:
            reader.read_points_from_file(str(tmp_path))
        
        assert "n'est pas un fichier" in str(exc_info.value)
    
    def test_read_file_with_wrong_extension_raises_error(self, tmp_path):
        """Test : Lire un fichier avec mauvaise extension lève une erreur."""
        file_path = tmp_path / "points.pdf"
        file_path.write_text("2,4\n")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError) as exc_info:
            reader.read_points_from_file(str(file_path))
        
        assert "non supportée" in str(exc_info.value)
    
    def test_read_empty_file_raises_error(self, tmp_path):
        """Test : Lire un fichier vide lève une erreur."""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError) as exc_info:
            reader.read_points_from_file(str(file_path))
        
        assert "aucun point valide" in str(exc_info.value)
    
    def test_read_file_with_only_comments_raises_error(self, tmp_path):
        """Test : Lire un fichier avec seulement des commentaires lève une erreur."""
        file_path = tmp_path / "comments.txt"
        file_path.write_text("# Commentaire 1\n# Commentaire 2\n")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError):
            reader.read_points_from_file(str(file_path))


class TestFileReaderInvalidFormat:
    """Tests de format invalide dans les fichiers."""
    
    def test_read_file_with_invalid_format_raises_error(self, tmp_path):
        """Test : Format invalide lève une erreur."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("2,4\ninvalid line\n")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError) as exc_info:
            reader.read_points_from_file(str(file_path))
        
        assert "Ligne 2" in str(exc_info.value)
    
    def test_read_file_with_too_many_values_raises_error(self, tmp_path):
        """Test : Trop de valeurs par ligne lève une erreur."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("2,4,6\n")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError):
            reader.read_points_from_file(str(file_path))
    
    def test_read_file_with_too_few_values_raises_error(self, tmp_path):
        """Test : Pas assez de valeurs par ligne lève une erreur."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("2\n")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError):
            reader.read_points_from_file(str(file_path))
    
    def test_read_file_with_non_numeric_values_raises_error(self, tmp_path):
        """Test : Valeurs non numériques lèvent une erreur."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("abc,def\n")
        
        reader = FileReader()
        with pytest.raises(InvalidFileFormatError):
            reader.read_points_from_file(str(file_path))


class TestFileReaderValidation:
    """Tests de validation de fichiers."""
    
    def test_validate_valid_file(self, tmp_path):
        """Test : Valider un fichier valide."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("2,4\n5,10\n")
        
        reader = FileReader()
        assert reader.validate_file(str(file_path)) is True
    
    def test_validate_invalid_file(self, tmp_path):
        """Test : Valider un fichier invalide."""
        file_path = tmp_path / "invalid.txt"
        file_path.write_text("invalid data\n")
        
        reader = FileReader()
        assert reader.validate_file(str(file_path)) is False
    
    def test_count_points_in_file(self, tmp_path):
        """Test : Compter les points dans un fichier."""
        file_path = tmp_path / "points.txt"
        file_path.write_text("2,4\n\n5,10\n# comment\n18,29\n")
        
        reader = FileReader()
        count = reader.count_points_in_file(str(file_path))
        
        assert count == 3
    
    def test_count_points_nonexistent_file_raises_error(self):
        """Test : Compter les points d'un fichier inexistant lève une erreur."""
        reader = FileReader()
        with pytest.raises(FileReaderError):
            reader.count_points_in_file("nonexistent.txt")