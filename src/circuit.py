from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from src.circuit_node import CircuitNode
from src.coordinate_and_position import Position
from src.electrical_components import CurrentSource, ElectricalComponent, VoltageSource, Wire
from src.fields import ScalarField, VectorField


class Circuit:
    """
    A circuit is a collection of electrical components that are connected together with nodes. A circuit must closed.
    This means that all nodes must have at least two connections. A circuit can have current sources and voltage
    sources. A circuit can be solved to find the potential at each node and the current flowing through each component
    with kirchoff's laws.
    """

    COMPONENT_KEY = "component"
    NODE_KEY = "node"

    def __init__(
            self,
            components: List[ElectricalComponent],
            ground_position: Position,
            increment_size: float = 0.01
    ):
        self._components = components
        self._graph = nx.DiGraph()
        self._ground_position = ground_position
        self._increment_size = increment_size

        self._build_graph()
        self._validate_closed_circuit()

    @property
    def components(self) -> List[ElectricalComponent]:
        return self._components

    @property
    def edges(self):
        return self.graph.edges

    @property
    def graph(self):
        return self._graph

    @property
    def has_current_sources(self):
        return len(self._get_current_sources()) != 0

    @property
    def has_voltage_sources(self):
        return len(self._get_voltage_sources()) != 0

    @property
    def is_closed(self):
        return all([self._graph.degree(n) > 1 for n in self._graph.nodes])

    @property
    def nodes(self):
        return self.graph.nodes

    @property
    def sorted_edges(self):
        edges = list(self.graph.edges)
        edges.sort()
        return edges

    def _build_position_to_node_mapping(self):
        """
        Build a mapping from a position to a node. This is used to find the node at a given position.
        """
        position_to_node_mapping = {}
        node_uid = 0
        for component in self.components:
            start_position, stop_position = component.start_position, component.stop_position
            if start_position not in list(position_to_node_mapping.keys()):
                position_to_node_mapping[start_position] = CircuitNode(start_position, node_uid)
                node_uid += 1
            if stop_position not in list(position_to_node_mapping.keys()):
                position_to_node_mapping[stop_position] = CircuitNode(stop_position, node_uid)
                node_uid += 1

        self._position_to_node_mapping = position_to_node_mapping

    def _build_graph(self):
        """
        Build a graph from the components. Each component is an edge in the graph. The start and stop nodes of the
        """
        self._build_position_to_node_mapping()
        for component in self.components:
            component.start_node = self._position_to_node_mapping[component.start_position]
            component.stop_node = self._position_to_node_mapping[component.stop_position]
            self.graph.add_edge(
                u_of_edge=component.start_node.uid,
                v_of_edge=component.stop_node.uid,
                component=component
            )
            self.nodes[component.start_node.uid][self.NODE_KEY] = component.start_node
            self.nodes[component.stop_node.uid][self.NODE_KEY] = component.stop_node

    def _get_graph_without_current_sources(self):
        """
        Return a copy of the graph without the current sources.
        """
        graph_without_current_sources = self.graph.copy()

        for edge in self.graph.edges:
            component = self.graph.get_edge_data(*edge)[self.COMPONENT_KEY]

            if isinstance(component, CurrentSource):
                graph_without_current_sources.remove_edge(*edge)

        return graph_without_current_sources

    def _get_kirchoff_loops(self):
        """
        Return a list of loops in the graph. A loop is a list of edges that form a closed loop.
        """
        graph_without_current_sources = self._get_graph_without_current_sources()
        undirected_graph = graph_without_current_sources.to_undirected()
        return nx.cycle_basis(undirected_graph)

    def _get_edge_index(self, edge):
        """
        Return the index of the edge in the sorted list of edges.
        """
        indices = []
        for i, e in enumerate(self.sorted_edges):
            if (e[0] == edge[0] and e[1] == edge[1]) or (e[0] == edge[1] and e[1] == edge[0]):
                indices.append(i)

        if len(indices) == 1:
            return indices[0]

        return indices

    def _get_current_sources(self):
        """
        Return a list of the current sources in the graph.
        """
        edges = list(self.edges(data=self.COMPONENT_KEY))
        edges.sort()

        return [edge for edge in edges if isinstance(edge[2], CurrentSource)]

    def _get_voltage_sources(self):
        """
        Return a list of the voltage sources in the graph.
        """
        edges = list(self.edges(data=self.COMPONENT_KEY))
        edges.sort()

        return [edge for edge in edges if isinstance(edge[2], VoltageSource)]

    def _get_node_current_constraints(self):
        """
        Return the constraints for the current at each node.
        """
        edges = self.sorted_edges

        n_nodes = len(self.graph.nodes)
        n_edges = len(edges)

        constraints = np.zeros(shape=(n_nodes, n_edges))
        constants = np.zeros(shape=n_nodes)

        for i, node in enumerate(self.graph.nodes):
            for j, current in enumerate(edges):
                if current[0] == node:
                    constraints[i][j] = -1

                elif current[1] == node:
                    constraints[i][j] = +1

        return constraints, constants

    def _get_loop_voltage_constraints(self):
        """
        Return the constraints for the voltage at each loop.
        """
        edges = self.sorted_edges
        loops = self._get_kirchoff_loops()

        n_loops = len(loops)
        n_edges = len(edges)

        constraints = np.zeros(shape=(n_loops, n_edges))
        constants = np.zeros(shape=n_loops)

        for i, loop in enumerate(loops):
            for j, node in enumerate(loop):
                forward_edge = (loop[j - 1], node)
                backward_edge = (node, loop[j - 1])
                for k, edge in enumerate(edges):
                    if forward_edge == edge:
                        direction = +1
                    elif backward_edge == edge:
                        direction = -1
                    else:
                        continue

                    data = self.graph.get_edge_data(*edge)

                    if isinstance(data[self.COMPONENT_KEY], Wire):
                        constraints[i][k] = -direction * data[self.COMPONENT_KEY].resistance
                    elif isinstance(data[self.COMPONENT_KEY], VoltageSource):
                        constants[i] += -direction * data[self.COMPONENT_KEY].voltage

        return constraints, constants

    def _get_current_source_constraints(self):
        """
        Return the constraints for the current at each current source.
        """
        edges = self.sorted_edges
        sources = self._get_current_sources()

        n_sources = len(sources)
        n_edges = len(edges)

        constraints = np.zeros(shape=(n_sources, n_edges))
        constants = np.zeros(shape=n_sources)

        for i, source in enumerate(sources):
            j = self._get_edge_index((source[0], source[1]))
            constraints[i][j] = 1
            constants[i] = source[2].current

        return constraints, constants

    def _get_constraints(self):
        """
        Return the constraints for the circuit.
        """
        current_constraints, current_constants = self._get_node_current_constraints()
        volt_constraints, volt_constants = self._get_loop_voltage_constraints()
        source_constraints, source_constants = self._get_current_source_constraints()
        return (
            np.concatenate((current_constraints, volt_constraints, source_constraints)),
            np.concatenate((current_constants, volt_constants, source_constants))
        )

    def _set_currents(self, current_solution):
        """
        Set the currents in the graph with the current solution.
        """
        for i, edge in enumerate(self.sorted_edges):
            self.graph.edges[edge][self.COMPONENT_KEY].current = current_solution[i]
            component = self.graph.edges[edge][self.COMPONENT_KEY]
            component.label = component.label + f" (I={component.current:.3f}A)"

    def _set_potentials(self):
        """
        Set the potentials in the graph by using the Kirchoff's voltage law and the solved currents
        """
        ground_node = self._position_to_node_mapping[self._ground_position]
        for i, edge in enumerate(nx.bfs_edges(self.graph, ground_node.uid)):
            component = self.graph.edges[edge][self.COMPONENT_KEY]
            if i == 0:
                component.start_node.potential = 0
            if isinstance(component, VoltageSource):
                component.stop_node.potential = component.start_node.potential + component.voltage
            if isinstance(component, Wire):
                component.stop_node.potential = component.start_node.potential - component.current*component.resistance

        for i, node in enumerate(self.nodes):
            node = self.nodes[node][self.NODE_KEY]
            node.label = f"{node.potential:.3f}V"

    def _verify_solvability(self, kirchoff_matrix):
        """
        Verify that the system is solvable by checking that the rank of the matrix is equal to the number of unknowns.
        """
        rank = np.linalg.matrix_rank(kirchoff_matrix)
        if rank != len(self.edges):
            raise ArithmeticError(f"The system is not fully solvable: rank is {rank} vs {self.edges} unknowns")

    def _validate_closed_circuit(self):
        """
        Verify that the circuit is closed by checking that each node has at least one wire start and one wire stop.
        """
        assert self.is_closed, (
            "Circuit is not closed or a node does not have at least one wire start and one wire stop."
        )

    def solve(self) -> List[ElectricalComponent]:
        """
        Solve the circuit by solving Kirchoff's laws and return the components with their currents and potentials.
        """
        kirchoff_matrix, constants = self._get_constraints()

        self._verify_solvability(kirchoff_matrix)

        currents = np.linalg.pinv(kirchoff_matrix) @ constants

        self._set_currents(currents)
        self._set_potentials()

        return self._components

    def display(self, nodes_position_in_figure: dict = None):
        """
        Display the circuit using networkx.
        """

        if not nodes_position_in_figure:
            nodes_position_in_figure = {}
            for n in self.graph.nodes:
                nodes_position_in_figure[n] = (n % 10, -(n // 10))

        edge_labels = {(u, v): self.graph.get_edge_data(u, v)[self.COMPONENT_KEY].label for u, v in self.graph.edges()}
        node_labels = {n: self.nodes[n][self.NODE_KEY].label for n in self.graph.nodes()}

        nx.draw_networkx_nodes(
            G=self.graph,
            pos=nodes_position_in_figure,
            linewidths=3,
            node_size=800,
            node_color='gray',
            alpha=0.9
        )

        nx.draw_networkx_labels(
            G=self.graph,
            pos=nodes_position_in_figure,
            alpha=0.9,
            labels=node_labels,
            font_size=9
        )

        nx.draw_networkx_edges(
            G=self.graph,
            pos=nodes_position_in_figure,
            edge_color='black',
            width=1,
            alpha=0.9
        )

        nx.draw_networkx_edge_labels(
            G=self.graph,
            pos=nodes_position_in_figure,
            font_color='black',
            edge_labels=edge_labels,
            font_size=9,
            verticalalignment='center',
        )

        plt.axis('off')
        plt.show()

    def _get_component_voltage_and_current_fields(
            self,
            component: ElectricalComponent,
            shape: Tuple[int, int],
            minimum: Position,
            maximum: Position
    ):
        """
        Return the voltage and current fields of a component.
        """
        component_voltage = ScalarField(np.zeros(shape))
        component_current = VectorField(np.zeros((shape[0], shape[1], 2)))
        horizontal_values = np.linspace(minimum[0], maximum[0], num=shape[0])
        vertical_values = np.linspace(minimum[1], maximum[1], num=shape[1])

        def get_nearest(value) -> np.ndarray:
            horizontal_idx = (np.abs(horizontal_values - value[0])).argmin()
            vertical_idx = (np.abs(vertical_values - value[1])).argmin()
            return np.array([horizontal_idx, vertical_idx])

        initial_point = np.asarray(component.start_position)
        final_point = np.asarray(component.stop_position)

        axis_vector = final_point - initial_point
        axis_vector_norm = np.linalg.norm(axis_vector)
        normalized_axis_vector = axis_vector / (axis_vector_norm + 1e-16)
        n_increments = int(axis_vector_norm / self._increment_size) + 1

        position_to_evaluate = initial_point
        old_evaluated_point = (0, 0)
        points_in_grid = []
        for increment in range(n_increments):
            movement_vector = position_to_evaluate - initial_point
            new_evaluated_point = component.evaluate_parametric_equations(movement_vector)

            direction_vector = new_evaluated_point - old_evaluated_point
            normalized_direction_vector = direction_vector / (np.linalg.norm(direction_vector) + 1e-16)

            old_evaluated_point = new_evaluated_point
            position_to_evaluate = position_to_evaluate + self._increment_size * normalized_axis_vector
            point_in_grid = get_nearest(initial_point + new_evaluated_point)

            if not list(point_in_grid) in [list(p) for p in points_in_grid]:
                points_in_grid.append(point_in_grid)

            component_current[point_in_grid[0], point_in_grid[1]] = component.current * normalized_direction_vector

        potentials = np.linspace(component.start_node.potential, component.stop_node.potential, len(points_in_grid))
        for point_in_grid, potential in zip(points_in_grid, potentials):
            component_voltage[point_in_grid[0], point_in_grid[1]] = potential

        return component_voltage, component_current

    def get_voltage_and_current_fields(
            self,
            shape: Tuple[int, int],
            minimum: Position,
            maximum: Position
    ):
        """
        Return the voltage and current fields of the circuit after solving the circuit
        """
        self.solve()

        circuit_voltages, circuit_currents = [], []
        for component in self.components:
            voltage, current = self._get_component_voltage_and_current_fields(component, shape, minimum, maximum)
            circuit_voltages.append(voltage)
            circuit_currents.append(current)

        masked_voltages = np.ma.masked_equal(np.array(circuit_voltages), 0)
        masked_voltage = masked_voltages.mean(axis=0)
        circuit_voltage = ScalarField(masked_voltage.data)

        masked_currents = np.ma.masked_equal(np.array(circuit_currents), 0)
        masked_current = masked_currents.mean(axis=0)
        circuit_current = VectorField(masked_current.data)

        return circuit_voltage, circuit_current
