import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol, pi, sin, cos

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World


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
        Wire((40, 0), (40, 100), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 100), (40, 120), tangential_eqs, polar_variables, HIGH_WIRE_RESISTANCE),
        Wire((40, 120), (40, 180), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((40, 180), (40, 0), tangential_eqs, polar_variables, BATTERY_VOLTAGE),
    ]
    ground_position = (40, 180)

    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.POLAR, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (40, 0), 1: (40, 100), 2: (40, 120), 3: (40, 180)}
    )
    world.compute()
    world.show_all()
