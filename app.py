import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

# ── Page config (must be first Streamlit call) ─────────────────
st.set_page_config(
    page_title="CreditIQ Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Internal imports ───────────────────────────────────────────
from styles.theme          import inject_css
from utils.model_loader    import load_models
from utils.feature_builder import build_feature_vector
from utils.fairness_engine import fair_credit_decision
from utils.llm             import get_explanation
from components.header     import render_header, render_api_key_row
from components.form_panel import render_form_panel
from components.risk_panel import render_risk_panel
from components.verdict_panel   import render_verdict
from components.exec_dashboard  import render_exec_dashboard
from components.audit_log       import render_audit_log

# ── Inject CSS ─────────────────────────────────────────────────
inject_css()

# ── Load model artifacts ───────────────────────────────────────
rf_model, model_columns = load_models()
model_loaded = rf_model is not None

# ── Session state ──────────────────────────────────────────────
if "audit_log"  not in st.session_state: st.session_state.audit_log  = []
if "groq_key"   not in st.session_state: st.session_state.groq_key   = ""

# ── Header ─────────────────────────────────────────────────────
render_header(model_loaded)
render_api_key_row()

# ── Navigator ──────────────────────────────────────────────────
NAV_ITEMS = ["Credit Assessment", "Executive Dashboard", "Audit Log"]
selected = option_menu(
    menu_title=None,
    options=NAV_ITEMS,
    icons=["clipboard2-check", "graph-up-arrow", "journal-text"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {
            "padding": "4px",
            "background-color": "#0c1220",
            "border": "1px solid rgba(255,255,255,0.07)",
            "border-radius": "12px",
            "margin-bottom": "20px",
        },
        "icon": {"color": "#8fa3b8", "font-size": "0.9rem"},
        # inactive tabs: visible chip so it's clear they're explorable
        "nav-link": {
            "font-family": "'Outfit', sans-serif",
            "font-size": "0.82rem",
            "font-weight": "600",
            "letter-spacing": "0.3px",
            "color": "#cdd9e5",
            "background-color": "rgba(255,255,255,0.03)",
            "border": "1px solid rgba(255,255,255,0.07)",
            "border-radius": "9px",
            "padding": "9px 22px",
            "margin": "0 4px",
            "--hover-color": "rgba(91,156,246,0.14)",
        },
        # active tab: strong blue pill
        "nav-link-selected": {
            "background-color": "#5b9cf6",
            "color": "#ffffff",
            "font-weight": "700",
            "border": "1px solid #5b9cf6",
            "box-shadow": "0 2px 12px rgba(91,156,246,0.3)",
        },
    },
)


# ══════════════════════════════════════════════════════════════
# VIEW 1 — CREDIT ASSESSMENT
# ══════════════════════════════════════════════════════════════
if selected == "Credit Assessment":
    left, right = st.columns([3, 2], gap="large")

    with left:
        fields = render_form_panel()

    with right:
        render_risk_panel(fields)

    # ── Prediction logic ───────────────────────────────────────
    if fields["predict_btn"]:
        if not st.session_state.groq_key:
            st.error("Please enter your Groq API key above to generate an explanation.")
        elif not model_loaded:
            st.error(
                f"Model files not found. Place `fair_credit_rf_model.pkl` and "
                f"`model_columns.pkl` in a `models/` subfolder next to `app.py`, "
                f"then restart the app."
            )
        else:
            applicant = {
                "full_name":              fields["name"],
                "age":                    fields["age"],
                "gender":                 fields["gender"],
                "duration":               fields["duration"],
                "amount":                 fields["amount"],
                "purpose":                fields["purpose"],
                "status":                 fields["status"],
                "savings":                fields["savings"],
                "credit_history":         fields["credit_history"],
                "installment_rate":       fields["installment_rate"],
                "number_credits":         fields["number_credits"],
                "housing":                fields["housing"],
                "employment_duration":    fields["emp_duration"],
                "job":                    fields["job"],
                "property":               fields["property_"],
                "other_installment_plans":fields["other_inst"],
                "other_debtors":          fields["other_debt"],
                "telephone":              fields["telephone"],
                "people_liable":          fields["people_liable"],
                "present_residence":      2,
            }

            with st.spinner("Running assessment…"):
                X     = build_feature_vector(applicant, model_columns)
                proba = rf_model.predict_proba(X)[0]
                prob_good = float(proba[1])
                prob_bad  = float(proba[0])

            approved, branch = fair_credit_decision(prob_good, fields["age"], fields["gender"])

            pred_result = {
                "approved":  approved,
                "prob_good": round(prob_good * 100, 1),
                "prob_bad":  round(prob_bad  * 100, 1),
                "branch":    branch,
            }

            with st.spinner("Generating explanation…"):
                explanation = get_explanation(applicant, pred_result, st.session_state.groq_key)

            # Audit log entry
            st.session_state.audit_log.append({
                "time":      datetime.now().strftime("%H:%M:%S"),
                "name":      fields["name"] or "N/A",
                "age":       fields["age"],
                "gender":    fields["gender"].capitalize(),
                "amount":    f"€{fields['amount']:,}",
                "verdict":   "APPROVED" if approved else "REJECTED",
                "prob_good": f"{pred_result['prob_good']}%",
                "branch":    branch["label"],
                "threshold": f"{branch['threshold']:.0%}",
                "purpose":   fields["purpose"],
            })

            with left:
                render_verdict(fields, pred_result, explanation)


# ══════════════════════════════════════════════════════════════
# VIEW 2 — EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════
elif selected == "Executive Dashboard":
    render_exec_dashboard()


# ══════════════════════════════════════════════════════════════
# VIEW 3 — AUDIT LOG
# ══════════════════════════════════════════════════════════════
elif selected == "Audit Log":
    render_audit_log()
