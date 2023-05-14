import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


from src.coordinate_and_position import CoordinateSystem
from src.fields import ScalarField


class LaplaceEquationSolver:
    """
    A Laplace equation solver used to compute the resultant potential field P in 2D-space generated by a constant
    voltage field V (for example due to wires).
    """

    def __init__(self, nb_iterations: int = 1000):
        """
        Laplace solver constructor. Used to define the number of iterations for the relaxation method.

        Parameters
        ----------
        nb_iterations : int
            Number of iterations performed to obtain the potential by the relaxation method (default = 1000).
        """
        self.nb_iterations = nb_iterations

    def _solve_in_cartesian_coordinate(
            self,
            constant_voltage: ScalarField,
            delta_x: float,
            delta_y: float
    ) -> ScalarField:
        """
        Solve the Laplace equation to compute the resultant potential field P in 2D-space.

        Parameters
        ----------
        constant_voltage : ScalarField
            A scalar field V : ℝ² → ℝ ; (x, y) → V(x, y), where V(x, y) is the electrical components' voltage at a
            given point (x, y) in space.
        delta_x : float
            Small discretization of the x-axis.
        delta_y : float
            Small discretization of the y-axis.

        Returns
        -------
        potential : ScalarField
            A scalar field P : ℝ² → ℝ ; (x, y) → P(x, y), where P(x, y) is the electric potential at a given point
            (x, y) in space. The difference between P and V is that P gives the potential in the whole world, i.e inside
            the electrical components and in the empty space between the electrical components, while the field V
            always gives V(x, y) = 0 if (x, y) is not a point belonging to an electrical component of the circuit.
        """

        circuit_list = []
        for y, line in enumerate(constant_voltage):
            for x, val in enumerate(line):
                if val != 0:
                    circuit_list.append((x, y, val))



        matrice_dep = constant_voltage


        for i in range(self.nb_iterations):
            V_ng = np.zeros((constant_voltage.shape[1] + 2, constant_voltage.shape[0] + 2))
            V_ng[0:-2, 1:-1]=matrice_dep
            V_nd = np.zeros((constant_voltage.shape[1] + 2, constant_voltage.shape[0] + 2))
            V_nd[2:, 1:-1]=matrice_dep
            V_nh = np.zeros((constant_voltage.shape[1] + 2, constant_voltage.shape[0] + 2))
            V_nh[1:-1, 0:-2]=matrice_dep
            V_nb = np.zeros((constant_voltage.shape[1] + 2, constant_voltage.shape[0] + 2))
            V_nb[1:-1, 2:]=matrice_dep
            matrice_dep=((1/delta_x**2+1/delta_y**2)**(-1) * 0.5 * ((V_nd+V_ng)/delta_x**2+(V_nb+V_nh)/delta_y**2))[1:-1, 1:-1]
            for k in circuit_list:
                matrice_dep[k[1], k[0]] = k[2]




        return ScalarField(matrice_dep)

    def _solve_in_polar_coordinate(
            self,
            constant_voltage: ScalarField,
            delta_r: float,
            delta_theta: float
    ) -> ScalarField:
        """
        Solve the Laplace equation to compute the resultant potential field P in 2D-space.

        Parameters
        ----------
        constant_voltage : ScalarField
            A scalar field V : ℝ² → ℝ ; (r, θ) → V(r, θ), where V(r, θ) is the electrical components' voltage at a
            given point (r, θ) in space.
        delta_r : float
            Small discretization of the r-axis.
        delta_theta : float
            Small discretization of the θ-axis.

        Returns
        -------
        potential : ScalarField
            A scalar field P : ℝ² → ℝ ; (r, θ) → P(r, θ), where P(r, θ) is the electric potential at a given point
            (r, θ) in space. The difference between P and V is that P gives the potential in the whole world, i.e inside
            the electrical components and in the empty space between the electrical components, while the field V
            always gives V(r, θ) = 0 if (r, θ) is not a point belonging to an electrical component of the circuit.
        """
        circuit_list = []
        for theta, line in enumerate(constant_voltage):
            for r, val in enumerate(line):
                if val != 0:
                    circuit_list.append((r, theta, val))
        print(circuit_list)



        matrice_dep = constant_voltage.copy()


        for i in range(self.nb_iterations):
            for theta, ligne in enumerate(matrice_dep):
                for r, val in enumerate(ligne):
                    if((r!=0 and r!=constant_voltage.shape[1]-1) and theta!=constant_voltage.shape[0]-1):
                        #comme on a un np.array, on doit quand meme utiliser delta_theta=1 pour les indices
                        matrice_dep[theta][r] = 1/(2/delta_r**2+1/(r*delta_r)+2/(r*delta_theta)**2)*(
                            (matrice_dep[theta][int(r+delta_r)]+matrice_dep[theta][int(r-delta_r)])/delta_r**2+(matrice_dep[theta][int(r+delta_r)])/(delta_r*r)+(matrice_dep[theta+1][r]+matrice_dep[theta-1][r])/(delta_theta*r)**2
                        )

            for k in circuit_list:
                matrice_dep[k[1], k[0]] = k[2]

            return ScalarField(matrice_dep)


    def solve(
            self,
            constant_voltage: ScalarField,
            coordinate_system: CoordinateSystem,
            delta_q1: float,
            delta_q2: float
    ) -> ScalarField:
        """
        Solve the Laplace equation to compute the resultant potential field P in 2D-space.

        Parameters
        ----------
        constant_voltage : ScalarField
            A scalar field V : ℝ² → ℝ representing a constant voltage field.
        coordinate_system : CoordinateSystem
            Coordinate system.
        delta_q1 : float
            Small discretization of the first axis.
        delta_q2 : float
            Small discretization of the second axis.

        Returns
        -------
        potential : ScalarField
            A scalar field P : ℝ² → ℝ  representing the potential in the 2D world.
        """
        if coordinate_system == CoordinateSystem.CARTESIAN:
            return self._solve_in_cartesian_coordinate(constant_voltage, delta_q1, delta_q2)
        elif coordinate_system == CoordinateSystem.POLAR:
            return self._solve_in_polar_coordinate(constant_voltage, delta_q1, delta_q2)
        else:
            raise NotImplementedError("Only the cartesian and polar coordinates system are implemented.")
