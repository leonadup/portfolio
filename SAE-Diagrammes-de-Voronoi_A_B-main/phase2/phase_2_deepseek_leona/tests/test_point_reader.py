"""
Tests unitaires pour le module point_reader.
"""

import pytest
import tempfile
import os
from src.models.point import Point
from src.io.point_reader import PointReader


class TestPointReader:
    """Tests pour la classe PointReader."""
    
    def test_read_valid_file(self):
        """Test la lecture d'un fichier valide."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2,4\n")
            f.write("5.3,4.5\n")
            f.write("18,29\n")
            f.write("12.5,23.7\n")
            temp_file = f.name
        
        try:
            reader = PointReader(temp_file)
            points = reader.read_points()
            
            assert len(points) == 4
            assert points[0] == Point(2, 4)
            assert points[1] == Point(5.3, 4.5)
            assert points[2] == Point(18, 29)
            assert points[3] == Point(12.5, 23.7)
        
        finally:
            os.unlink(temp_file)
    
    def test_read_file_with_empty_lines(self):
        """Test la lecture d'un fichier avec des lignes vides."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2,4\n")
            f.write("\n")
            f.write("5.3,4.5\n")
            f.write("   \n")
            f.write("18,29\n")
            temp_file = f.name
        
        try:
            reader = PointReader(temp_file)
            points = reader.read_points()
            
            assert len(points) == 3
            assert points[0] == Point(2, 4)
            assert points[1] == Point(5.3, 4.5)
            assert points[2] == Point(18, 29)
        
        finally:
            os.unlink(temp_file)
    
    def test_read_file_with_spaces(self):
        """Test la lecture d'un fichier avec des espaces."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2, 4\n")
            f.write("5.3 , 4.5\n")
            f.write("  18  ,  29  \n")
            temp_file = f.name
        
        try:
            reader = PointReader(temp_file)
            points = reader.read_points()
            
            assert len(points) == 3
            assert points[0] == Point(2, 4)
            assert points[1] == Point(5.3, 4.5)
            assert points[2] == Point(18, 29)
        
        finally:
            os.unlink(temp_file)
    
    def test_file_not_found(self):
        """Test la gestion d'un fichier inexistant."""
        reader = PointReader("fichier_inexistant.txt")
        
        with pytest.raises(FileNotFoundError):
            reader.read_points()
    
    def test_invalid_format(self):
        """Test la gestion d'un format invalide."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("2,4,6\n")  # Trop de valeurs
            f.write("5.3\n")    # Pas assez de valeurs
            f.write("abc,def\n") # Non numérique
            temp_file = f.name
        
        try:
            reader = PointReader(temp_file)
            
            with pytest.raises(ValueError) as excinfo:
                reader.read_points()
            
            assert "Format invalide" in str(excinfo.value) or "non numériques" in str(excinfo.value)
        
        finally:
            os.unlink(temp_file)
    
    def test_empty_file(self):
        """Test la gestion d'un fichier vide."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            reader = PointReader(temp_file)
            
            with pytest.raises(ValueError) as excinfo:
                reader.read_points()
            
            assert "ne contient aucun point valide" in str(excinfo.value)
        
        finally:
            os.unlink(temp_file)
    
    def test_validate_file_extension(self):
        """Test la validation d'extension."""
        assert PointReader.validate_file_extension("points.txt") == True
        assert PointReader.validate_file_extension("points.TXT") == True
        assert PointReader.validate_file_extension("points.csv") == False
        assert PointReader.validate_file_extension("points") == False
        
        # Avec extensions personnalisées
        assert PointReader.validate_file_extension("points.csv", ['.csv', '.txt']) == True
        assert PointReader.validate_file_extension("points.dat", ['.dat']) == True
        assert PointReader.validate_file_extension("points.txt", ['.csv']) == False
    
    def test_reader_initialization(self):
        """Test l'initialisation du reader."""
        with pytest.raises(ValueError):
            PointReader("")
        
        with pytest.raises(ValueError):
            PointReader(None)
        
        reader = PointReader("test.txt")
        assert reader.file_path == "test.txt"