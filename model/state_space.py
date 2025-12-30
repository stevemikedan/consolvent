import networkx as nx
import random
from typing import List, Tuple, Optional

class StateSpace:
    """
    Represents the finite state space of the HCCDE toy model as a graph.
    The system occupies one node at a time.
    """
    def __init__(self, size: int = 100, topology: str = "random_regular", **kwargs):
        self.size = size
        self.topology = topology
        self.graph = self._build_graph(size, topology, **kwargs)
        self.current_state = None

    def _build_graph(self, size: int, topology: str, **kwargs) -> nx.Graph:
        """Builds the graph based on the specified topology."""
        if topology == "random_regular":
            degree = kwargs.get("degree", 4)
            return nx.random_regular_graph(degree, size)
        elif topology == "small_world" or topology == "watts_strogatz":
            k = kwargs.get("k", 4)
            p = kwargs.get("p", 0.1)
            return nx.watts_strogatz_graph(size, k, p)
        elif topology == "erdos_renyi":
            p = kwargs.get("p", 0.04) # p = k / (n-1) -> 4/99 approx 0.04
            return nx.erdos_renyi_graph(size, p)
        else:
            raise ValueError(f"Unsupported topology: {topology}")

    def reset(self, start_node: Optional[int] = None):
        """Initializes or resets the system state to a random or specific node."""
        if start_node is not None:
            if start_node not in self.graph.nodes:
                raise ValueError(f"Start node {start_node} not in graph.")
            self.current_state = start_node
        else:
            self.current_state = random.choice(list(self.graph.nodes))
        return self.current_state

    def get_neighbors(self, node: int) -> List[int]:
        """Returns the neighbors of a given node."""
        return list(self.graph.neighbors(node))

    def get_edges(self) -> List[Tuple[int, int]]:
        """Returns all edges in the graph (directed as pairs)."""
        edges = []
        for u, v in self.graph.edges:
            edges.append((u, v))
            edges.append((v, u)) # Model treats edges as directed for constraints
        return edges

    def set_state(self, node: int):
        """Sets the current state of the system."""
        if node not in self.graph.nodes:
            raise ValueError(f"State {node} not in graph.")
        self.current_state = node
