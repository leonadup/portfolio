# src/parsers/file_parser.py
from typing import List
from models.point import Point

class FileParser:
    @staticmethod
    def parse(file_path: str) -> List[Point]:
        points = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        print(f"Ligne lue: '{line}'")  # Debug
                        try:
                            x, y = map(float, line.split(','))
                            points.append(Point(x, y))
                            print(f"Point ajouté: ({x}, {y})")  # Debug
                        except ValueError as e:
                            print(f"Erreur de format: {e}")
            print(f"Nombre de points lus: {len(points)}")  # Debug
        except FileNotFoundError:
            print(f"Fichier non trouvé: {file_path}")
        return points
