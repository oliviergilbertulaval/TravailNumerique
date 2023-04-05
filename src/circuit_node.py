from src.coordinate_and_position import Position


class CircuitNode:
    """A node in a circuit. All nodes have a unique ID, a position and a potential."""

    def __init__(self, position: Position, uid: int, label: str = None) -> None:
        self._label = label if label else str(uid)
        self._uid = uid
        self._position = position
        self._potential = None

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def position(self) -> Position:
        return self._position

    @property
    def potential(self) -> float:
        return self._potential

    @potential.setter
    def potential(self, potential: float):
        self._potential = potential

    @property
    def uid(self) -> int:
        return self._uid
