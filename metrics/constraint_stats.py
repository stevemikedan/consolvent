from typing import List, Dict
import pandas as pd

class ConstraintStatsTracker:
    """
    Records and manages constraint field statistics across episodes.
    """
    def __init__(self):
        self.stats_history: List[Dict[str, float]] = []

    def record(self, episode_idx: int, summary_stats: Dict[str, float]):
        """Records summary statistics for an episode."""
        stats = summary_stats.copy()
        stats['episode'] = episode_idx
        self.stats_history.append(stats)

    def get_dataframe(self) -> pd.DataFrame:
        """Returns the history as a pandas DataFrame."""
        return pd.DataFrame(self.stats_history)
