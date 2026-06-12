import matplotlib.pyplot as plt
import numpy as np
from point import Point


def txt_reader_et_generateur_point(chemin:str="germes.txt"):

    with open(chemin, 'r') as f:
        lignes = f.readlines()

    liste_de_germes = []
    x,y = 0,0
    for ligne in lignes:
        parties = ligne.split(",")
        x = float(parties[0])
        y = float(parties[1])
        point = Point(x,y)
        liste_de_germes.append(point)
    return liste_de_germes

def dictionnaire_germes(germes:list[Point], pixel:Point):
    dico_distances = {}
    for germe in germes:
        dico_distances[germe]=germe.distance_to(pixel)
    return dico_distances

def distance_minimale(dico_distances:dict[Point,float]):
    for germe, distance in dico_distances.items():
        if distance == min(dico_distances.values()):
            return germe

def germe_le_plus_proche(germes:list[Point], pixel:Point):
    dictionnaire_distances = dictionnaire_germes(germes, pixel)
    return distance_minimale(dictionnaire_distances)


def afficher_germe(germes:list[Point]):
    for germe in germes:
        plt.scatter(germe.x, germe.y, color='red', marker='o')

def coloriage(height, width, espacement, germes):

    voronoi_diagram = np.zeros((height,width))

    dico_couleur = {}
    c=0
    for germe in germes :
        dico_couleur[germe]=c
        c+=1

    for i in range(0,width,espacement):
        for j in range(0,height,espacement):
            voronoi_diagram[j][i] = dico_couleur[germe_le_plus_proche(germes, pixel = Point(i, j))]
        
    plt.imshow(voronoi_diagram,origin='lower')

if __name__ == "__main__":
    
    fig = plt.figure()

    germes_fichier = txt_reader_et_generateur_point()

    afficher_germe(germes_fichier)
    coloriage(100,100,1,germes_fichier)

    plt.savefig("matplotlib_voronoi.svg", bbox_inches='tight')
    plt.show()  # affiche le grillage
    plt.close()