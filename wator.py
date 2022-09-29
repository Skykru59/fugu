from cmd import IDENTCHARS
from random import Random, randint, choice, random
from time import sleep
import os
import math


nb_poisson = 5
nb_requin = 2
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
        coup_possibles= []
        if monde.grille[(self.y+1)%monde.hauteur][self.x] == " ":
            coup_possibles.append((self.y+1)%monde.hauteur),(self.x)

        if monde.grille[(self.y-1)%monde.hauteur][self.x] == " ":
            coup_possibles.append((self.y-1)%monde.hauteur),(self.x)


        if monde.grille[self.y][(self.x+1)%monde.largeur] == " ":
            coup_possibles.append((self.x+1)%monde.hauteur),(self.y)


        if monde.grille[self.y][(self.x-1)%monde.largeur] == " ":
            coup_possibles.append((self.x-1)%monde.hauteur),(self.y)


        return coup_possibles
       
    
    def se_deplacer(self, monde):
        coup_possibles = self.deplacement_possible(monde)
        if len(coup_possibles) != 0:
            coup_a_jouer = choice(coup_possibles)
            y_preced = self.y
            x_preced = self.x

            self.y = coup_a_jouer[0]
            self.x = coup_a_jouer[1]
                     
            y_coup = self.y 
            x_coup = self.x
            
            monde.grille[y_coup] [x_coup] = self

            if self.duree_gestation >= 5:
                monde.grille [y_preced][x_preced] = Poisson(x_preced)(y_preced)
            else:
                monde.grille [y_preced][x_preced] = " "
        
    def vivre_une_journee(self, monde):
        self.duree_gestation += 1
        self.se_deplacer(monde)

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
    
        return coup_possibles

    def se_deplacer(self, monde):
        coup_possibles = self.deplacement_possible(monde)
        if len(coup_possibles) != 0:
            coup_a_jouer = choice(coup_possibles)
            x_coup = coup_a_jouer[0]
            y_coup = coup_a_jouer[1]

            x_preced = self.x
            y_preced = self.y

            self.x = x_coup
            self.y = y_coup

            monde.grille[y_coup] [x_coup] = self

            if self.duree_gestation >= 5:
                monde.grille [y_preced][x_preced] = Requin(x_preced)(y_preced)
            else:
                monde.grille [y_preced][x_preced] = " "
        
    def vivre_une_journee(self, monde):
        pass

monde=Monde(10,8)

monde.peupler( 5,2)

Monde.afficher_monde(monde)
for ligne in monde.grille:
    for case in ligne:  
        if isinstance(case, Poisson):
            case.se_deplacer(monde)

Monde.afficher_monde(monde)

