from sympy import Symbol, pi, sin, cos
from math import sqrt

# circuit c
# function qui itère sur x et qui calcule les valeur de y avec une racine carée
def top_circle_function(precision, tuple_dep, tuple_end):
    delta_x = (tuple_end[0] - tuple_dep[0]) / precision
    
    rayon_2 = sqrt((tuple_end[0] - 50) ** 2 + (tuple_end[1] - 50) ** 2)
    rayon_1 = sqrt((tuple_dep[0] - 50) ** 2 + (tuple_dep[1] - 50) ** 2)
    #on choisit la poisition du centre (50, 50) comme étant le centre du centre
    #ainsi on raise un erreur si les points départs et arrivés sont pas à la même distance
    if rayon_2 != rayon_1:
        raise ValueError("Deux rayons différents")
    posi_dict = {}
    #on crée un dict avec des indices et leurs points associés, ce qui va être utile pour world.show_circuit()
    for i in range(precision+1):
        posi_dict[i]= (tuple_dep[0]+delta_x*i, 50 + sqrt(rayon_1 ** 2 - (tuple_dep[0] + delta_x * i - 50) ** 2))
    
    return posi_dict

#on refait la même affaire mais avec un moins avant la racine pour exprimer le dessous
def bottom_circle_function(precision, tuple_dep, tuple_end):
    delta_x = (tuple_end[0] - tuple_dep[0]) / precision
    
    rayon_2 = sqrt((tuple_end[0] - 50) ** 2 + (tuple_end[1] - 50) ** 2)
    rayon_1 = sqrt((tuple_dep[0] - 50) ** 2 + (tuple_dep[1] - 50) ** 2)
    if rayon_2 != rayon_1:
        raise ValueError("Deux rayons différents")
    posi_dict = {}
    for i in range(precision+1):
        posi_dict[i]= (tuple_dep[0]+delta_x*i, 50 - sqrt(rayon_1 ** 2 - (tuple_dep[0] + delta_x * i - 50) ** 2))
            
    return posi_dict

#cette fonction est utilisé dans world.show_circuit(), elle ne fait qu'unire les deux fonctions précédentes en un dictionnaire
def full_circle_function(precision, tuple_dep):
    posi_dict = top_circle_function(precision, tuple_dep, (100 - tuple_dep[0], tuple_dep[1]))
    for i in range(precision+1):
        posi_dict[i+precision] = bottom_circle_function(precision, (100 - tuple_dep[0], tuple_dep[1]), tuple_dep)[i]
    return posi_dict


#circuit d
#même affaire que top_circle_function mais centré à (0,0)
def top_circle_function2(precision, tuple_dep, tuple_end):
    delta_x = (tuple_end[0] - tuple_dep[0]) / precision
    
    rayon_2 = sqrt(tuple_end[0] ** 2 + tuple_end[1] ** 2)
    rayon_1 = sqrt(tuple_dep[0] ** 2 + tuple_dep[1] ** 2)
    if rayon_2 != rayon_1:
        raise ValueError("Deux rayons différents")
    posi_dict = {}
    for i in range(precision+1):
        posi_dict[i]= (tuple_dep[0]+delta_x*i, sqrt(rayon_1 ** 2 - (tuple_dep[0] + delta_x * i) ** 2))
    
    return posi_dict

#utilise top_circle_function2 pour créer un arc de cercle avec n'importe quel 4 points (les coins)
def full_arch(precision, tuple_t1, tuple_t2, tuple_b1, tuple_b2):
    posi_dict = top_circle_function2(precision, tuple_t1, tuple_t2)
    posi_dict[precision+1] = tuple_b2
    for i in range(precision+1):
        posi_dict[1+i+precision] = top_circle_function2(precision, tuple_b2, tuple_b1)[i]
    posi_dict[precision * 2 + 2] = tuple_t1
    return posi_dict

