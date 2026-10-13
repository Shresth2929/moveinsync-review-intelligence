import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pandas as pd, pytest


@pytest.fixture
def synthetic():
    """SYNTHETIC TEST FIXTURE ONLY - not real reviews, never used in analysis."""
    return pd.DataFrame({
        "reviewId": ["a", "b", "b", "c", "d", "e", "f"],
        "score": [1, 2, 2, 5, 7, 1, 4],
        "content": ["app crashes on login", "cab is always late, wrong eta", "cab is always late, wrong eta",
                    "Great app, easy to use", "invalid rating row", "", "ok"],
        "at": ["2025-01-05", "2025-01-20", "2025-01-20", "2025-02-02", "2025-02-03", None, "2025-02-10"],
    })
