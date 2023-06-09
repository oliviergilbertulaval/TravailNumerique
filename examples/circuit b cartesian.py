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
        Wire((20, 20), (20, 45), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((20, 45), (20, 60), vertical_eqs, cartesian_variables, BATTERY_VOLTAGE),
        Wire((20, 60), (20, 80), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((20, 80), (40, 80), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),

        Wire((40, 80), (40, 60), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 60), (40, 45), vertical_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE),
        Wire((40, 45), (40, 20), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 20), (20, 20), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),

        Wire((40, 80), (60, 80), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 80), (60, 60), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 60), (60, 45), vertical_eqs, cartesian_variables, HIGH_WIRE_RESISTANCE),
        Wire((60, 45), (60, 20), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 20), (40, 20), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),

        Wire((60, 20), (80, 20), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((80, 20), (80, 45), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((80, 45), (80, 60), vertical_eqs, cartesian_variables, BATTERY_VOLTAGE),
        Wire((80, 60), (80, 80), vertical_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
        Wire((80, 80), (60, 80), horizontal_eqs, cartesian_variables, LOW_WIRE_RESISTANCE),
    ]
    #on met le ground_position juste avant la batterie
    ground_position = (20, 45)

    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.CARTESIAN, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (20, 20), 1: (20, 45), 2: (20, 60), 3: (20, 80), 4: (40, 80), 5: (40, 60), 6: (40, 45), 7: (40, 20), 8: (60, 80), 9: (60, 60),
        10: (60, 45), 11: (60, 20), 12:(80, 20), 13:(80, 45), 14:(80, 60), 15:(80, 80)}
    )
    world.compute()
    world.show_all()
