"""
:mod:`wator` module
:date: mai 2019
:auteur: Patrice THIBAUD

"""
import time
from random import randrange
#import pylab


H = 25   # nombre horizontal de cases de la grille
V = 25   # nombre vertical de cases de la grille
G_REQUIN = 5    # durée de gestation initiale des requins
E_REQUIN = 3    # énergie initiale des requins
G_THON = 2       # durée de gestation initiale des thons
P_THON = 0.30  # pourcentage des  cases initialement ocupées par des thons
P_REQUIN = 0.10  # pourcentage des cases initialement ocupées par des requins
PAS_AFFICHAGE = 200
# indique le nombre de pas entre chaque affichage de la grille-: durée d'un cycle
PAS_TOTAL = H*V*PAS_AFFICHAGE   # pas total pour la simulation

# ----------------------Choix relatifs aux  structures de données------------
#
#   une case de mer est définie par un tuple (0,0,0)
#   une case avec un thon : (1,gestation_restante,0)
#   une case avec un requin (2,gestation_restante,energie_restante)
#   accés au contenu d'une case de coordonnées (x,y) :  grille[y][x]
#
# --------------------------------------------------------------------------------


def creer_grille(case_h, case_v):
    """
    :param case_h: (int) représente le nombre horizontal de cases de la grille
    :param case_v: (int) représente le nombre vertical de cases de la grille
    :return: (list)  une liste (de longueur case_v-1) de  listes (de longueurs case_h-1)
     contenant uniquement des tuples (0, 0, 0)
    :CU: aucune
    :Exemples:

    >>> creer_grille(3, 2)
    [[(0, 0, 0), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0)]]

    """
    return [[(0, 0, 0) for _ in range(case_h)] for _ in range(case_v)]


def selection_case(case_h, case_v):
    """
    Choix aléatoire d'une case de la grille repérée par 2 coordonnées x et y
    L origine se trouve en haut à gauche de la grille,
    les axes sont orientés vers la droite et vers le bas
    :param case_h: (int) représente le nombre horizontal de cases de la grille
    :param case_v: (int) représente le nombre vertical de cases de la grille
    :return: (tuple) (x, y) avec x et y valant 0,1,2..,ou 9
    :CU: aucune
    """
    return (randrange(case_h), randrange(case_v))


def init_case(nature):
    """
    Renvoie un tuple initial pour un des 3 types de cases
    :param nature: (int) représente le type de case devant être générée
    (0 pour une mer, 1 pour un thon, 2 pour un requin)
    :return: (tuple)
    :CU: n doit valoir 0,1 ou 2
    :Exemples:
    >>> init_case(0)
    (0, 0, 0)
    >>> init_case(1)
    (1, 2, 0)
    >>> init_case(2)
    (2, 5, 3)
    """
    if nature == 0:
        tup = (nature, 0, 0)
    elif nature == 1:
        tup = (nature, G_THON, 0)
    elif nature == 2:
        tup = (nature, G_REQUIN, E_REQUIN)
    return tup

def placement_espece(grille, nature, n_poissons):
    """
    Permet de placer dans une grille un nombre donné de poissons identiques
    dans des cases de mers libres
    :param grille: (list) représente une grille du jeu
    :param nature: (int) représente le chiffre associé au poisson
    (1 pour un thon, 2 pour un requin)
    :param n_poissons: (int) représente le nombre de poissons à placer
    :return: (list) une grille du jeu avec les poissons placés
    :CU: n_poissons ne doit pas être plus grand que le nombre de mer encore disponibles
    """
    while n_poissons > 0:
        case = selection_case(len(grille[0]), len(grille))
        if grille[case[1]][case[0]][0] not in (1, 2):
            grille[case[1]][case[0]] = init_case(nature)
            n_poissons -= 1
    return grille


def denombre_espece(grille, espece):
    """
    Renvoie le nombre d'espéces d'un type présent dans la grille
    :param grille: (list) représente une grille du jeu
    :param espece: (int) représente le chiffre associé au poisson
    (1 pour un thon, 2 pour un requin)
    :return : (int) représente le nombre de poisson du type sélectionné
    présent dans la grille
    :CU: espece doit valoir 1 ou 2
    :Exemples:
    >>> grille = [[(1,2,0),(1,2,0),(0,0,0)],[(0,0,0),(2,5,3),(0,0,0)]]
    >>> denombre_espece(grille, 1)
    2
    >>> denombre_espece(grille, 2)
    1
    """
    nbre_espece = 0
    for ligne in grille:
        for case in ligne:
            if case[0] == espece:
                nbre_espece += 1
    return nbre_espece


