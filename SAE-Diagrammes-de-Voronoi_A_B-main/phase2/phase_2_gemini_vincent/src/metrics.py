from abc import ABC, abstractmethod

class DistanceMetric(ABC):
    @abstractmethod
    def calculate_sq(self, x1, y1, x2, y2) -> float:
        pass

class EuclideanDistance(DistanceMetric):
    def calculate_sq(self, x1, y1, x2, y2) -> float:
        return (x1 - x2)**2 + (y1 - y2)**2