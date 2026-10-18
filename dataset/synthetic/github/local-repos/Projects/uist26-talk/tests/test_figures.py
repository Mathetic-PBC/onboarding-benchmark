import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1] / "figures"))
import palette, timeline, transitions, kappa_bar  # noqa: E402

SAMPLE = pd.DataFrame({"t0": [0, 300, 492, 1010], "t1": [300, 492, 1010, 1320],
                       "state": ["productive", "exploring", "stalled-after-error", "productive"]})


def test_transition_figure(tmp_path):
    transitions.draw(SAMPLE, tmp_path / "x.svg")
    assert (tmp_path / "x.svg").stat().st_size > 1000


def test_palette_has_all_six_states():
    assert len(palette.STATE_COLORS) == 6


def test_timeline_frame(tmp_path):
    timeline.strip(SAMPLE, 600, tmp_path / "f.svg", "t")
    assert (tmp_path / "f.svg").exists()


def test_kappa_states_match_palette():
    assert set(kappa_bar.KAPPA) == set(palette.STATE_COLORS)
