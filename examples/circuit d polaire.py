import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World

from numpy import pi, sin, cos


if __name__ == "__main__":
    WORLD_SHAPE = (101, 91)
    BATTERY_VOLTAGE = 1.0
    HIGH_WIRE_RESISTANCE = 1.0
    LOW_WIRE_RESISTANCE = 0.01

    polar_variables = Symbol("r"), Symbol("theta")
    r, theta = polar_variables

    r_expression_tangential = 0 * r
    theta_expression_tangential = theta
    tangential_eqs = (r_expression_tangential, theta_expression_tangential)

    r_expression_radial = r
    theta_expression_radial = 0 * theta
    radial_eqs = (r_expression_radial, theta_expression_radial)

    wires = [
        Wire((40, 15), (40, 40), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((40, 40), (40, 50), tangential_eqs, polar_variables, BATTERY_VOLTAGE),
        Wire((40, 50), (40, 75), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 75), (60, 75), radial_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 75), (60, 50), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 50), (60, 40), tangential_eqs, polar_variables, HIGH_WIRE_RESISTANCE),
        Wire((60, 40), (60, 15), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 15), (40, 15), radial_eqs, polar_variables, LOW_WIRE_RESISTANCE),
    ]
    ground_position = (40, 40)

    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.POLAR, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (40, 15), 1: (40, 40), 2: (40, 50), 3: (40, 75), 4:(60, 75), 5:(60, 50), 6:(60, 40), 7:(60, 15), 8:(40,15)}
    )
    world.compute()
    world.show_all()
