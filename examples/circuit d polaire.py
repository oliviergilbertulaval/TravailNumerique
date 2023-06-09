import env_examples  # Modifies path, DO NOT REMOVE

from sympy import Symbol

from src import Circuit, CoordinateSystem, VoltageSource, Wire, World

from numpy import pi, sin, cos


if __name__ == "__main__":
    #on initialise l'espace, le voltage et les résistances   
    WORLD_SHAPE = (101, 101)
    BATTERY_VOLTAGE = 1.0
    HIGH_WIRE_RESISTANCE = 1.0
    LOW_WIRE_RESISTANCE = 0.01

    #on paramétrise avec des équations tangentielles et radiales
    polar_variables = Symbol("r"), Symbol("theta")
    r, theta = polar_variables

    r_expression_tangential = 0 * r
    theta_expression_tangential = theta
    tangential_eqs = (r_expression_tangential, theta_expression_tangential)

    r_expression_radial = r
    theta_expression_radial = 0 * theta
    radial_eqs = (r_expression_radial, theta_expression_radial)

    # on construit le circuit en oubliant pas de changer les angles de degré à rad
    wires = [
        Wire((40, 15*pi/(2* WORLD_SHAPE[1])), (40, 40*pi/(2* WORLD_SHAPE[1])), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        VoltageSource((40, 40*pi/(2* WORLD_SHAPE[1])), (40, 50*pi/(2* WORLD_SHAPE[1])), tangential_eqs, polar_variables, BATTERY_VOLTAGE),
        Wire((40, 50*pi/(2* WORLD_SHAPE[1])), (40, 75*pi/(2* WORLD_SHAPE[1])), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((40, 75*pi/(2* WORLD_SHAPE[1])), (60, 75*pi/(2* WORLD_SHAPE[1])), radial_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 75*pi/(2* WORLD_SHAPE[1])), (60, 50*pi/(2* WORLD_SHAPE[1])), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 50*pi/(2* WORLD_SHAPE[1])), (60, 40*pi/(2* WORLD_SHAPE[1])), tangential_eqs, polar_variables, HIGH_WIRE_RESISTANCE),
        Wire((60, 40*pi/(2* WORLD_SHAPE[1])), (60, 15*pi/(2* WORLD_SHAPE[1])), tangential_eqs, polar_variables, LOW_WIRE_RESISTANCE),
        Wire((60, 15*pi/(2* WORLD_SHAPE[1])), (40, 15*pi/(2* WORLD_SHAPE[1])), radial_eqs, polar_variables, LOW_WIRE_RESISTANCE),
    ]
    #on définit la ground_position comme étant juste avant la batterie
    ground_position = (40, 40*pi/(2* WORLD_SHAPE[1]))

    circuit = Circuit(wires, ground_position)
    world = World(circuit=circuit, coordinate_system=CoordinateSystem.POLAR, shape=WORLD_SHAPE)
    world.show_circuit(
        {0: (40, 15), 1: (40, 40), 2: (40, 50), 3: (40, 75), 4:(60, 75), 5:(60, 50), 6:(60, 40), 7:(60, 15), 8:(40,15)}
    )
    world.compute()
    world.show_all()