def init_grille(p_thon, p_requin, case_h, case_v):
    """
    Crée une grille initiale pour démarrer le jeu
    :param p_thon: (float) pourcentage de cases occupées par les thons
    :param p_requin: (float) pourcentage de cases occupées par les requins
    :param case_h: (int) représente le nombre horizontal de cases de la grille
    :param case_v: (int) représente le nombre vertical de cases de la grille
    :return: (list) Une grille initiale du jeu avec les poissons placés
    dans les bonnes proportions
    :Exemples:
    >>> grille =  [[(1,2,0),(1,2,0),(0,0,0)],[(0,0,0),(2,5,3),(0,0,0)]]
    >>> denombre_espece(grille, 1)
    2
    """
    grille = creer_grille(case_h, case_v)
    n_thon = p_thon*case_h*case_v  # nombre de thons
    grille = placement_espece(grille, 1, n_thon)
    n_requin = p_requin*case_h*case_v  # nombre de requins
    grille = placement_espece(grille, 2, n_requin)
    return grille


def afficher_grille(grille):
    """
    :param grille: (list) représente la grille du jeu
    :return: (NoneType) None
    :CU:  Les cases de mer seront affichées avec un tiret bas (_),
    ,les cases requins avec un "R", celles avec un thon avec un "T"
    Le contenu des cases sera séparé par une espace.
    Chaque ligne de la grille sera affichée sur une ligne distincte.
    :Exemples:
    >>> grille = [[(0,0,0), (1,0,0), (0,0,0)], \
    [(2,0,0), (0,0,0), (0,0,0)], \
    [(2,0,0), (1,0,0), (1,0,0)]]
    >>> afficher_grille(grille)
    _  T  _
    R  _  _
    R  T  T
    >>> afficher_grille(creer_grille(3, 2))
     _  _  _
     _  _  _

    """
    affichage = ""
    for ligne in grille:
        for case in ligne:
            if case[0] == 0:
                affichage += "_"+" "
            elif case[0] == 1:
                affichage += "T"+" "
            elif case[0] == 2:
                affichage += "R"+" "
        affichage += "\n"
    print(affichage)


def afficher_grille2(grille, pas_simul, nb_thons, nb_requins):
    """
    Réalise un affichage de la grille avec les paramètres de la simulation
    :param grille: (list) représente la grille du jeu
    :pas_simul:(int) valeur du pas de simulation
    :nb_thons:(int) nombre de thons présents dans la grille
    :nb_requins:(int) nombre de requins présents dans la grille
    :return: (NoneType) None
    :CU:  Les cases de mer seront affichées avec un tiret bas (_)
    , les cases requins avec un "R", celles avec un thon avec un "T"
      Le contenu des cases sera séparé par une espace.
      Chaque ligne de la grille sera affichée sur une ligne distincte.
    :Exemples:
    >>> grille = [[(0, 0, 0), (1, 0, 0), (0, 0, 0)], \
    [(2, 0, 0), (0, 0, 0), (0, 0,0)], \
    [(2, 0, 0), (1, 0, 0), (1, 0, 0)]]
    >>> afficher_grille(grille)
    _  T  _
    R  _  _
    R  T  T
    >>> afficher_grille(creer_grille(3, 2))
     _  _  _
     _  _  _

    """
    affichage = f'pas de simulation : {pas_simul}/{PAS_TOTAL} \n \
Nombre de thons :{nb_thons} Nombre de requins: {nb_requins}  \n\n'
    for ligne in grille:
        for case in ligne:
            if case[0] == 0:
                affichage += "_"+" "
            elif case[0] == 1:
                affichage += "T"+" "
            elif case[0] == 2:
                affichage += "R"+" "
        affichage += "\n"
    print(affichage)


