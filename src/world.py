from typing import Tuple, Union

import numpy as np
from scipy.constants import mu_0, pi
import matplotlib.pyplot as plt
from scipy import ndimage

from src.biot_savart_equation_solver import BiotSavartEquationSolver
from src.circuit import Circuit
from src.coordinate_and_position import CoordinateSystem, Position
from src.fields import VectorField
from src.laplace_equation_solver import LaplaceEquationSolver


class World:
    """
    A 2D world. We place an electric circuit in the world and observe the resulting electromagnetic fields.
    """

    def __init__(
            self,
            circuit: Circuit,
            coordinate_system: Union[CoordinateSystem, int],
            shape: Tuple[int, int]
    ):
        """
        Solves the given circuit and builds the voltage scalar field (self._circuit_voltage) and the electric current
        vector field (self._circuit_current) with the same shape as the world.

        Parameters
        ----------
        circuit : Circuit
            Electrical circuit to place in the world.
        shape : Tuple[int, int]
            Two-dimensional tuple defining the size (x, y) of the world.

        Attributes
        ----------
        self._circuit_voltage : ScalarField
            A scalar field V : ℝ² → ℝ ; (x, y) → V(x, y), where V(x, y) is the electrical components' voltage at a
            given point (x, y) in space.
        self._circuit_current : VectorField
            A vector field I : ℝ² → ℝ³ ; (x, y) → (I_x(x, y), I_y(x, y), I_z(x, y)), where I_x(x, y), I_y(x, y) and
            I_z(x, y) are the 3 components of the electrical component current vector at a given point (x, y) in space.
            Note that I_z = 0 is always True in our 2D world.
        self._magnetic_field : VectorField
            A vector field B : ℝ² → ℝ³ ; (x, y) → (B_x(x, y), B_y(x, y), B_z(x, y)), where B_x(x, y), B_y(x, y) and
            B_z(x, y) are the 3 components of the magnetic vector at a given point (x, y) in space. Note that
            B_x = B_y = 0 is always True in our 2D world.
        self._potential : ScalarField
            A scalar field P : ℝ² → ℝ ; (x, y) → P(x, y), where P(x, y) is the electric potential at a given point
            (x, y) in space. The difference between P and V is that P gives the potential in the whole world, i.e inside
            the electrical components and in the empty space between the electrical components, while the field V
            always gives V(x, y) = 0 if (x, y) is not a point belonging to an electrical component of the circuit.
        self._electric_field : VectorField
            A vector field E : ℝ² → ℝ² ; (x, y) → (E_x(x, y), E_y(x, y)), where E_x(x, y) and E_y(x, y) are the 2
            components of the electric vector at a given point (x, y) in space. Note that the E_z component is missing
            because it is not possible to compute the gradient of the potential in the z axis in a 2D world.
        self._energy_flux : VectorField
            A vector field EF : ℝ² → ℝ³ ; (x, y) → (EF_x(x, y), EF_y(x, y), EF_z(x, y)), where EF_x(x, y), EF_y(x, y)
            and EF_z(x, y) are the 3 components of the energy flux vector at a given point (x, y) in space. Note that
            EF_z = 0 is always True in our 2D world.

        Notes
        -----
        In the previous text, we are using the coordinates x, y, z. Obviously, the fields' descriptions is also valid
        with polar coordinates using the correspondence x -> r, y -> θ, z -> z.
        """
        if not isinstance(shape, tuple):
            raise ValueError(f"The world's shape should be a tuple. Received a {type(shape)}.")
        if len(shape) != 2:
            raise ValueError(f"The length of the world's shape should be 2. The given shape has length {len(shape)}.")

        self._shape = shape
        self._circuit = circuit
        self._coordinate_system = CoordinateSystem(coordinate_system)

        voltage, current = self._circuit.get_voltage_and_current_fields(self._shape, self.minimum, self.maximum)
        self._circuit_voltage = voltage
        self._circuit_current = current

        self._electric_field = None
        self._energy_flux = None
        self._magnetic_field = None
        self._potential = None

    @property
    def minimum(self) -> Position:
        """
        Minimum position in the grid.

        Returns
        -------
        position : Position
            A tuple of two floats.
        """
        return 0, 0

    @property
    def maximum(self) -> Position:
        """
        Maximum position in the grid.

        Returns
        -------
        position : Position
            A tuple of two floats.
        """
        if self._coordinate_system == CoordinateSystem.CARTESIAN:
            return self._shape[0] - 1, self._shape[1] - 1
        elif self._coordinate_system == CoordinateSystem.POLAR:
            return self._shape[0] - 1, pi/2

    @property
    def delta_q1(self) -> float:
        """
        Discretization of the first axis.

        Returns
        -------
        discretization : float
            Small discretization.
        """
        return (self.maximum[0] - self.minimum[0])/(self._circuit_voltage.shape[0] - 1)

    @property
    def delta_q2(self) -> float:
        """
        Discretization of the second axis.

        Returns
        -------
        discretization : float
            Small discretization.
        """
        return (self.maximum[1] - self.minimum[1])/(self._circuit_voltage.shape[1] - 1)

    def compute(self, nb_relaxation_iterations: int = 1000):
        """
        Calculates all the fields in the world using the voltage and current fields produced by the electrical
        components in the circuit. The known fields are the voltage (self._circuit_voltage) and current
        (self._circuit_current) fields. The fields we need to compute are the potential (self._potential), the electric
        field (self._electric_field), the magnetic field (self._magnetic_field) and the energy flux (self._energy_flux).

        Parameters
        ----------
        nb_relaxation_iterations : int
            Number of iterations performed to obtain the potential by the relaxation method (default = 1000)
        """
        if (self._coordinate_system == CoordinateSystem.CARTESIAN):
            test = LaplaceEquationSolver(nb_relaxation_iterations)
            test2 = BiotSavartEquationSolver()




            self._potential = test._solve_in_cartesian_coordinate(self._circuit_voltage, self.delta_q1, self.delta_q2)

            self._electric_field= -self._potential.gradient()

            self._magnetic_field = test2._solve_in_cartesian_coordinate(self._circuit_current, self.delta_q1, self.delta_q2)

            self._energy_flux = self._electric_field.cross(self._magnetic_field)






        elif(self._coordinate_system == CoordinateSystem.POLAR):
            print("TEST")
            test = LaplaceEquationSolver(nb_relaxation_iterations)
            test2 = BiotSavartEquationSolver()
            self._potential = test._solve_in_polar_coordinate(self._circuit_voltage, self.delta_q1, self.delta_q2)
            
            self._electric_field= -self._potential.gradient()

            self._magnetic_field = test2._solve_in_polar_coordinate(self._circuit_current, self.delta_q1, self.delta_q2)

            #self._energy_flux = self._electric_field.cross(self._magnetic_field)



    def show_circuit(self, nodes_position_in_figure: dict = None):
        """
        Shows circuit.
        """
        self._circuit.display(nodes_position_in_figure)

    def show_circuit_voltage(self):
        """
        Shows circuit's voltage field.
        """
        self._circuit_voltage.show(title="Initial voltage")

    def show_circuit_current(self):
        """
        Shows circuit's current fields.
        """
        self._circuit_current.x.show(title="Initial current 'x'")
        self._circuit_current.y.show(title="Initial current 'y'")

    def show_potential(self):
        """
        Shows the electric potential.
        """
        self._potential.show(title="Potential")

    def show_electric_field(self, hide_components: bool = True):
        """
        Shows the electric field.

        Parameters
        ----------
        hide_components : bool
            Hide the electric field near the electrical components to produce a clearer stream plot.
        """
        if hide_components:
            electric_field = VectorField(self._electric_field)

            for x, y in zip(np.nonzero(self._circuit_voltage)[0], np.nonzero(self._circuit_voltage)[1]):
                electric_field[x, y] = np.array([np.nan, np.nan])
        else:
            electric_field = self._electric_field

        electric_field.show(title="Electric field")

    def show_magnetic_field(self):
        """
        Shows the z-component of the magnetic field.
        """
        self._magnetic_field.z.show(title="Magnetic field (z component)")

    def show_energy_flux(self):
        """
        Shows the energy flux.
        """
        self._energy_flux.show(title="Energy flux")

    def show_all(self):
        """
        Shows all fields.
        """
        self.show_circuit_voltage()
        self.show_potential()
        self.show_electric_field()
        self.show_magnetic_field()
        self.show_energy_flux()
