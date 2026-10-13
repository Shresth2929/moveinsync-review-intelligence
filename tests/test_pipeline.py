import os, subprocess, sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(__file__))


def test_pipeline_csv_import_end_to_end_is_rerunnable(tmp_path):
    """Runs in a temp dir with SYNTHETIC rows; never touches the real data/ folder."""
    rows = [{"reviewId": f"s{i}", "score": 1 if i % 2 else 5, "content": "app crashes on login" if i % 2 else "great app",
             "at": f"2025-0{1 + i % 3}-{10 + i % 15}"} for i in range(30)]
    f = tmp_path / "synthetic.csv"
    pd.DataFrame(rows).to_csv(f, index=False)
    env = {**os.environ, "PYTHONPATH": ROOT}
    for _ in range(2):  # rerun must not duplicate
        r = subprocess.run([sys.executable, "-m", "src.pipeline", "--import-csv", str(f)], cwd=tmp_path, env=env, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
    assert len(pd.read_csv(tmp_path / "data/reviews_clean.csv")) == 30
    rep = (tmp_path / "reports/executive_recommendations.md").read_text()
    assert "15 of 15 negative reviews" in rep or "(100.0%)" in rep
    assert os.path.exists(tmp_path / "data/latest_flags.json")
