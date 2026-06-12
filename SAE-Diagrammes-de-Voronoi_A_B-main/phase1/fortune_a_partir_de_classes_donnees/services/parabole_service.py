from domain.point import Point
from math import sqrt
from typing import Optional

def get_x(f:Point, y:float, xd:float) -> float:
    '''
    f: foyer, à gauche de la directrice
    y: ordonnée désirée
    xd: position de la directrice
    pour cette parabole, connaissant le y désiré et la position de la plage calculer le x
    '''
    assert f.x <= xd
    if xd == f.x:
        return float("-inf")
    return (f.x**2 - xd**2 + (f.y - y)**2 ) / (f.x - xd) / 2

def intersection(f0:Point, f1:Point = None, xd : float = None) -> Point:
    '''
    considérons deux paraboles qui sont placés dans l'ordre y croissant,
    celle-ci et top_p (y supérieur)
    On cherche l'intersection entre les deux pour une directrice donnée
    '''
    assert f0.x <= xd
    if f1 is None:
        # l'intersection est donc rejetée à l'infini
        return Point(float("-inf"), float("inf"))
    assert f1.x <= xd

    if f0.x == f1.x:
        # intersection placée à la moitié
        y = (f0.y + f1.y) / 2
        if f0.x == xd:
            x = float("-inf")
        else:
            x = get_x(f0, y, xd)
    elif f1.x == xd:
        y = f1.y
        x = get_x(f0, y, xd)
    elif f0.x == xd:
        y = f0.y
        x = get_x(f1, y, xd)
    else:
        # il faut passer par une résolution d'équation du second degré
        # l'équation pour self est :
        # 2x(x0 - bx) = x0**2 - bx**2 + (y - y0)**2
        # l'équation pour next_arc est :
        # 2x(x1 - bx) = x1**2 - bx**2 + (y - y1)**2
        # on voit qu'il faut multiplier la première par (x1-bx) et la seconde par (x0-bx)
        # puis soustraire ce qui donne :
        # 0 = (x0**2 - bx**2 + (y - y0)**2) (x1-bx) - x1**2 - bx**2 + (y - y1)**2) (x0 - bx)
        # le coefficient en y**2 est donc a = (x1-bx) - (x0 - bx)
        # le coefficient en y est b = -2y0(x1-bx) + 2y1(x0-bx)
        # le coefficient sans y est c = (x0**2 - bx**2 + y0**2)(x1-bx) - (x1**2 - bx**2 + y1**2)(x0 - bx)
        dx0 = f0.x - xd
        dx1 = f1.x - xd
        a = f1.x - f0.x
        b = -2*(f0.y * dx1 - f1.y * dx0)
        c = (f0.x**2 - xd**2 + f0.y**2)*dx1 - (f1.x**2 - xd**2 + f1.y**2)*dx0
        delta = b**2 - 4*a*c
        # il y a deux racines. laquelle choisir ?
        # c'est un peu délicat : p0 -> p1 est sur la plage en y croissant
        # en passant le bon point d'intersection, la parabole de p1 doit passer devant
        # c'est à dire avec un x plus grand
        # donc si xp1(y) et xp2(y) sont les formules donnant x pour les deux paraboles
        # on doit avoir xp1 - xp0 croissant à la bonne racine
        # on écrit donc xp0(y) = (x0**2 - bx**2 + (y - y0)**2)/2(x0-bx)
        #               xp1(y) = (x1**2 - bx**2 + (y - y1)**2)/2(x1-bx)
        # on dérive xp1 - xp0 : f'(y) = (y - y1)/(x1-bx) - (y - y0)(x0-bx) > 0
        # en multipliant par les deux déno, on ne change pas le signe
        # (y-y1)(x0-bx) - (y-y0)(x1-bx) > 0
        # y (x0 - x1) - y1 (x0-bx) + y0(x1 - bx) > 0
        # pour y = (-b +- rdelta)/2(x1-x0)
        # on trouve exactement -+ rdelta > 0
        # donc il faut choisir la solution y = (-b - rdelta)/2(x1-x0)
        # on peut dire que c'est la valeur x1 - x0 qui décide automatiquement quelle racine prendre
        y = (-b-sqrt(delta)) / (2*a)
        x = get_x(f0, y, xd)
    return Point(x,y)