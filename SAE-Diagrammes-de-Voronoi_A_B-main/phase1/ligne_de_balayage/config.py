import pygame
import math

def egalite_float(float_1: float, float_2: float, rel_tol=1e-9, abs_tol=1e-9) -> bool:
        return math.isclose(float_1, float_2, rel_tol=rel_tol, abs_tol=abs_tol)

pygame.init()
screen = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()