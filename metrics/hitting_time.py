from typing import List

class HittingTimeTracker:
    """
    Tracks hitting times (T_k) across episodes.
    """
    def __init__(self):
        self.hitting_times: List[int] = []

    def record(self, t_k: int):
        """Records the hitting time for an episode."""
        self.hitting_times.append(t_k)

    def get_history(self) -> List[int]:
        """Returns the list of recorded hitting times."""
        return self.hitting_times
