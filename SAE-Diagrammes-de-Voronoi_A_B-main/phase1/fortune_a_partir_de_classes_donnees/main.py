from matplotlib import animation

from services.json_loader import load_json, convert_to_points
from domain.point import Point
from domain.priorityqueue import PriorityQueue
from services.parabole_service import *
from domain.beach import Beach
import matplotlib.pyplot as plt


if __name__ == "__main__":
    data = load_json("data/liste_de_sites100.json")
    sites = convert_to_points(data)
    plot_cadre = (Point(min(p.x for p in sites) - 10.0, min(p.y for p in sites) - 10.0), Point(max(p.x for p in sites) + 10.0, max(p.y for p in sites) + 10.0))
    queue:PriorityQueue = PriorityQueue()
    for point in sites:
        queue.push(point)
    beach = Beach()
    cercle_traites = []
    while not queue.empty():
        event = queue.pop()
        if type(event) == Point:
            beach.insert_point(event)
            new_circles = beach.detecte_cercle_valable(event)
            if new_circles is not None:
                for circle in new_circles:
                    if circle not in queue._events:
                        queue.push(circle)
        else:
            cercle_traites.append(event)
            beach.refermer_segments(event)
            new_circles = beach.insert_cercle(event)
            if new_circles is not None:
                for circle in new_circles:
                    if circle not in cercle_traites and circle not in queue._events:
                        queue.push(circle)

    
    nuage = sites
    segs = beach._liste_segment_finis
    # en supposant que nuage est la liste de Point du diagramme
    xs_nuage = [pt.x for pt in nuage]
    ys_nuage = [pt.y for pt in nuage]
    plt.scatter(xs_nuage, ys_nuage)

    # en supposant que segs est la liste des segments
    def afficher_segment(i):
        s = segs[i]
        p1, p2 = s.points
        plt.plot([p1.x, p2.x], [p1.y, p2.y])

    # sans animation:
    def afficher_tout():
        for i in range(len(segs)):
            afficher_segment(i)

    # zoom sur la zone utile, en supposant que
    # left, right, top, bottom définissent le cadre
    plt.xlim(plot_cadre[0].x, plot_cadre[1].x)
    plt.ylim(plot_cadre[0].y, plot_cadre[1].y)
        
    # orthonormé :
    ax = plt.gca()
    ax.set_aspect(1)

    # animation:
    a_animer = True
    if a_animer:
        anim = animation.FuncAnimation(plt.gcf(), afficher_segment, interval = 1, repeat = False, frames = len(segs))
    else :
        afficher_tout()
    
    #affichage
    plt.show()