"""
Module pour la lecture des fichiers de points.
"""

from typing import List, Optional
import os
from src.models.point import Point


class PointReader:
    """
    Responsable de la lecture des fichiers contenant les points.
    
    Cette classe suit le principe de responsabilité unique (SOLID) :
    elle ne s'occupe que de la lecture et de la validation des points.
    """
    
    def __init__(self, file_path: str):
        """
        Initialise le lecteur de points.
        
        Args:
            file_path: Chemin vers le fichier à lire
            
        Raises:
            ValueError: Si le chemin est invalide
        """
        if not file_path or not isinstance(file_path, str):
            raise ValueError("Le chemin du fichier doit être une chaîne non vide")
        
        self.file_path = file_path
    
    def read_points(self) -> List[Point]:
        """
        Lit le fichier et retourne la liste des points.
        
        Returns:
            List[Point]: Liste des points lus
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le format du fichier est invalide
            IOError: Si une erreur de lecture survient
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Le fichier {self.file_path} n'existe pas")
        
        points = []
        line_number = 0
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line_number += 1
                    line = line.strip()
                    
                    # Ignorer les lignes vides
                    if not line:
                        continue
                    
                    point = self._parse_line(line, line_number)
                    if point:
                        points.append(point)
            
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier : {str(e)}")
        
        if not points:
            raise ValueError("Le fichier ne contient aucun point valide")
        
        return points
    
    def _parse_line(self, line: str, line_number: int) -> Optional[Point]:
        """
        Analyse une ligne du fichier pour en extraire un point.
        
        Args:
            line: Ligne à analyser
            line_number: Numéro de ligne pour les messages d'erreur
            
        Returns:
            Optional[Point]: Le point créé ou None si la ligne est invalide
            
        Raises:
            ValueError: Si le format de la ligne est invalide
        """
        try:
            # Supprimer les espaces et diviser par la virgule
            parts = line.replace(' ', '').split(',')
            
            if len(parts) != 2:
                raise ValueError(f"Ligne {line_number}: Format invalide (attendu: x,y)")
            
            x = float(parts[0])
            y = float(parts[1])
            
            return Point(x, y)
            
        except ValueError as e:
            if "could not convert string to float" in str(e):
                raise ValueError(f"Ligne {line_number}: Coordonnées non numériques")
            raise
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str] = ['.txt']) -> bool:
        """
        Valide l'extension du fichier.
        
        Args:
            filename: Nom du fichier
            allowed_extensions: Liste des extensions autorisées
            
        Returns:
            bool: True si l'extension est valide
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in allowed_extensions