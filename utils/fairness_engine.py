from __future__ import annotations

# ──────────────────────────────────────────────────────────────
# Intersectional Threshold Matrix
# Each demographic group receives a calibrated approval threshold
# that corrects for historical bias in the German Credit dataset.
# ──────────────────────────────────────────────────────────────

THRESHOLD_MATRIX = {
    ("older",   "male"):   {
        "threshold":  0.50,
        "label":      "Standard Group",
        "short":      "Older Male",
        "adjustment": "none",
        "rationale":  "Standard bar — no historical disadvantage detected in lending data.",
    },
    ("older",   "female"): {
        "threshold":  0.44,
        "label":      "Gender-Adjusted Group",
        "short":      "Older Female",
        "adjustment": "gender",
        "rationale":  "Threshold lowered by 6 points to correct for historical gender bias in lending approvals.",
    },
    ("younger", "male"):   {
        "threshold":  0.42,
        "label":      "Age-Adjusted Group",
        "short":      "Younger Male",
        "adjustment": "age",
        "rationale":  "Threshold lowered by 8 points to offset systemic disadvantage against younger applicants.",
    },
    ("younger", "female"): {
        "threshold":  0.42,
        "label":      "Dual-Adjusted Group",
        "short":      "Younger Female",
        "adjustment": "both",
        "rationale":  "Maximum adjustment — applicant faces both age and gender disadvantage in historical data.",
    },
}

# Human-readable explanation for each adjustment type
ADJUSTMENT_EXPLANATIONS = {
    "none": (
        "This applicant belongs to the group with no historical lending disadvantage. "
        "The model applies its standard 50% confidence bar — the same threshold used "
        "as the baseline for all other comparisons."
    ),
    "gender": (
        "Historical lending data shows women were approved at lower rates than equally-qualified men. "
        "To correct this, the model's approval bar is lowered by 6 percentage points, "
        "giving female applicants a fairer evaluation."
    ),
    "age": (
        "Historical data shows applicants under 30 were systematically rejected at higher rates "
        "than older applicants with equivalent credit profiles. "
        "The approval bar is lowered by 8 points to offset this disadvantage."
    ),
    "both": (
        "This applicant faces compounding disadvantages: both gender bias and age bias "
        "are present in the historical training data. The threshold receives the "
        "maximum equity adjustment — an 8 point reduction — to ensure a fair evaluation."
    ),
}


def get_demographic_branch(age: int, gender: str) -> tuple[str, str]:
    age_group  = "younger" if age < 30 else "older"
    gender_key = "female" if str(gender).lower() == "female" else "male"
    return age_group, gender_key


def fair_credit_decision(prob_good: float, age: int, gender: str):
    age_group, gender_key = get_demographic_branch(age, gender)
    branch   = THRESHOLD_MATRIX[(age_group, gender_key)]
    approved = prob_good >= branch["threshold"]
    return approved, branch
