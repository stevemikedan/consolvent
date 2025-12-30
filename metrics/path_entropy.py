import numpy as np
from typing import List, Tuple, Dict

class PathEntropyTracker:
    """
    Computes path entropy as Shannon entropy over normalized edge-usage frequencies.
    Measures trajectory diversity independent of endpoint identity.
    """
    def __init__(self):
        self.entropy_history: List[float] = []

    def calculate_entropy(self, transitions: List[Tuple[int, int]]) -> float:
        """
        Calculates Shannon entropy for a sequence of transitions.
        H = -sum(p_i * log(p_i)) where p_i is the frequency of edge i.
        """
        if not transitions:
            return 0.0
            
        edge_counts: Dict[Tuple[int, int], int] = {}
        for edge in transitions:
            edge_counts[edge] = edge_counts.get(edge, 0) + 1
            
        counts = np.array(list(edge_counts.values()))
        probs = counts / counts.sum()
        
        # Shannon entropy
        entropy = -np.sum(probs * np.log(probs + 1e-12)) # Small epsilon to avoid log(0)
        return float(entropy)

    def record_episode(self, transitions: List[Tuple[int, int]]):
        """Calculates and records entropy for an episode's transition sequence."""
        h = self.calculate_entropy(transitions)
        self.entropy_history.append(h)
        return h

    def get_history(self) -> List[float]:
        """Returns the list of recorded entropy values."""
        return self.entropy_history