def cases_voisines(case, case_h, case_v):
    """
    Donne la liste des coordonnées des cases voisines dans la grille torique
    :param case: (tuple) coordonnées de la case étudiée sous la forme (x,y)
    :param case_h: (int) représente le nombre horizontal de cases de la grille
    :param case_v: (int) représente le nombre vertical de cases de la grille
    :return: (list) liste des coordonnées des cases voisines
    :CU: les coordonnées doivent être comprises entre 0 et 9
    :Exemples:
    >>> cases_voisines((1, 1), 2, 2)
    [(1, 0), (0, 1), (0, 1), (1, 0)]
    >>> cases_voisines((1, 1), 3, 3)
    [(1, 0), (0, 1), (2, 1), (1, 2)]
    >>> cases_voisines((2,0), 3, 3)
    [(2, -1), (1, 0), (0, 0), (2, 1)]
    """
    x = case[0]
    y = case[1]
    """
    # version plus abordable sans l'opérateur %
    if  y < v-1 and x < h-1:
        coordos_voisins = [(x, y-1), (x-1, y),(x+1, y), (x, y+1)]
    elif y == v-1 and x < h-1:
    coordos_voisins = [(x, y-1), (x-1, y), (x+1, y), (x, 0)]
    elif y < v-1 and x == h-1:
        coordos_voisins=[(x, y-1),(x-1, y),(0,y),(x,y+1)]
    elif y == v-1 and x == h-1:
    coordos_voisins = [(x, y-1), (x-1, y), (0, y), (x, 0)]
    """
    coordos_voisins = [(x, y-1), (x-1, y), ((x+1) % case_h, y), (x, (y+1) % case_v)]
    return coordos_voisins


def evol_gestation(case, grille):
    """
    Mise à jour de la durée de gestation
    :param case: (tuple) coordonnées de la case étudiée sous la forme (x,y)
    :param grille: (list) représente la grille du jeu
    :return: (int) La nouvelle durée de gestation
    :Exemples:

    >>> evol_gestation((0, 0), \
    [[(1, 2, 0), (1, 2, 0), (0, 0, 0)], [(0, 0, 0),(2, 5, 3), (0, 0, 0)]])
    1
    >>> evol_gestation((1, 1), \
    [[(1, 2, 0), (1, 2, 0), (0, 0, 0)], [(0, 0, 0),(2, 5, 3), (0, 0, 0)]])
    4
    """
    return grille[case[1]][case[0]][1]-1  # gestation diminue de 1


def evol_energie(case, grille):
    """
    Mise à jour de l'énergie
    :param case: (tuple) coordonnées de la case étudiée sous la forme (x,y)
    :param grille: (list) représente la grille du jeu
    :return: (int) La nouvelle énergie
    :Exemples:

    >>> evol_energie((1, 1), \
    [[(1, 2, 0), (1, 2, 0), (0, 0, 0)], [(0, 0, 0), (2, 5, 3), (0, 0, 0)]])
    2

    """
    return grille[case[1]][case[0]][2]-1  # energie diminue de 1


def deplace_vers_mer(nature, case, case_mer, grille, gestation, energie=0):
    """
    Retourne la grille après le déplacement d'une espèce vers une case de mer
    :param nature: (int) représente le chiffre associé au poisson
    (1 pour un thon, 2 pour un requin)
    :param case: (tuple) coordonnées de la case étudiée sous la forme (x, y)
    :param case_mer: (tuple) coordonnées de la case de mer vers laquelle
    le poisson se déplace
    :param grille: (list) représente la grille du jeu
    :param gestation: (int) durée de gestation de l'espèce ayant déjà été mise à jour
    :param energie: (int) energie de l'espèce ayant déjà été mise à jour
    ( 0 si non concerné)
    :return: (list) une grille du jeu mise à jour après le délacement du poisson
    :CU:  l'énergie et la gestation évolue avant le déplacement,
    les naissances sont gérées par la fonction
    :Exemples:
    >>> grille = [[(1, 2, 0), (1, 2, 0), (0, 0, 0)], [(0, 0, 0), (2, 5, 3), (0, 0, 0)]]
    >>> deplace_vers_mer(1, (0, 0), (0, 1),grille, 1)
    [[(0, 0, 0), (1, 2, 0), (0, 0, 0)], [(1, 1, 0), (2, 5, 3), (0, 0, 0)]]
    >>> grille2 = [[(0, 0, 0), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (2, 5, 3), (0, 0, 0)]]
    >>> deplace_vers_mer(2, (1, 1), (2, 1), grille2, 4, 2)
    [[(0, 0, 0), (0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (2, 4, 2)]]
    """
    if gestation == 0:  # si la durée de gestation devient nulle
        if nature == 1:
        # le thon se déplace et gestation remise à valeur initiale
            grille[case_mer[1]][case_mer[0]] = init_case(nature)
        elif nature == 2:
            grille[case_mer[1]][case_mer[0]] = (2, G_REQUIN, energie)
        grille[case[1]][case[0]] = init_case(nature)  # naissance d'un poisson sur la case quittée
    else:
        grille[case_mer[1]][case_mer[0]] = (nature, gestation, energie)
        # le poisson se déplaçant perd 1 de gestation
        grille[case[1]][case[0]] = init_case(0)  # case quitée devient une mer
    return grille


