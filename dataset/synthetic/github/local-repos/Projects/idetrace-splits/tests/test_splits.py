import pandas as pd
import pytest


@pytest.mark.parametrize("version", ["v2", "v2_seed11", "v2_seed23", "v2_seed42", "v2_seed101"])
def test_no_student_in_two_splits(version):
    s = {k: set(pd.read_csv(f"splits/{version}/{k}.csv").student_id) for k in ("train", "val", "test")}
    assert not (s["train"] & s["test"]), "student in train and test"
    assert not (s["train"] & s["val"]), "student in train and val"
    assert not (s["val"] & s["test"]), "student in val and test"


def test_v1_is_unchanged():
    # the submission numbers depend on v1; it must never be regenerated
    assert len(pd.read_csv("splits/v1/test.csv")) == 41207
