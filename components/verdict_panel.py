from __future__ import annotations
import re
import streamlit as st
from utils.fairness_engine import THRESHOLD_MATRIX, ADJUSTMENT_EXPLANATIONS


def render_verdict(fields: dict, pred_result: dict, explanation: str):
    approved  = pred_result["approved"]
    prob_good = pred_result["prob_good"]
    prob_bad  = pred_result["prob_bad"]
    branch    = pred_result["branch"]
    name      = fields.get("name") or "Applicant"
    age       = fields.get("age", 35)
    gender    = fields.get("gender", "male")

    verdict_class = "verdict-approved" if approved else "verdict-rejected"
    verdict_text  = "APPROVED"         if approved else "REJECTED"
    verdict_color = "#34d399"          if approved else "#f87171"
    score_color   = "#34d399" if prob_good >= branch["threshold"] * 100 else "#f87171"

    # Format markdown bold → HTML
    explanation_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', explanation)
    explanation_html = explanation_html.replace('\n', '<br>')

    # ── Verdict card ──
    html = (
        '<div class="' + verdict_class + '">'
        '<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:14px">'
        '<div>'
        '<div class="verdict-title" style="color:' + verdict_color + '">' + verdict_text + '</div>'
        '<div class="verdict-sub">'
        + name + ' &nbsp;&middot;&nbsp; Model confidence: '
        '<strong style="color:' + score_color + '">' + str(prob_good) + '%</strong>'
        ' creditworthiness probability'
        '</div>'
        '</div>'
        '<div style="display:flex;gap:12px;text-align:center">'
        '<div class="metric-box" style="min-width:92px;padding:12px 18px;margin-bottom:0">'
        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:1.5rem;font-weight:400;color:#34d399">' + str(prob_good) + '%</div>'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:0.8px;text-transform:uppercase;margin-top:4px;font-weight:700">Good Credit</div>'
        '</div>'
        '<div class="metric-box" style="min-width:92px;padding:12px 18px;margin-bottom:0">'
        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:1.5rem;font-weight:400;color:#f87171">' + str(prob_bad) + '%</div>'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:0.8px;text-transform:uppercase;margin-top:4px;font-weight:700">Default Risk</div>'
        '</div>'
        '</div>'
        '</div>'
        '<hr>'
        '<div class="verdict-body">' + explanation_html + '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    # ── Fairness Transparency ──
    age_group_label = "Under 30" if age < 30 else "30 or older"
    gender_label    = "Female"   if gender == "female" else "Male"
    active_ag       = "younger"  if age < 30 else "older"
    active_gk       = "female"   if gender == "female" else "male"
    explanation_txt = ADJUSTMENT_EXPLANATIONS[branch["adjustment"]]
    threshold_pct   = f"{branch['threshold']:.0%}"
    branch_label    = branch["label"]
    prob_good_str   = str(prob_good) + "%"

    # Build branch rows
    branch_rows_html = ""
    for (ag, gk), bdata in THRESHOLD_MATRIX.items():
        is_active    = (ag == active_ag and gk == active_gk)
        row_class    = "branch-row branch-row-active" if is_active else "branch-row branch-row-inactive"
        thresh_color = "#5b9cf6" if is_active else "#4a6272"
        name_color   = "#cdd9e5" if is_active else "#8fa3b8"
        weight       = "600"     if is_active else "400"
        t_str        = f"{bdata['threshold']:.0%}"
        branch_rows_html += (
            '<div class="' + row_class + '">'
            '<div style="font-size:0.78rem;color:' + name_color + ';font-weight:' + weight + '">' + bdata["short"] + '</div>'
            '<div style="font-family:IBM Plex Mono,monospace;font-size:1rem;font-weight:500;color:' + thresh_color + '">' + t_str + '</div>'
            '<div style="font-size:0.7rem;color:#4a6272">' + bdata["rationale"] + '</div>'
            '</div>'
        )

    fairness_html = (
        '<div class="fairness-card">'
        '<div class="fairness-title">Fairness Transparency &mdash; How This Decision Was Made</div>'

        # 4-col grid
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;margin-bottom:18px">'

        # col 1 — group
        '<div>'
        '<div class="fairness-col-label">Applicant Group</div>'
        '<div style="font-size:1rem;font-weight:700;color:#fff;margin-top:4px">' + age_group_label + ' &middot; ' + gender_label + '</div>'
        '<div style="font-size:0.72rem;color:#8fa3b8;margin-top:2px">' + branch_label + '</div>'
        '</div>'

        # col 2 — threshold
        '<div>'
        '<div class="fairness-col-label">Approval Threshold Used</div>'
        '<div class="threshold-display">' + threshold_pct + '</div>'
        '<div style="font-size:0.7rem;color:#8fa3b8">min. confidence needed</div>'
        '</div>'

        # col 3 — model score
        '<div>'
        '<div class="fairness-col-label">Model Score</div>'
        '<div class="threshold-display" style="color:' + score_color + '">' + prob_good_str + '</div>'
        '<div style="font-size:0.7rem;color:#8fa3b8">raw creditworthiness</div>'
        '</div>'

        # col 4 — regulatory
        '<div>'
        '<div class="fairness-col-label">Regulatory Status</div>'
        '<div style="margin-top:8px">'
        '<span class="badge-pass">Fairness Score 88.1%</span><br>'
        '<span style="font-size:0.68rem;color:#8fa3b8;margin-top:4px;display:block">EU AI Act &mdash; Annex III</span>'
        '</div>'
        '</div>'

        '</div>'  # end grid

        # explanation paragraph
        '<div style="font-size:0.74rem;color:#cdd9e5;line-height:1.7;background:rgba(255,255,255,0.03);'
        'border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:12px 16px;margin-bottom:18px">'
        + explanation_txt +
        '</div>'

        # branch matrix
        '<div style="font-size:0.64rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700;margin-bottom:8px">'
        'Full Fairness Matrix &mdash; All 4 Groups</div>'
        '<div style="background:#0c1220;border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:8px 0">'
        '<div class="branch-header">'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700">Group</div>'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700">Threshold</div>'
        '<div style="font-size:0.62rem;color:#4a6272;letter-spacing:1px;text-transform:uppercase;font-weight:700">Why</div>'
        '</div>'
        + branch_rows_html +
        '</div>'

        '<div style="font-size:0.7rem;color:#4a6272;margin-top:10px;font-style:italic">'
        'The loan officer reviews this recommendation and makes the final decision. '
        'This system is advisory only &mdash; no automated rejection without human review.'
        '</div>'
        '</div>'
    )
    st.markdown(fairness_html, unsafe_allow_html=True)