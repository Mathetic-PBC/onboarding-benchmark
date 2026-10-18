"""Baseline models. FEATURES are per-window telemetry aggregates computed in data prep."""
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier

FEATURES = ["n_edits", "n_runs", "n_errors", "n_ai_prompts", "n_file_switches", "idle_s", "chars_added", "chars_deleted",
            "secs_since_error", "secs_since_run", "err_streak", "ai_open"]


def make_model(name, **cfg):
    if name == "majority":
        return DummyClassifier(strategy="most_frequent")
    if name == "gbm":
        return HistGradientBoostingClassifier(max_iter=cfg.get("n_estimators", 400), max_depth=cfg.get("max_depth", 6),
                                              learning_rate=cfg.get("learning_rate", 0.05), random_state=7)
    if name == "bilstm":
        from seq_models import BiLSTMClassifier  # torch; windows in session order
        return BiLSTMClassifier(**cfg)
    raise ValueError(name)
