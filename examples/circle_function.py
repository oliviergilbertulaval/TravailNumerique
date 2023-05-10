from sympy import Symbol, pi, sin, cos
from math import sqrt

#circuit c
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
#print(full_circle_function(8, (0, 50)))


#circuit d
def top_circle_function2(precision, tuple_1, tuple_2):
    delta_x = (tuple_2[0] - tuple_1[0]) / precision
    rayon_2 = sqrt(tuple_2[0] ** 2 + tuple_2[1] ** 2)
    rayon_1 = sqrt(tuple_1[0] ** 2 + tuple_1[1] ** 2)
    if rayon_2 != rayon_1:
        raise ValueError("Deux rayons différents")
    posi_dict = {}
    posi_list = []
    for i in range(precision+1):
        posi_dict[i]= (tuple_1[0]+delta_x*i, sqrt(rayon_1 ** 2 - (tuple_1[0] + delta_x * i) ** 2))
        posi_list.append((tuple_1[0]+delta_x*i, sqrt(rayon_1 ** 2 - (tuple_1[0] + delta_x * i) ** 2)))
    
    return posi_dict

def straight_lines(precision, tuple_1, tuple_2):
    delta_x = (tuple_2[0] - tuple_1[0]) / precision
    delta_y = (tuple_2[1] - tuple_1[1]) / precision
    posi_dict = {}
    posi_list = []
    for i in range(precision+1):
        posi_dict[i] = (tuple_1[0] + delta_x * i, tuple_1[1] + delta_y * i)
    
    return posi_dict
      
#print(straight_lines(10, (10,0), (0, 10)))

def full_arch(precision, tuple_t1, tuple_t2, tuple_b1, tuple_b2):
    posi_dict = top_circle_function2(precision, tuple_t1, tuple_t2)
    # print(posi_dict)
    posi_dict[precision+1] = tuple_b2
    # print(posi_dict)
    for i in range(precision+1):
        posi_dict[1+i+precision] = top_circle_function2(precision, tuple_b2, tuple_b1)[i]
        # print(posi_dict)
    posi_dict[precision * 2 + 2] = tuple_t1
    return posi_dict


# print(top_circle_function2(4, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100)))
# print(top_circle_function2(4, (12/13 * 70, 5/13 * 70), (5/13 * 70, 12/13 * 70)))
# print("------------------------------------------")
# print(full_arch(4, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100), (5/13 * 70, 12/13 * 70), (12/13 * 70, 5/13 * 70)))
    