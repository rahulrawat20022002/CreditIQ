import streamlit as st
from utils.helpers import (
    credit_score_color, credit_score_label,
    debt_ratio_color, debt_ratio_label,
    employment_risk, savings_score, gauge_html,
)
from utils.fairness_engine import (
    THRESHOLD_MATRIX, ADJUSTMENT_EXPLANATIONS, get_demographic_branch
)


def render_risk_panel(fields: dict):
    """Renders the live risk indicator panel (right column)."""

    status           = fields["status"]
    savings          = fields["savings"]
    credit_history   = fields["credit_history"]
    emp_duration     = fields["emp_duration"]
    housing          = fields["housing"]
    age              = fields["age"]
    gender           = fields["gender"]
    amount           = fields["amount"]
    duration         = fields["duration"]
    installment_rate = fields["installment_rate"]
    name             = fields["name"]
    purpose          = fields["purpose"]

    # ── Computed indicators ──
    dti_proxy   = installment_rate * 10 + (20 if status == "< 0 DM" else 0)
    score_map   = {"no checking account": 720, ">= 200 DM": 760, "0<=X<200 DM": 650, "< 0 DM": 520}
    hist_bonus  = {
        "existing credits paid back duly": 20,
        "all credits paid back duly":      40,
        "no credits taken":                 0,
        "delay in paying off":            -60,
        "critical account":              -100,
    }
    score_proxy    = max(300, min(850, score_map.get(status, 650) + hist_bonus.get(credit_history, 0)))
    s_col          = credit_score_color(score_proxy)
    s_label        = credit_score_label(score_proxy)
    dti_col        = debt_ratio_color(dti_proxy)
    dti_lbl        = debt_ratio_label(dti_proxy)
    emp_label, emp_col, emp_risk_pct = employment_risk(emp_duration)
    sav_pct        = savings_score(savings)
    sav_col        = "#34d399" if sav_pct > 50 else ("#fbbf24" if sav_pct > 20 else "#f87171")
    monthly_burden = amount / max(duration, 1)
    burden_pct     = min(monthly_burden / 500 * 100, 100)
    burden_col     = "#f87171" if burden_pct > 70 else ("#fbbf24" if burden_pct > 40 else "#34d399")

    # ── Metric boxes ──
    st.markdown('<div class="section-label">Live Risk Indicators</div>', unsafe_allow_html=True)
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(
            f'<div class="metric-box">'
            f'<div class="metric-num" style="color:{s_col}">{score_proxy}</div>'
            f'<div class="metric-label">Estimated Credit Score</div>'
            f'<div style="font-size:0.68rem;color:{s_col};margin-top:3px;font-weight:600">{s_label}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with mc2:
        st.markdown(
            f'<div class="metric-box">'
            f'<div class="metric-num" style="color:{dti_col}">{dti_proxy}%</div>'
            f'<div class="metric-label">Monthly Debt Ratio</div>'
            f'<div style="font-size:0.68rem;color:{dti_col};margin-top:3px;font-weight:600">{dti_lbl}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='font-size:0.68rem;color:#4a6272;margin:-6px 0 12px;'>"
        "Monthly Debt Ratio = estimated share of take-home pay going to debt repayments. "
        "Above 35% is considered high risk by most lenders."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Fairness Branch Preview — pre-compute everything first ──
    ag, gk       = get_demographic_branch(age, gender)
    preview      = THRESHOLD_MATRIX[(ag, gk)]
    age_label    = "Under 30" if age < 30 else "30 or older"
    gender_label = "Female"   if gender == "female" else "Male"
    explanation  = ADJUSTMENT_EXPLANATIONS[preview["adjustment"]]
    branch_rows  = _branch_rows(ag, gk)
    threshold_pct = f"{preview['threshold']:.0%}"
    preview_label = preview["label"]

    st.markdown(
        '<div class="card" style="margin-top:2px;border-color:rgba(91,156,246,0.25)">'
        '<div class="section-label" style="border:none;padding:0;margin-bottom:10px">'
        'How the Fairness Engine Evaluates This Applicant</div>'
        '<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:14px">'
        '<div style="flex:1;min-width:120px">'
        '<div style="font-size:0.64rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700;margin-bottom:4px">Applicant Group</div>'
        f'<div style="font-size:1rem;font-weight:700;color:#fff">{age_label} &middot; {gender_label}</div>'
        f'<div style="font-size:0.72rem;color:#8fa3b8;margin-top:2px">{preview_label}</div>'
        '</div>'
        '<div style="flex:1;min-width:100px">'
        '<div style="font-size:0.64rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700;margin-bottom:4px">Approval Bar</div>'
        f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:1.6rem;font-weight:400;color:#5b9cf6;line-height:1">{threshold_pct}</div>'
        '<div style="font-size:0.7rem;color:#8fa3b8;margin-top:2px">confidence required</div>'
        '</div>'
        '</div>'
        '<div style="font-size:0.74rem;color:#cdd9e5;line-height:1.7;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:12px 14px;margin-bottom:14px">'
        f'{explanation}'
        '</div>'
        '<div style="font-size:0.64rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700;margin-bottom:8px">'
        'All 4 Groups &mdash; For Transparency</div>'
        '<div style="background:#111828;border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:8px 0">'
        '<div class="branch-header">'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700">Group</div>'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700">Bar</div>'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700">Reason for Adjustment</div>'
        '</div>'
        + branch_rows +
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Gauge bars — pre-compute before embedding ──
    g1 = gauge_html("Employment Stability",        emp_label,               100 - emp_risk_pct,              emp_col)
    g2 = gauge_html("Savings Buffer",              str(sav_pct) + "%",      sav_pct,                         sav_col)
    g3 = gauge_html("Monthly Loan Payment Burden", "\u20ac" + f"{monthly_burden:.0f}" + "/month", burden_pct, burden_col)
    g4 = gauge_html("Credit Score Strength",       str(score_proxy) + " / 850", (score_proxy - 300) / 550 * 100, s_col)
    gauges_html = g1 + g2 + g3 + g4

    st.markdown(
        '<div class="card" style="margin-top:0">' + gauges_html + '</div>',
        unsafe_allow_html=True,
    )

    # ── Risk Flags ──
    st.markdown('<div class="section-label">Risk Flags</div>', unsafe_allow_html=True)
    flags = []
    if score_proxy < 580:                                flags.append(("red",   "Poor credit score — elevated default risk"))
    if dti_proxy > 35:                                   flags.append(("red",   "Monthly debt ratio above 35% — high repayment burden"))
    elif dti_proxy > 20:                                 flags.append(("amber", "Monthly debt ratio 20-35% — moderate burden"))
    if emp_duration == "unemployed":                     flags.append(("red",   "Applicant is currently unemployed"))
    if emp_duration == "< 1 year":                       flags.append(("amber", "Employment tenure under 1 year — limited stability"))
    if sav_pct == 5:                                     flags.append(("red",   "No savings account — limited financial cushion"))
    elif sav_pct < 20:                                   flags.append(("amber", "Very low savings — minimal buffer against default"))
    if status == "< 0 DM":                              flags.append(("red",   "Checking account overdrawn — negative balance"))
    if score_proxy >= 670:                               flags.append(("green", "Credit score in acceptable range"))
    if sav_pct >= 65:                                    flags.append(("green", "Strong savings account"))
    if emp_duration in [">= 7 years", "4<=X<7 years"]:  flags.append(("green", "Stable long-term employment"))
    if housing == "own":                                 flags.append(("green", "Property owner — lower risk profile"))

    color_map = {
        "red":   ("#f87171", "rgba(248,113,113,0.08)", "rgba(248,113,113,0.2)"),
        "amber": ("#fbbf24", "rgba(251,191,36,0.08)",  "rgba(251,191,36,0.2)"),
        "green": ("#34d399", "rgba(52,211,153,0.08)",  "rgba(52,211,153,0.2)"),
    }
    dot_map = {"red": "&#9650;", "amber": "&#9670;", "green": "&#9660;"}

    if not flags:
        st.markdown(
            '<div class="card-sm" style="color:#4a6272">Complete the form to see risk flags.</div>',
            unsafe_allow_html=True,
        )
    else:
        flag_html = ""
        for kind, msg in flags:
            col, bg, border = color_map[kind]
            dot = dot_map[kind]
            flag_html += (
                f'<div class="card-sm" style="font-size:0.78rem;background:{bg};border-color:{border}">'
                f'<span style="color:{col};font-weight:700;margin-right:6px">{dot}</span>{msg}</div>'
            )
        st.markdown(flag_html, unsafe_allow_html=True)

    # ── Loan Snapshot ──
    monthly_str = f"\u20ac{monthly_burden:.0f}"
    amount_str  = f"\u20ac{amount:,}"
    st.markdown('<div class="section-label" style="margin-top:8px">Loan Snapshot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card" style="font-size:0.8rem;line-height:2.1">'
        f'<div style="display:flex;justify-content:space-between"><span style="color:#4a6272">Applicant</span><span>{name or "&mdash;"}</span></div>'
        f'<div style="display:flex;justify-content:space-between"><span style="color:#4a6272">Age &middot; Gender</span><span>{age} &middot; {gender.capitalize()}</span></div>'
        f'<div style="display:flex;justify-content:space-between"><span style="color:#4a6272">Loan Amount</span><span style="font-family:\'IBM Plex Mono\',monospace">{amount_str}</span></div>'
        f'<div style="display:flex;justify-content:space-between"><span style="color:#4a6272">Repayment Period</span><span>{duration} months</span></div>'
        f'<div style="display:flex;justify-content:space-between"><span style="color:#4a6272">Purpose</span><span>{purpose}</span></div>'
        f'<div style="display:flex;justify-content:space-between"><span style="color:#4a6272">Est. Monthly Payment</span><span style="font-family:\'IBM Plex Mono\',monospace">{monthly_str}</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _branch_rows(active_ag: str, active_gk: str) -> str:
    rows = ""
    for (ag, gk), bdata in THRESHOLD_MATRIX.items():
        is_active    = (ag == active_ag and gk == active_gk)
        row_class    = "branch-row branch-row-active" if is_active else "branch-row branch-row-inactive"
        thresh_color = "#5b9cf6" if is_active else "#4a6272"
        name_color   = "#cdd9e5" if is_active else "#8fa3b8"
        weight       = "600"     if is_active else "400"
        thresh_str   = f"{bdata['threshold']:.0%}"
        rows += (
            f'<div class="{row_class}">'
            f'<div style="font-size:0.78rem;color:{name_color};font-weight:{weight}">{bdata["short"]}</div>'
            f'<div style="font-family:IBM Plex Mono,monospace;font-size:1rem;font-weight:500;color:{thresh_color}">{thresh_str}</div>'
            f'<div style="font-size:0.7rem;color:#4a6272">{bdata["rationale"]}</div>'
            '</div>'
        )
    return rows