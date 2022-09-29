from cmd import IDENTCHARS
from random import Random, randint, choice, random
from time import sleep
import os
import math


nb_poisson = 20
nb_requin = 20
duree_gestation=4 


class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = 10
        self.hauteur = 8
        self.grille = [[ " " for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        for ligne in self.grille:
            for case in ligne:
                if isinstance(case,Poisson):
                    print("P", end=" | ")
                elif isinstance(case,Requin):
                    print("R", end=" | ")   
                else:
                    print(" ", end=" | ")
            print("\n")

        
    def peupler(self, nb_poisson, nb_requin):
            for i in range(nb_poisson):
                x_rand = randint (0,self.largeur-1)
                y_rand = randint (0, self.hauteur-1)
                if self.grille[y_rand][x_rand] == " ":
                    self.grille[y_rand][x_rand] = Poisson(y_rand,x_rand)
                    
            for i in range(nb_requin):
                x_rand = randint (0,self.largeur-1)
                y_rand = randint (0, self.hauteur-1)
                if self.grille[y_rand][x_rand] == " ":
                    self.grille[y_rand][x_rand] = Requin(y_rand,x_rand)

        

    
    def jouer_un_tour(self):
        pass



class Poisson:
    def __init__(self, x, y ):
        self.id = id
        self.x, self.y = x, y
        self.energy = float('inf')
        self.duree_gestation = duree_gestation
        self.duree_gestation = 0
        self.dead = False
    
    def deplacement_possible(self, monde):
        coup_possibles= ()
        if monde.grille[(self.y+1)%self.hauteur][self.x] == " ":
            coup_possibles.append(self.x, (self.y+1)%monde.hauteur)

        if monde.grille[(self.y-1)%self.hauteur][self.x] == " ":
            coup_possibles.append(self.x, (self.y-1)%monde.hauteur)

        if monde.grille[self.y][(self.x+1)%self.largeur] == " ":
            coup_possibles.append(self.x+1, (self.y-1)%monde.largeur)

        if monde.grille[self.y][(self.x+1)%self.largeur] == " ":
            coup_possibles.append(self.x+1, (self.y-1)%monde.largeur)


        return coup_possibles
       
    
    def se_deplacer(self, monde):
        pass
        
    def vivre_une_journee(self, monde):
        pass

class Requin:
    def __init__(self, x, y ):
        self.id = id
        self.x, self.y = x, y
        self.energy = 6
        self.duree_gestation = duree_gestation
        self.duree_gestation = 0
        self.dead = False
    
    def deplacement_possible(self, monde):
        coup_possibles= ()
        if monde.grille[(self.y+1)%monde.hauteur][self.x] == " " or Poisson:
            coup_possibles.append(self.x, (self.y+1)%monde.hauteur)

        if monde.grille[(self.y-1)%monde.hauteur][self.x] == " " or Poisson:
            coup_possibles.append(self.x, (self.y-1)%monde.hauteur)

        if monde.grille[self.y][(self.x+1)%monde.largeur] == " " or Poisson:
            coup_possibles.append(self.x+1, (self.y-1)%monde.largeur)

        if monde.grille[self.y][(self.x+1)%monde.largeur] == " " or Poisson:
            coup_possibles.append(self.x+1, (self.y-1)%monde.largeur)
    
    def se_deplacer(self, monde):
        pass
        
    def vivre_une_journee(self, monde):
        pass


monde=Monde(10,8)



monde.peupler( 20,20)

Monde.afficher_monde(monde)
