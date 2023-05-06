import numpy as np
from scipy.constants import mu_0, pi
import matplotlib.pyplot as plt
from scipy import ndimage

from coordinate_and_position import CoordinateSystem
from fields import VectorField



test_array = np.array([
    [[2, 2, 2],
    [2, 2, 2],
    [2, 2, 2]],

    [[2, 2, 2],
    [2, 2, 2],
    [2, 2, 2]]
    ])

test_array = np.array([[[float(20), float(20), 0.0]], [[float(20), float(20), 0.0]]])

input_dimension = len(test_array.shape[:-1])  # Input dimension is 2
output_dimension = test_array.shape[-1]

print("Array:", test_array)
print("Shape:", test_array.shape[:-1])
print("i_d:", input_dimension)
print("o_d:", output_dimension)
print(

    VectorField(

    test_array

    )

    )