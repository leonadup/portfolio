import pygame
from config import screen
class Point():
    def __init__(self, abscisse : float, ordonnee : float):
        self._x : float = abscisse
        self._y : float = ordonnee

    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @x.setter
    def x(self, abscisse : float) -> None:
        self._x = abscisse
    
    @y.setter
    def y(self, ordonnee : float) -> None:
        self._y = ordonnee
    
    def tracer(self, couleur: tuple[int, int, int] = (0, 0, 0)) -> None:
        if self.y > 0 and self.y < screen.get_height():
            pygame.draw.circle(screen, couleur, (self.x, self.y), 1)