def tour_thon(case, liste, grille):
    """
    Traduit le comportement d'un thon lors de son tour
    :param case:(tuple) coordonnées de la case choisie contenant un thon de la forme (x, y)
    :param liste:(list) coordonnées des 4 cases voisines (liste de tuples)
    :param grille:(list) grille du jeu
    :return: (list) la grille mise à jour après le tour du thon
    """
    gestation = evol_gestation(case, grille)
    # recherche d'une mer libre dans les cases voisines
    case_mer = recherche_case(liste, grille, 0)
    if case_mer:
        grille = deplace_vers_mer(1, case, case_mer, grille, gestation)
    else:  # si pas de cases dispo
        if gestation == 0:  # si la durée de gestation devient nulle
            grille[case[1]][case[0]] = init_case(1)  # durée de gestation réinitialisée
        else:
            grille[case[1]][case[0]] = (1, gestation, 0)
    return grille


def recherche_case(liste, grille, nature):
    """
    Retourne un type de case cherchée parmis les cases voisines s'il en existe bien un
    :param liste:(list) coordonnées des 4 cases voisines (liste de tuples)
    :param grille:(list) grille du jeu
    :param nature:(int) type de case recherchée 0 mer, 1 :thon, 2 : requin
    :CU: la liste des coordonnées des cases voisines doit êtr fournie par la fonction
    :return:(tuple or bool) retourne False si aucune case du type recherché n'est trouvée
    :Exemples:
    >>> grille = [[(1,2,0),(0,0,0),(0,0,0)],[(0,0,0),(2,5,3),(0,0,0)]]
    >>> recherche_case([(2, -1), (1, 0), (0, 0), (2, 1)], grille, 2)
    False
    >>> recherche_case([(1, -1), (0, 0), (2, 0), (1, 1)], grille, 1)
    (0, 0)
    """
    liste_voisins = list(liste)
    n_voisins_test = 4
    while n_voisins_test > 0:
        choix = randrange(n_voisins_test)
        # choix d'un nombre entier dans l'intervalle [0,4[ correspondant à une des 4 cases voisines
        case_voisine_testee = liste_voisins[choix]  # case testée dans la liste
        # si la case voisine contient un thon
        if grille[case_voisine_testee[1]][case_voisine_testee[0]][0] == nature:
            return case_voisine_testee
        else:
            del liste_voisins[choix]
            n_voisins_test -= 1
    return False


def chasse_au_thon(case, case_thon, grille, gestation):
    """
    Renvoie une grille traduisant le comportement d'un requin s'il a trouvé un thon a proximité
    :param case: (tuple) coordonnées de la case sous la forme (x,y)
    :param case_thon: (tuple) coordonnées de la case occupée par un thon
    :param grille: (list) représente la grille du jeu
    :param gestation: (int) durée de gestation du requin ayant déjà été mise à jour
    :return:(list) grille mise à jour après la digestion du thon
    """
    if gestation == 0:  # si la gestation devient nulle
        grille[case[1]][case[0]] = init_case(2)  # un requin nait sur la case quitée
        grille[case_thon[1]][case_thon[0]] = init_case(2)
        # le requin mange le thon, son energie et sa gestation sont restaurées
    else:
        grille[case_thon[1]][case_thon[0]] = (2, gestation, E_REQUIN)
        # le requin mange le thon, son energie est restaurée
        grille[case[1]][case[0]] = init_case(0)  # case quitée devient une mer
    return grille




