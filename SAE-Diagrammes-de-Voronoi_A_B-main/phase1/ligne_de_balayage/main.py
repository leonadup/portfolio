import pygame
from droite import Droite
from point import Point
from parabole import Parabole
from config import screen, clock
screen.fill((255, 255, 255))
from random import randint

droite = Droite(100)
droite.tracer()


foyer1 = Point(220, 250)

foyer2 = Point(220, 350)

parabole1 = Parabole(foyer1, droite)

parabole2 = Parabole(foyer2, droite)




foyer3 = Point(randint(100, 500), randint(100, 500))

foyer4 = Point(randint(100, 500), randint(100, 500))




parabole3 = Parabole(foyer3, droite)

parabole4 = Parabole(foyer4, droite)




intersection = []

def calc_inter(parabole1, parabole2) -> list[Point]:
    global intersection
    points_intersection = parabole1.intersection(parabole2)
    for point in points_intersection:
        intersection.append(point)
running = True
while running:
    dt = clock.tick(10)
    screen.fill((255, 255, 255))
    if droite.x <= screen.get_width():
        droite.x += 0.01 * dt

    droite.tracer()
    foyer1.tracer()
    foyer2.tracer()    
    foyer3.tracer()
    foyer4.tracer()

    if droite.x > foyer1.x :
        parabole1.tracer()
    if droite.x > foyer2.x :
        parabole2.tracer()
    if droite.x > foyer3.x :
        parabole3.tracer()
    if droite.x > foyer4.x :
        parabole4.tracer()

    if droite.x > foyer1.x and droite.x > foyer2.x:
        calc_inter(parabole1, parabole2)
    if droite.x > foyer1.x and droite.x > foyer3.x:
        calc_inter(parabole1, parabole3)
    if droite.x > foyer1.x and droite.x > foyer4.x:
        calc_inter(parabole1, parabole4)
    if droite.x > foyer2.x and droite.x > foyer3.x:
        calc_inter(parabole2, parabole3)
    if droite.x > foyer2.x and droite.x > foyer4.x:
        calc_inter(parabole2, parabole4)
    if droite.x > foyer3.x and droite.x > foyer4.x:
        calc_inter(parabole3, parabole4)

    for point in intersection:
        point.tracer((255,0,0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




            