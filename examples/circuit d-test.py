import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol, pi, sin, cos
from math import sqrt

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World

from circle_function import top_circle_function2, straight_lines, full_arch

if __name__ == "__main__":
    WORLD_SHAPE = (101, 101)
    precision = 10
    BATTERY_VOLTAGE = 1.0/precision
    HIGH_WIRE_RESISTANCE = 1.0/precision
    LOW_WIRE_RESISTANCE = 0.01/precision

    cartesian_variables = Symbol("x"), Symbol("y")
    x, y = cartesian_variables

    
    x_expression_diagonal = x
    y_expression_diagonal = y
    diagonal_eqs = (x_expression_diagonal, y_expression_diagonal)

    wires = []
    
    #Low resistance big radius
    for k in range(precision):
        wires.append(Wire(top_circle_function2(precision, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100))[k], top_circle_function2(precision, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100))[k+1], 
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
        # wires.append((top_circle_function2(precision, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100))[k], top_circle_function2(precision, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100))[k+1]))
    
    #Low resistance right line
    # for k in range(precision):
    #     wires.append(Wire(straight_lines(precision, (12/13 * 100, 5/13 * 100), (12/13 * 70, 5/13 * 70))[k], straight_lines(precision, (12/13 * 100, 5/13 * 100), (12/13 * 70, 5/13 * 70))[k+1], 
    #                       diagonal_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE))
    
    wires.append(Wire((12/13 * 100, 5/13 * 100), (12/13 * 70, 5/13 * 70),
                      diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
    #     wires.append(((12/13 * 100, 5/13 * 100), (12/13 * 70, 5/13 * 70)))
        
    #Low resistance small radius
    for k in range(precision):
        wires.append(Wire(top_circle_function2(precision, (12/13 * 70, 5/13 * 70), (5/13 * 70, 12/13 * 70))[k], top_circle_function2(precision, (12/13 * 70, 5/13 * 70), (5/13 * 70, 12/13 * 70))[k+1], 
                          diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
        # wires.append((top_circle_function2(precision, (12/13 * 70, 5/13 * 70), (5/13 * 70, 12/13 * 70))[k], top_circle_function2(precision, (12/13 * 70, 5/13 * 70), (5/13 * 70, 12/13 * 70))[k+1]))
    
    #Low resistance left line
    # for k in range(precision):
    #     wires.append(Wire(straight_lines(precision, (5/13 * 70, 12/13 * 70), (5/13 * 100, 12/13 * 100))[k], straight_lines(precision, (5/13 * 70, 12/13 * 70), (5/13 * 100, 12/13 * 100))[k+1], 
    #                       diagonal_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE))
    
    wires.append(Wire((5/13 * 70, 12/13 * 70), (5/13 * 100, 12/13 * 100), 
                      diagonal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE))
    #     wires.append(((5/13 * 70, 12/13 * 70), (5/13 * 100, 12/13 * 100)))
    
    # for k in wires:
    #     print(k)   
    
    ground_position = (5/13 * 70, 12/13 * 70)
    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.CARTESIAN, shape=WORLD_SHAPE)
    world.show_circuit(
        full_arch(precision, (5/13 * 100, 12/13 * 100), (12/13 * 100, 5/13 * 100), (5/13 * 70, 12/13 * 70), (12/13 * 70, 5/13 * 70))
    )
    world.compute()
    world.show_all()
