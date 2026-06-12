"""
Module de lecture de fichiers de points.

Ce module fournit un service pour lire des fichiers contenant
des coordonnées de points.
"""

import os
from typing import List
from src.domain.point import Point


class FileReaderError(Exception):
    """Exception levée lors d'erreurs de lecture de fichier."""
    pass


class InvalidFileFormatError(FileReaderError):
    """Exception levée quand le format du fichier est invalide."""
    pass


class FileReader:
    """
    Service de lecture de fichiers de points.
    
    Ce service lit des fichiers texte contenant des coordonnées de points
    au format : x,y (une paire par ligne).
    
    Principles SOLID respectés :
    - Single Responsibility : Lecture de fichiers uniquement
    - Open/Closed : Extensible pour d'autres formats via héritage
    """
    
    def __init__(self) -> None:
        """Initialise le lecteur de fichiers."""
        self._supported_extensions = ['.txt', '.csv']
    
    def read_points_from_file(self, file_path: str) -> List[Point]:
        """
        Lit des points depuis un fichier.
        
        Format attendu : une paire de coordonnées par ligne (x,y).
        Les lignes vides et les commentaires (#) sont ignorés.
        
        Args:
            file_path: Chemin vers le fichier à lire.
            
        Returns:
            Liste des points lus depuis le fichier.
            
        Raises:
            FileReaderError: Si le fichier n'existe pas.
            InvalidFileFormatError: Si le format du fichier est invalide.
            ValueError: Si une ligne contient des données invalides.
        """
        # Vérifier l'existence du fichier
        if not os.path.exists(file_path):
            raise FileReaderError(f"Le fichier '{file_path}' n'existe pas")
        
        if not os.path.isfile(file_path):
            raise FileReaderError(f"'{file_path}' n'est pas un fichier")
        
        # Vérifier l'extension
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self._supported_extensions:
            raise InvalidFileFormatError(
                f"Extension '{ext}' non supportée. "
                f"Extensions supportées : {', '.join(self._supported_extensions)}"
            )
        
        points: List[Point] = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    # Ignorer les lignes vides et les commentaires
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parser la ligne
                    try:
                        point = self._parse_line(line, line_number)
                        points.append(point)
                    except (ValueError, TypeError) as e:
                        raise InvalidFileFormatError(
                            f"Ligne {line_number} : {str(e)}"
                        )
        
        except UnicodeDecodeError:
            raise InvalidFileFormatError(
                "Le fichier contient des caractères non-UTF-8"
            )
        except IOError as e:
            raise FileReaderError(f"Erreur lors de la lecture du fichier : {str(e)}")
        
        if not points:
            raise InvalidFileFormatError("Le fichier ne contient aucun point valide")
        
        return points
    
    def _parse_line(self, line: str, line_number: int) -> Point:
        """
        Parse une ligne pour extraire un point.
        
        Args:
            line: La ligne à parser.
            line_number: Le numéro de ligne (pour les messages d'erreur).
            
        Returns:
            Le point extrait.
            
        Raises:
            ValueError: Si le format est invalide.
        """
        # Séparer par la virgule
        parts = line.split(',')
        
        if len(parts) != 2:
            raise ValueError(
                f"Format invalide. Attendu : 'x,y', reçu : '{line}'"
            )
        
        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
        except ValueError:
            raise ValueError(
                f"Coordonnées invalides : '{line}'. "
                f"Les coordonnées doivent être des nombres."
            )
        
        # Créer le point (la validation est faite dans le constructeur)
        try:
            return Point(x, y)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Point invalide : {str(e)}")
    
    def validate_file(self, file_path: str) -> bool:
        """
        Valide un fichier sans charger tous les points.
        
        Args:
            file_path: Chemin vers le fichier à valider.
            
        Returns:
            True si le fichier est valide, False sinon.
        """
        try:
            self.read_points_from_file(file_path)
            return True
        except (FileReaderError, InvalidFileFormatError):
            return False
    
    def count_points_in_file(self, file_path: str) -> int:
        """
        Compte le nombre de points dans un fichier sans tous les charger.
        
        Args:
            file_path: Chemin vers le fichier.
            
        Returns:
            Le nombre de points dans le fichier.
            
        Raises:
            FileReaderError: Si le fichier n'existe pas.
        """
        if not os.path.exists(file_path):
            raise FileReaderError(f"Le fichier '{file_path}' n'existe pas")
        
        count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        count += 1
        except IOError as e:
            raise FileReaderError(f"Erreur lors de la lecture : {str(e)}")
        
        return count