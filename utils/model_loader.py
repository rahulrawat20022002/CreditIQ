from __future__ import annotations
import os, sys
import joblib


def find_pkl(filename: str) -> str | None:
    candidates = set()
    candidates.add(os.getcwd())
    try:
        candidates.add(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        pass
    try:
        candidates.add(os.path.dirname(os.path.abspath(sys.argv[0])))
    except Exception:
        pass
    for d in candidates:
        if d:
            p = os.path.join(d, "models", filename)
            if os.path.exists(p):
                return p
            p2 = os.path.join(d, filename)
            if os.path.exists(p2):
                return p2
    return None


def load_models():
    mp = find_pkl("fair_credit_rf_model.pkl")
    cp = find_pkl("model_columns.pkl")
    model   = joblib.load(mp) if mp else None
    columns = joblib.load(cp) if cp else None
    return model, columns
