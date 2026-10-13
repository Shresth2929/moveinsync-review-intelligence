import os
from streamlit.testing.v1 import AppTest


def test_dashboard_starts_without_data(tmp_path, monkeypatch):
    root = os.path.dirname(os.path.dirname(__file__))
    monkeypatch.chdir(tmp_path)  # no data/ here -> empty-state path
    monkeypatch.syspath_prepend(root)
    at = AppTest.from_file(os.path.join(root, "app.py"), default_timeout=60).run()
    assert not at.exception
    assert any("No review data" in w.value for w in at.warning)
