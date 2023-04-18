from enum import Enum
from typing import Tuple, Union
from typing_extensions import TypeAlias


Position: TypeAlias = Tuple[Union[int, float], Union[int, float]]


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2
