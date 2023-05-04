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
        Wire((20, 0), (20, 100), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((20, 100), (20, 120), tangential_eqs, polar_variables, HIGH_WIRE_RESISTANCE),
        Wire((20, 120), (20, 180), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((20, 180), (20, 0), tangential_eqs, polar_variables, BATTERY_VOLTAGE),
    ]
    ground_position = (20, 180)

    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.POLAR, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (20, 0), 1: (20, 100), 2: (20, 120), 3: (20, 180)}
    )
    world.compute()
    world.show_all()
