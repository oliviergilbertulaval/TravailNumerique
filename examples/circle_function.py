from sympy import Symbol, pi, sin, cos
from math import sqrt

def top_circle_function(precision, tuple_1, tuple_2):
    delta_x = (tuple_2[0] - tuple_1[0]) / precision
    delta_y = tuple_2[1] - tuple_1[1]
    rayon_2 = sqrt((tuple_2[0] - 50) ** 2 + (tuple_2[1] - 50) ** 2)
    rayon_1 = sqrt((tuple_1[0] - 50) ** 2 + (tuple_1[1] - 50) ** 2)
    if rayon_2 != rayon_1:
        raise ValueError("Deux rayons différents")
    posi_dict = {}
    posi_list = []
    for i in range(precision+1):
        posi_dict[i]= (tuple_1[0]+delta_x*i, 50 + sqrt(rayon_1 ** 2 - (tuple_1[0] + delta_x * i - 50) ** 2))
        posi_list.append((tuple_1[0]+delta_x*i, 50 + sqrt(rayon_1 ** 2 - (tuple_1[0] + delta_x * i - 50) ** 2)))
    
    return posi_dict

def bottom_circle_function(precision, tuple_1, tuple_2):
    delta_x = (tuple_2[0] - tuple_1[0]) / precision
    delta_y = tuple_2[1] - tuple_1[1]
    rayon_2 = sqrt((tuple_2[0] - 50) ** 2 + (tuple_2[1] - 50) ** 2)
    rayon_1 = sqrt((tuple_1[0] - 50) ** 2 + (tuple_1[1] - 50) ** 2)
    if rayon_2 != rayon_1:
        raise ValueError("Deux rayons différents")
    posi_dict = {}
    posi_list = []
    for i in range(precision+1):
        posi_dict[i]= (tuple_1[0]+delta_x*i, 50 - sqrt(rayon_1 ** 2 - (tuple_1[0] + delta_x * i - 50) ** 2))
        posi_list.append((tuple_1[0]+delta_x*i, 50 - sqrt(rayon_1 ** 2 - (tuple_1[0] + delta_x * i - 50) ** 2)))
    
    return posi_dict

def full_circle_function(precision, tuple_dep):
    posi_dict = top_circle_function(precision, tuple_dep, (100 - tuple_dep[0], tuple_dep[1]))
    for i in range(precision+1):
        posi_dict[i+precision] = bottom_circle_function(precision, (100 - tuple_dep[0], tuple_dep[1]), tuple_dep)[i]
    return posi_dict
#print(top_circle_function(8, (55, 90), (55, 10)))