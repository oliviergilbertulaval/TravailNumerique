import numpy as np
from scipy.constants import mu_0, pi
import matplotlib.pyplot as plt
from scipy import ndimage

from coordinate_and_position import CoordinateSystem
from fields import VectorField



# test_array = np.array([
#     [[2, 2, 2],
#     [2, 2, 2],
#     [2, 2, 2]],

#     [[2, 2, 2],
#     [2, 2, 2],
#     [2, 2, 2]]
#     ])

# test_array = np.array([[[float(20), float(20), 0.0]], [[float(20), float(20), 0.0]]])

# input_dimension = len(test_array.shape[:-1])  # Input dimension is 2
# output_dimension = test_array.shape[-1]

# print("Array:", test_array)
# print("Shape:", test_array.shape[:-1])
# print("i_d:", input_dimension)
# print("o_d:", output_dimension)
# print(

#     VectorField(

#     test_array

#     )

#     )


# Define a 2D NumPy matrix
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Divide the matrix by its x-value
x_value = matrix[0][0]  # The x-value is the first element in the first row
result = matrix / x_value

# Print the original matrix and the result
print("Original matrix:\n", matrix)
print("Result:\n", result)

def _solve_in_polar_coordinate(
        self,
        constant_voltage: ScalarField,
        delta_r: float,
        delta_theta: float
) -> ScalarField:
    """
    Solve the Laplace equation in polar coordinates to compute the resultant potential field P.

    Parameters
    ----------
    constant_voltage : ScalarField
        A scalar field V : ℝ² → ℝ ; (r, theta) → V(r, theta), where V(r, theta) is the electrical components' voltage at a
        given point (r, theta) in space.
    delta_r : float
        Small discretization of the radial distance.
    delta_theta : float
        Small discretization of the angular coordinate.

    Returns
    -------
    potential : ScalarField
        A scalar field P : ℝ² → ℝ ; (r, theta) → P(r, theta), where P(r, theta) is the electric potential at a given point
        (r, theta) in space. The difference between P and V is that P gives the potential in the whole world, i.e inside
        the electrical components and in the empty space between the electrical components, while the field V
        always gives V(r, theta) = 0 if (r, theta) is not a point belonging to an electrical component of the circuit.
    """

    circuit_list = []
    for i, r in enumerate(constant_voltage):
        for j, val in enumerate(r):
            if val != 0:
                circuit_list.append((i, j, val))

    matrice_dep = constant_voltage

    for _ in range(self.nb_iterations):
        P_nr = np.zeros_like(matrice_dep)
        P_nr[:-1, :] = matrice_dep[1:, :]
        P_nr[-1, :] = matrice_dep[0, :]

        P_nl = np.zeros_like(matrice_dep)
        P_nl[1:, :] = matrice_dep[:-1, :]
        P_nl[0, :] = matrice_dep[-1, :]

        P_nt = np.zeros_like(matrice_dep)
        P_nt[:, :-1] = matrice_dep[:, 1:]
        P_nt[:, -1] = matrice_dep[:, 0]

        P_nb = np.zeros_like(matrice_dep)
        P_nb[:, :-1] = matrice_dep[:, -1]

        laplacian = (
            (P_nr - 2 * matrice_dep + P_nl) / delta_r ** 2 +
            (1 / (i * delta_r) * (matrice_dep - P_nb) + (P_nt - matrice_dep) / (j * delta_theta * delta_r)) / delta_theta
        )
        matrice_dep += 0.25 * laplacian

        # Apply boundary conditions
        for k in circuit_list:
            matrice_dep[k[0], k[1]] = k[2]

    return ScalarField(matrice_dep)
