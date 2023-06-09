import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World


if __name__ == "__main__":
    #on initialise l'espace, le voltage et les résistances
    WORLD_SHAPE = (101, 101)
    BATTERY_VOLTAGE = 1.0
    HIGH_WIRE_RESISTANCE = 1.0
    LOW_WIRE_RESISTANCE = 0.01


    #on paramétrise
    cartesian_variables = Symbol("x"), Symbol("y")
    x, y = cartesian_variables

    x_expression_vertical = 0 * x
    y_expression_vertical = y
    vertical_eqs = (x_expression_vertical, y_expression_vertical)

    x_expression_horizontal = x
    y_expression_horizontal = 0 * y
    horizontal_eqs = (x_expression_horizontal, y_expression_horizontal)

    #on construit le circuit
    wires = [
        Wire((26, 26), (26, 74), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((26, 74), (60, 74), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 74), (74, 74), horizontal_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE),
        Wire((74, 74), (74, 40), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((74, 40), (74, 26), vertical_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE),
        Wire((74, 26), (40, 26), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((40, 26), (26, 26), horizontal_eqs, cartesian_variables, BATTERY_VOLTAGE)
    ]
    
    #on met le ground_position juste avant la batterie
    ground_position = (40, 26)
    
    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.CARTESIAN, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (26, 26), 1: (26, 74), 2: (60, 74), 3: (74, 74), 4: (74, 40), 5: (74, 26), 6: (40, 26)}
    )
    world.compute()
    world.show_all()
