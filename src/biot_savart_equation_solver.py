import numpy as np
from scipy.constants import mu_0, pi
import matplotlib.pyplot as plt
from scipy import ndimage

from src.coordinate_and_position import CoordinateSystem
from src.fields import VectorField


class BiotSavartEquationSolver:
    """
    A Biot–Savart law solver used to compute the resultant magnetic field B in 2D-space generated by a constant current
    field I (for example due to wires).
    """

    def _solve_in_cartesian_coordinate(
            self,
            electric_current: VectorField,
            delta_x: float,
            delta_y: float
    ) -> VectorField:
        """
        Solve the Biot–Savart equation to compute the magnetic field given an electric current field.

        Parameters
        ----------
        electric_current : VectorField
            A vector field I : ℝ² → ℝ³ ; (x, y) → (I_x(x, y), I_y(x, y), I_z(x, y)), where I_x(x, y), I_y(x, y) and
            I_z(x, y) are the 3 components of the electric current vector at a given point (x, y) in space. Note that
            I_z = 0 is always True in our 2D world.
        delta_x : float
            Small discretization of the x-axis.
        delta_y : float
            Small discretization of the y-axis.

        Returns
        -------
        magnetic_field : VectorField
            A vector field B : ℝ² → ℝ³ ; (x, y) → (B_x(x, y), B_y(x, y), B_z(x, y)), where B_x(x, y), B_y(x, y) and
            B_z(x, y) are the 3 components of the magnetic vector at a given point (x, y) in space. Note that
            B_x = B_y = 0 is always True in our 2D world.
        """

        fig, ax = plt.subplots(1, 2, figsize=(15, 7))

        courant = ndimage.rotate(electric_current, 90)
        #potential = ndimage.rotate(matrice_dep, 90)


        ax[0].imshow(courant, cmap='jet', alpha=0.85)
        ax[0].invert_xaxis()
        #ax[1].imshow(potential, cmap='jet', alpha=0.85)
        ax[1].invert_xaxis()
        plt.show()




        raise NotImplementedError

    def _solve_in_polar_coordinate(
            self,
            electric_current: VectorField,
            delta_r: float,
            delta_theta: float
    ) -> VectorField:
        """
        Solve the Biot–Savart equation to compute the magnetic field given an electric current field.

        Parameters
        ----------
        electric_current : VectorField
            A vector field I : ℝ² → ℝ³ ; (r, θ) → (I_r(r, θ), I_θ(r, θ), I_z(r, θ)), where I_r(r, θ), I_θ(r, θ) and
            I_z(r, θ) are the 3 components of the electric current vector at a given point (r, θ) in space. Note that
            I_z = 0 is always True in our 2D world.
        delta_r : float
            Small discretization of the r-axis.
        delta_theta : float
            Small discretization of the θ-axis.

        Returns
        -------
        magnetic_field : VectorField
            A vector field B : ℝ² → ℝ³ ; (r, θ) → (B_r(r, θ), B_θ(r, θ), B_z(r, θ)), where B_r(r, θ), B_θ(r, θ) and
            B_z(r, θ) are the 3 components of the magnetic vector at a given point (r, θ) in space. Note that
            B_r = B_θ = 0 is always True in our 2D world.
        """
        raise NotImplementedError

    def solve(
            self,
            electric_current: VectorField,
            coordinate_system: CoordinateSystem,
            delta_q1: float,
            delta_q2: float
    ) -> VectorField:
        """
        Solve the Biot–Savart equation to compute the magnetic field given an electric current field.

        Parameters
        ----------
        electric_current : VectorField
            A vector field I : ℝ² → ℝ³ representing currents in the 2D world.
        coordinate_system : CoordinateSystem
            Coordinate system.
        delta_q1 : float
            Small discretization of the first axis.
        delta_q2 : float
            Small discretization of the second axis.

        Returns
        -------
        magnetic_field : VectorField
            A vector field B : ℝ² → ℝ³ representing the magnetic field in the 2D world.
        """
        if coordinate_system == CoordinateSystem.CARTESIAN:
            return self._solve_in_cartesian_coordinate(electric_current, delta_q1, delta_q2)
        elif coordinate_system == CoordinateSystem.POLAR:
            return self._solve_in_polar_coordinate(electric_current, delta_q1, delta_q2)
        else:
            raise NotImplementedError("Only the cartesian and polar coordinates solvers are implemented.")
