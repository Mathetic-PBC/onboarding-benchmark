import glob
import pytest
from beat_tools.bpm import fold


def test_fold():
    assert fold(62) == 124 and fold(248) == 124 and fold(140) == 140


@pytest.mark.skipif(not glob.glob("tests/audio/*.wav"), reason="test audio is not committed")
def test_labeled_loops():
    from beat_tools.bpm import estimate
    for f, want in (("tests/audio/drums_loop_92.wav", 92), ("tests/audio/trap_loop_140.wav", 140)):
        assert estimate(f) == want
