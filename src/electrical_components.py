import numpy as np

from src.circuit_node import CircuitNode
from src.coordinate_and_position import Position


class ElectricalComponent:
    """
    Base class for all electrical components. An electric component is defined as any object that can be used to
    create a circuit. This includes wires, voltage sources, and current sources. All electrical components have a
    label, a start position, and a stop position. They also require parametric equations to define the 2D function
    connecting the start to the stop. The parametric equations must be made with the scipy library. To do this, you
    must fist define the two variables to be used in the equations. Then, you can define the equations using these
    variables. It is important to note that the equation goes through the origin, given that the origin is associated
    to the start position. In other words, the given parametric equation is drawn from the start position to the stop
    position.
    """

    def __init__(
            self,
            start_position: Position,
            stop_position: Position,
            wire_parametric_equations,
            variables,
            label: str
    ):
        """
        Constructor for the ElectricalComponent class.

        Parameters
        ----------
        start_position : Position
            The start position of the component. This is a tuple of two floats.
        stop_position : Position
            The stop position of the component. This is a tuple of two floats.
        wire_parametric_equations
            The parametric equations that define the 2D function connecting the start to the stop.
        variables
            The variables used in the parametric equations.
        label : str
            The label of the component.
        """
        self._label = label
        self._start_position = start_position
        self._stop_position = stop_position
        self._variables = variables
        self._wire_parametric_equations = wire_parametric_equations

        self._validate_equations_pass_through_origin()
        self._validate_start_and_stop_connected()

        self._current = None
        self._potential = None
        self._start_node = None
        self._stop_node = None

    @property
    def current(self) -> float:
        return self._current

    @current.setter
    def current(self, current: float):
        self._current = current

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def start_node(self) -> CircuitNode:
        return self._start_node

    @start_node.setter
    def start_node(self, node):
        self._start_node = node

    @property
    def stop_node(self) -> CircuitNode:
        return self._stop_node

    @stop_node.setter
    def stop_node(self, node):
        self._stop_node = node

    @property
    def start_position(self) -> Position:
        return self._start_position

    @property
    def stop_position(self) -> Position:
        return self._stop_position

    @property
    def variables(self):
        return self._variables

    @property
    def wire_parametric_equations(self):
        return self._wire_parametric_equations

    def evaluate_parametric_equations(self, values: np.ndarray) -> np.ndarray:
        """Evaluates the parametric equations at the given values. The values are given as a numpy array."""
        subs = {
            self._variables[0]: values[0],
            self._variables[1]: values[1]
        }

        evaluated_point = np.asarray(
            [
                float(self._wire_parametric_equations[0].evalf(subs=subs)),
                float(self._wire_parametric_equations[1].evalf(subs=subs))
            ]
        )

        return evaluated_point

    def _validate_equations_pass_through_origin(self) -> None:
        """Validates that the parametric equations pass through the origin."""
        evaluated_point = self.evaluate_parametric_equations((0, 0))

        assert np.isclose(evaluated_point, (0, 0), atol=0.1).all(), (
            f"Function {self._wire_parametric_equations} does not pass through the origin (0, 0, 0)."
        )

    def _validate_start_and_stop_connected(self) -> None:
        """Validates that the start and stop positions are connected by the parametric equations."""
        initial_point = np.asarray(list(self.start_position))
        final_point = np.asarray(list(self.stop_position))
        movement_vector = final_point - initial_point

        evaluated_point = self.evaluate_parametric_equations(movement_vector)
        evaluate_final_point = initial_point + np.asarray(evaluated_point)

        assert np.isclose(evaluate_final_point, final_point, atol=0.1).all(), (
            f"Starting point {self._start_position} of wire not connected to the stopping point {self._stop_position} "
            f"by function {self._wire_parametric_equations}."
        )


class Wire(ElectricalComponent):
    """
    Class representing a wire in a circuit. This class inherits from the ElectricalComponent class, so its behaviour is
    similar to that of the ElectricalComponent class. The main difference is that the Wire class will have a
    resistance property, which is used to calculate the current flowing through the wire.
    """

    def __init__(
            self,
            start_position: Position,
            stop_position: Position,
            wire_parametric_equations,
            variables,
            resistance: float,
            label: str = None,
    ):
        super().__init__(
            start_position,
            stop_position,
            wire_parametric_equations,
            variables,
            label if label else f"R={resistance:.2f}$\Omega$"
        )
        self._resistance = resistance

    @property
    def resistance(self) -> float:
        return self._resistance


class VoltageSource(ElectricalComponent):
    """
    Class representing a voltage source in a circuit. This class inherits from the ElectricalComponent class, so its
    behaviour is similar to that of the ElectricalComponent class. The main difference is that the VoltageSource class
    will have a voltage property, which is used to calculate the potential difference between the start and stop nodes.
    """

    def __init__(
            self,
            start_position: Position,
            stop_position: Position,
            wire_parametric_equations,
            variables,
            voltage: float,
            label: str = None,
    ):
        super().__init__(
            start_position,
            stop_position,
            wire_parametric_equations,
            variables,
            label if label else f"$V_s$={voltage:.2f}V"
        )
        self._voltage = voltage

    @property
    def voltage(self) -> float:
        return self._voltage


class CurrentSource(ElectricalComponent):
    """
    Class representing a current source in a circuit. This class inherits from the ElectricalComponent class, so its
    behaviour is similar to that of the ElectricalComponent class. The main difference is that the CurrentSource class
    will have a fixed current that won't be calculate.
    """

    def __init__(
            self,
            start_position: Position,
            stop_position: Position,
            wire_parametric_equations,
            variables,
            current: float,
            label: str = None,
    ):
        super().__init__(
            start_position,
            stop_position,
            wire_parametric_equations,
            variables,
            label if label else f"$I_s$={current:.2f}I"
        )
        self._current = current

    @property
    def current(self) -> float:
        return self._current

    @current.setter
    def current(self, current: float):
        assert np.isclose(current, self._current), (
            f"Current source's current is constant. New current is {current} A, which is not the same as the source's "
            f"current, i.e. {self._current} A."
        )
        self._current = current
