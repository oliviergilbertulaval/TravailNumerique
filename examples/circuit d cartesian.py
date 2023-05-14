import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol, pi, sin, cos
from math import sqrt

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World

from circle_function import full_arch

if __name__ == "__main__":
    WORLD_SHAPE = (101, 101)
    
    #longueur de la batterie ainsi que son voltage adapté pour garder un voltage de 1 V total
    Battery_length = 1
    BATTERY_VOLTAGE = 1.0 / Battery_length
    
    #longueur de la haute résistance ainsi que sa resistance adapté pour garder 1 ohm
    High_resistance_length = 2
    HIGH_WIRE_RESISTANCE = 1.0/High_resistance_length
    
    #nombre de segments pour représenter les deux arcs de cercles
    precision = 10
    LOW_WIRE_RESISTANCE = 0.01/(2*precision + 2 - Battery_length - High_resistance_length)

    cartesian_variables = Symbol("x"), Symbol("y")
    x, y = cartesian_variables


    x_expression_diagonal = x
    y_expression_diagonal = y
    diagonal_eqs = (x_expression_diagonal, y_expression_diagonal)

    wires = []
    #on définit un dictionaire qui contient tous les points du circuit
    arch = full_arch(precision, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100), (5/13 * 70, 12/13 * 70), (12/13 * 70, 5/13 * 70))

    #top gauche à haute résistance
    for key in range(int((precision - High_resistance_length)/2)):
        # print('lr', key)
        # print((arch[key], arch[key +1]))
        wires.append(Wire(arch[key], arch[key+1],
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
    
    #haute resistance    
    for key in range(int((precision - High_resistance_length)/2), int((precision + High_resistance_length)/2)):
        # print('hr', key)
        # print((arch[key], arch[key +1]))
        wires.append(Wire(arch[key], arch[key+1],
                          diagonal_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE))
        
    #haute resistance à batterie
    for key in range(int((precision + High_resistance_length)/2), int(3/2*precision + 1 - Battery_length/2)):
        # print('lr', key)
        # print((arch[key], arch[key +1]))
        wires.append(Wire(arch[key], arch[key+1],
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))

    #batterie
    for key in range(int(3/2*precision + 1 - Battery_length/2), int(3/2*precision + 1 + Battery_length/2)):
        # print('B', key)
        # print((arch[key], arch[key +1]))
        wires.append(VoltageSource(arch[key], arch[key+1],
                          diagonal_eqs, cartesian_variables, BATTERY_VOLTAGE))

    #batterie à top gauche
    for key in range(int(3/2*precision + 1 + Battery_length/2), int(2*precision+2)):
        # print('lr', key)
        # print((arch[key], arch[key +1]))
        wires.append(Wire(arch[key], arch[key+1],
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
    
    #on définit la ground_position comme étant juste avant la batterie
    ground_position = (arch[int(3/2*precision + 1 - Battery_length/2)])
    
    
    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.CARTESIAN, shape=WORLD_SHAPE)
    world.show_circuit(
        arch
    )
    world.compute()
    world.show_all()
