def credit_score_color(score: int) -> str:
    if score < 580: return "#f87171"
    if score < 670: return "#fbbf24"
    if score < 740: return "#34d399"
    return "#5b9cf6"

def credit_score_label(score: int) -> str:
    if score < 580: return "POOR"
    if score < 670: return "FAIR"
    if score < 740: return "GOOD"
    return "EXCELLENT"

def debt_ratio_color(dti: float) -> str:
    if dti > 35: return "#f87171"
    if dti > 20: return "#fbbf24"
    return "#34d399"

def debt_ratio_label(dti: float) -> str:
    if dti > 35: return "HIGH"
    if dti > 20: return "MODERATE"
    return "ACCEPTABLE"

def employment_risk(emp: str) -> tuple[str, str, int]:
    """Returns (label, hex_color, risk_pct)."""
    risky = {
        "unemployed":   ("HIGH",   "#f87171", 90),
        "< 1 year":     ("MEDIUM", "#fbbf24", 55),
    }
    ok = {
        "1<=X<4 years": ("LOW",      "#34d399", 25),
        "4<=X<7 years": ("LOW",      "#34d399", 15),
        ">= 7 years":   ("VERY LOW", "#5b9cf6", 8),
    }
    if emp in risky: return risky[emp]
    if emp in ok:    return ok[emp]
    return ("LOW", "#34d399", 20)

def savings_score(sav: str) -> int:
    m = {
        "< 100 DM":                    15,
        "100<=X<500 DM":               35,
        "500<=X<1000 DM":              65,
        ">= 1000 DM":                  90,
        "unknown/no savings account":   5,
    }
    return m.get(sav, 30)


def gauge_html(label: str, value_label: str, fill_pct: float, color: str) -> str:
    fill_pct = min(max(fill_pct, 0), 100)
    return f"""
    <div class="gauge-wrap">
        <div class="gauge-header">
            <span class="gauge-label">{label}</span>
            <span class="gauge-value" style="color:{color}">{value_label}</span>
        </div>
        <div class="gauge-track">
            <div class="gauge-fill" style="width:{fill_pct}%;background:{color}"></div>
        </div>
    </div>"""
