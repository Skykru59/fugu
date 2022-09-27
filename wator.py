from random import randint, choice
from time import sleep
import os

class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = 10
        self.hauteur = 8
        self.grille = [[ None for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        pass

    def peupler(self, nb_poisson, nb_requin):
        pass
    
    def jouer_un_tour(self):
        pass

class Poisson:
    def __init__(self, x, y):
        pass
    
    def deplacement_possible(self, monde):
        pass
    
    def se_deplacer(self, monde):
        pass
        
    def vivre_une_journee(self, monde):
        pass
