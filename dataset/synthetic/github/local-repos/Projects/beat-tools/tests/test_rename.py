import sys
from pathlib import Path
from beat_tools.rename import parse, new_name


def test_vendor_and_parens():
    assert new_name(Path("KSHMR Kick 07 (Punchy).wav")) == "kick_punchy_07.wav"


def test_key_and_bpm():
    assert new_name(Path("140_Am_dark_pluck_loop_03.wav")) == "pluck_dark_03_am_140.wav"


def test_keys_alias():
    assert new_name(Path("Lofi Keys - Rhodes Chop 4 85bpm.wav")) == "keys_chop_04_85.wav"


def test_hat_alias():
    assert parse("Unison_Open_HiHat_11")[0] == "hat"


def test_dry_run_changes_nothing(tmp_path, monkeypatch):
    (tmp_path / "Snare - Tight 2.WAV").write_bytes(b"RIFF")
    monkeypatch.setattr(sys, "argv", ["rename", str(tmp_path), "--log", str(tmp_path / "rename_log.csv")])
    from beat_tools import rename
    rename.main()
    assert (tmp_path / "Snare - Tight 2.WAV").exists()


def test_apply_never_overwrites(tmp_path, monkeypatch):
    (tmp_path / "Kick 1 (Punchy).wav").write_bytes(b"RIFF1")
    (tmp_path / "KSHMR Kick 01 (Punchy).wav").write_bytes(b"RIFF2")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["rename", str(tmp_path), "--apply"])
    from beat_tools import rename
    rename.main()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["kick_punchy_01.wav", "kick_punchy_02.wav", "rename_log.csv"]
