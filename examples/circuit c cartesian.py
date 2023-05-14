import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol, pi, sin, cos
from math import sqrt

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World

from circle_function import top_circle_function, bottom_circle_function, full_circle_function

if __name__ == "__main__":
    WORLD_SHAPE = (101, 101)
    precision = 30
    BATTERY_VOLTAGE = 1.0/precision
    HIGH_WIRE_RESISTANCE = 1.0/precision
    LOW_WIRE_RESISTANCE = 0.01/precision

    cartesian_variables = Symbol("x"), Symbol("y")
    x, y = cartesian_variables

    
    x_expression_diagonal = x
    y_expression_diagonal = y
    diagonal_eqs = (x_expression_diagonal, y_expression_diagonal)

    wires = []
    
    #High resistance from (35, 70) to (65, 70)
    for k in range(precision):
        wires.append(Wire(top_circle_function(precision, (35, 70), (65, 70))[k], top_circle_function(precision, (35, 70), (65, 70))[k+1], 
                          diagonal_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE))
        
    #Low resistance wire from (65, 70) to (65, 30)
    for k in range(precision):
        wires.append(Wire(top_circle_function(precision, (65, 70), (75, 50))[k], top_circle_function(precision, (65, 70), (75, 50))[k+1], 
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
    for k in range(precision):
        wires.append(Wire(bottom_circle_function(precision, (75, 50), (65, 30))[k], bottom_circle_function(precision, (75, 50), (65, 30))[k+1], 
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))

    #Voltage from (65, 30) to (35, 30)
    for k in range(precision):
        wires.append(VoltageSource(bottom_circle_function(precision, (65, 30), (35, 30))[k], bottom_circle_function(precision, (65, 30), (35, 30))[k+1], 
                          diagonal_eqs, cartesian_variables, BATTERY_VOLTAGE))
        
    #Low resistance wire from (35, 30) to (35, 70)
    for k in range(precision):
        wires.append(Wire(bottom_circle_function(precision, (35, 30), (25, 50))[k], bottom_circle_function(precision, (35, 30), (25, 50))[k+1], 
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
    for k in range(precision):
        wires.append(Wire(top_circle_function(precision, (25, 50), (35, 70))[k], top_circle_function(precision, (25, 50), (35, 70))[k+1], 
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))

    ground_position = (65, 30)
    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.CARTESIAN, shape=WORLD_SHAPE)
    world.show_circuit(
        full_circle_function(3*precision, (25, 50))
    )
    world.compute()
    world.show_all()
