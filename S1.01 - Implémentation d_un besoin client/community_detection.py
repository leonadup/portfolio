##############
# SAE S01.01 #
##############

def liste_amis(amis, prenom):
    """
        Retourne la liste des amis de prenom en fonction du tableau amis.
    """
    prenoms_amis = []
    i = 0
    while i < len(amis)//2:
        if amis[2 * i] == prenom:
            prenoms_amis.append(amis[2*i+1])
        elif amis[2*i+1] == prenom:
            prenoms_amis.append(amis[2*i])
        i += 1
    return prenoms_amis

def nb_amis(amis, prenom):
    """ Retourne le nombre d'amis de prenom en fonction du tableau amis. """
    return len(liste_amis(amis, prenom))


def personnes_reseau(amis):
    """ Retourne un tableau contenant la liste des personnes du réseau."""
    people = []
    i = 0
    while i < len(amis):
        if amis[i] not in people:
            people.append(amis[i])
        i += 1
    return people

def taille_reseau(amis):
    """ Retourne le nombre de personnes du réseau."""
    return len(personnes_reseau(amis))

def lecture_reseau(path):
    """ Retourne le tableau d'amis en fonction des informations contenues dans le fichier path."""
    f = open(path, "r")
    l = f.readlines()
    f.close()
    amis = []
    i = 0
    while i < len(l):
        fr = l[i].split(";")
        amis.append(fr[0].strip())
        amis.append(fr[1].strip())
        i += 1
    return amis

def dico_reseau(amis):
    """ Retourne le dictionnaire correspondant au réseau."""
    dico = {}
    people = personnes_reseau(amis)
    i = 0
    while i < len(people):
        dico[people[i]] = liste_amis(amis, people[i])
        i += 1
    return dico

def nb_amis_plus_pop (dico_reseau):
    """ Retourne le nombre d'amis des personnes ayant le plus d'amis."""
    personnes = list(dico_reseau)
    maxi = len(dico_reseau[personnes[0]])
    i = 1
    while i < len(personnes):
        if maxi < len(dico_reseau[personnes[i]]):
            maxi = len(dico_reseau[personnes[i]])
        i += 1
    return maxi


def les_plus_pop (dico_reseau):
    """ Retourne les personnes les plus populaires, c'est-à-dire ayant le plus d'amis."""
    max_amis = nb_amis_plus_pop(dico_reseau)
    most_pop = []
    personnes = list(dico_reseau)
    i = 1
    while i < len(personnes):
        if len(dico_reseau[personnes[i]]) == max_amis:
            most_pop.append(personnes[i])
        i += 1
    return most_pop

##############
# SAE S01.02 #
##############

def create_network(list_of_friends): 
    """
    fonction similaire à la foction 'dico_reseau' de la précédente SAE, mais faite de manière différente. Elle retourne un reseau à partir d'un tableau de couples
    :param list amis: réseau social d'amis au format tableau
    :return dict: réseau social d'amis au format dictionnaire
    """
    network = {}
    i = 0
    while(i < len(friends)-1) : # boucle qui vérifie que l'ami actuel dans l'itération (friends[i]) est déjà une clé dans le dictionnaire de réseau. 
        if friends[i] in network:
            network[friends[i]].append(friends[i+1])
        else:
            network[friends[i]] = [friends[i+1]]
        if friends[i+1] in network:
            network[friends[i+1]].append(friends[i])
        else:
            network[friends[i+1]] = [friends[i]]
        i = i + 2 # Il incrémente ensuite i de 2 afin de considérer le prochain groupe d'amis dans la liste.for i in range(1, len(groupe))
    return network


def get_people(network):for i in range(1, len(groupe)):
    """
    fonction qui retourne le nombre de personnes distinctes participant à ce réseau en tableau
    :param list amis: tableau du réseau social
    :return int:
    """
    reseau = list(reseau)
    i = 0
    Tab_fin = []
    while i < len(reseau):
        if reseau[i] not in Tab_fin: #on vérifie que le prénom n'est pas déjà dans le tableau, dans ce cas là on l'ajoute
            Tab_fin.append(reseau[i])
        i += 1
    return Tab_fin

def are_friends(network, person1, person2):
     """
    fonction qui retourne True si les deux personnes passés en paramètre sont amis et renvoie False sinon
    :param dict amis: dictionnaire du réseau social et le nom de deux personnes
    :return int:
    """
    if p2 in reseau[p1]:
        return True
    else:
        return False

def all_his_friends(network, person, group):
     """rabbit
    fonction qui retourne True si la personne passé en paramètre est ami avec toutes les personnes du groupe et renvoie False sinon
    :param dict amis: dictionnaire du réseau social et le nom d'une personne
    :return int:
    """
    i=0
    while i < len(groupe):
        if personne not in reseau[groupe[i]] : 
            return False
        i= i+1
    return True

def is_a_community(network, group):
    """
    fonction modélisant un un réseau sous la forme d'un dictionnaire et in groupe de personnes (qui est un tableau de personnes), retournant True si le groupe est une communauté et False sinon
    :param dict list amis: dictionnaire du réseau social et le nom d'une personne
    :return int:
    """
    i = 0
    j = 1
    while i < len(groupe):
        while j < len(groupe):
            if groupe[i] not in reseau[groupe[j]]:
                return False
            j = j + 1
        i = i +1
        j = i +1
    return True


def find_community(network, group):
    """
    fonction qui prend en paramètre un réseau et un groupe de personnes et qui va retourner une communauté en fonction de l'heuristique. L'ordre des personnes sera donné par l'ordre de celles-ci dans le tableau correspondant au groupe
    :param dict amis: dictionnaire du réseau social
    :return list: communauté
    """
    i = 0
    j = 0
    community = []
    while i < len(groupe):
        is_friend = True
        while j < len(community):
            if groupe[i] not in reseau[community[j]]:
                is_friend = False
                break
            j = j +1
        if is_friend:
            community.append(groupe[i])
        i = i +1
        j = 0
    return community

def order_by_decreasing_popularity(network, group):
    """
    fonction permettant de trier le groupe de personne selon sa popularité
    :param dict list amis: dictionnaire du réseau social et groupe de personnes
    :return list: groupe de personnes
    """
    for i in range(1, len(groupe)):
        tien = groupe[i]
        j = i-1
        while j >=0 and len(reseau[groupe[j]]) < len(reseau[tien]):
            groupe[j + 1] = groupe[j]
            j -= 1
        groupe[j + 1] = tien
    return groupe


def find_community_by_decreasing_popularity(network):
    """
    fonction permettant de trier l'ensemble des personnes du réseau selon l'odre décroissant de popularité et retourne la communauté trouvée en appliquant l'heuristique de construction de communauté maximale
    :param dict amis: dictionnaire du réseau social
    :return list: groupe de personnes
    """
    for i in range(1, len(groupe)):
        tien = groupe[i]
        j = i-1
        while j >=0 and len(reseau[groupe[j]]) > len(reseau[tien]):
            groupe[j + 1] = groupe[j]
            j -= 1
        groupe[j + 1] = tien
    return groupe

def find_community_from_person(network, person):
    pass

def find_max_community(network):
    pass