def tour_requin(case, liste, grille):
    """
     Traduit le comportement d'un requin lors de son tour
    :param case:(tuple) coordonnées de la case requin de la forme (x,y)
    :param liste:(list) coordonnées des 4 cases voisines (liste de tuples)
    :param grille:(list) grille du jeu
    :return: (list) la grille mise à jour après le tour du requin
    """
    gestation = evol_gestation(case, grille)  # durée de gestation du requin
    energie = evol_energie(case, grille)
    case_thon = recherche_case(liste, grille, 1)  # recherche d'un thon dans les cases voisines
    if case_thon:
        grille = chasse_au_thon(case, case_thon, grille, gestation)
    else:  # sinon recherche d'une mer libre dans les cases voisines
        case_mer = recherche_case(liste, grille, 0)
        if case_mer:  # si case de mer trouvée
            if energie == 0:  # si l'énergie est nulle
                grille[case_mer[1]][case_mer[0]] = init_case(0)  # le requin meurt
                grille[case[1]][case[0]] = init_case(0)  # case quitée devient une mer
            else:  # si energie requin n'est pas  nulle
                grille = deplace_vers_mer(2, case, case_mer, grille, gestation, energie)
        else:  # pas de déplacement
            if energie == 0:  # si energie nulle
                grille[case[1]][case[0]] = init_case(0)  # le requin ne se déplace pas et meurt
            else:
                if gestation == 0:  # si la gestation devient nulle
                    # la durée de gestation est réinitialisée
                    grille[case[1]][case[0]] = (2, G_REQUIN, energie)
                else:
                    grille[case[1]][case[0]] = (2, gestation, energie)
    return grille


def evol_population(grille):
    """
    Simule un tour complet de jeu
    :param grille:(list) grille du jeu
    :return: (list) la grille mise à jour après un tour
    """
    case_h = len(grille[0])  # nombre de cases horizontalement dans la grille
    case_v = len(grille)  # nombre de cases verticalement dans la grille
    case_choisie = selection_case(case_h, case_v)
    if grille[case_choisie[1]][case_choisie[0]][0] == 1:
        grille = tour_thon(case_choisie, cases_voisines(case_choisie, case_h, case_v), grille)
    elif grille[case_choisie[1]][case_choisie[0]][0] == 2:
        grille = tour_requin(case_choisie, cases_voisines(case_choisie, case_h, case_v), grille)
    return grille


def simulation(grille, p_affichage, n_pas_total):
    """
    Simule N-tours complets de jeu
    :param grille:(list) grille du jeu
    :param p_affichage:(int) pas aubout du quel un affichage de la grille est réalisé
    :param n_pas_total:(int) nombre de pas total pour la simulation
    :return: (NoneType)
    """
    liste_thons = [] # liste contenant le nombre de thons à chaque pas de la simulation
    liste_requins = []  # liste contenant le nombre de requins à chaque pas de la simulation
    for i in range(n_pas_total//p_affichage):
        for _ in range(p_affichage):
            evol_population(grille)
            nb_thons = denombre_espece(grille, 1)
            nb_requins = denombre_espece(grille, 2)
            liste_thons.append(nb_thons)
            liste_requins.append(nb_requins)
        afficher_grille2(grille, (i+1)*p_affichage, nb_thons, nb_requins)
        time.sleep(0.05)
    construct_courbe(liste_thons, liste_requins, n_pas_total)


def construct_courbe(liste_n_thons, liste_n_requins, n_pas_total):
    """
    Construction et affichage des courbes représentants l'évolution du nombre
    de chaque espèces en fonction du pas de simulation
    :param liste_n_thons:(list) liste contenant le nombre de thons
    à chaque pas de la simulation
    :param liste_n_requins:(list) liste contenant le nombre de requins
    à chaque pas de la simulation
    :param n_pas_total:(int) nombre de pas total pour la simulation
    :return: (NoneType)
    """
    data_x = [i for i in range(n_pas_total)]  # abscisses
    pylab.plot(data_x, liste_n_thons, label='Nombre de thons')
    pylab.plot(data_x, liste_n_requins, label='Nombre de requins')
    pylab.legend()
    pylab.title('Evolution des populations de thons et de requins')
    pylab.xlabel('pas de la simulation')
    pylab.ylabel('Population')
    pylab.grid()
    pylab.show()


def demarrage():
    """
    fonction d'initialisation
    """
    grille = init_grille(P_THON, P_REQUIN, H, V)  # création de la grille aléatoire
    simulation(grille, PAS_AFFICHAGE, PAS_TOTAL)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=False)
    demarrage()
