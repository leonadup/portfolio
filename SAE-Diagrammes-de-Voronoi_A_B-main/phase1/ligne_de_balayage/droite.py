import pygame
from config import screen
from point import Point
class Droite():
    def __init__(self, abscisse) -> None:
        self._x = abscisse

    @property
    def x(self) -> float:
        return self._x
    
    @x.setter
    def x(self, abscisse: float) -> None:
        self._x = abscisse

    def parabole(self, point: Point):
        return 
    
    def tracer(self)->None:
        for y in range(0, 500):
            pygame.draw.circle(screen, (0, 0, 0), (self.x, y), 1)