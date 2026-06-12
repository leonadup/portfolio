from .models import Point
import os

class FileHandler:
    @staticmethod
    def read_points_from_file(path: str) -> List[Point]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fichier {path} introuvable.")
        
        points = []
        with open(path, 'r') as f:
            for line in f:
                try:
                    parts = line.replace(',', ' ').split()
                    if len(parts) >= 2:
                        points.append(Point(float(parts[0]), float(parts[1])))
                except ValueError:
                    continue # Ignore les lignes malformées
        return points