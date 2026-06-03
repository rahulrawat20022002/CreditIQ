import pandas as pd


def build_feature_vector(data: dict, cols: list) -> pd.DataFrame:
    if not cols:
        raise ValueError("model_columns is empty — cannot build feature vector.")

    train_cols = [c for c in cols if c != "credit_risk_label"]
    row = {c: 0.0 for c in train_cols}

    # ── Numeric fields mapped directly ──
    numeric_map = {
        "duration":          float(data.get("duration", 12)),
        "amount":            float(data.get("amount", 0)),
        "installment_rate":  float(data.get("installment_rate", 4)),
        "age":               float(data.get("age", 35)),
        "number_credits":    float(data.get("number_credits", 1)),
        "people_liable":     float(data.get("people_liable", 1)),
        "present_residence": float(data.get("present_residence", 2)),
        "age_group_num":     1.0 if data.get("age", 35) >= 30 else 0.0,
        "gender":            0.0 if str(data.get("gender", "male")).lower() == "female" else 1.0,
    }
    for col, val in numeric_map.items():
        if col in row:
            row[col] = val

    # ── Categorical fields — one-hot encoding ──
    categorical_fields = [
        "status", "credit_history", "purpose", "savings",
        "employment_duration", "other_debtors", "property",
        "other_installment_plans", "housing", "job", "telephone",
    ]
    for field in categorical_fields:
        value = str(data.get(field, ""))
        for col in train_cols:
            if col.startswith(f"{field}_") and value.lower() in col.lower():
                row[col] = 1.0
                break

    return pd.DataFrame([row])[train_cols].astype(float)
