import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World

from numpy import pi, sin, cos


if __name__ == "__main__":
    WORLD_SHAPE = (101, 101)
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
        Wire((40, 20), (40, 40), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 40), (40, 60), tangential_eqs, polar_variables, HIGH_WIRE_RESISTANCE),
        Wire((40, 60), (40, 80), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 80), (20, 80), radial_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((20, 80), (20, 60), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((20, 60), (20, 40), tangential_eqs, polar_variables, BATTERY_VOLTAGE),
        Wire((20, 40), (20, 20), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((20, 20), (40, 20), radial_eqs, polar_variables, LOW_WIRE_RESISTANCE),
    ]
    ground_position = (20, 60)

    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.POLAR, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (40, 20), 1: (40, 40), 2: (40, 60), 3: (40, 80), 4:(20, 80), 5:(20, 60), 6:(20, 40), 7:(20, 20)}
    )
    world.compute()
    world.show_all()
