import streamlit as st
from groq import Groq
import pandas as pd
import numpy as np
import joblib
import json
import os
import sys

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CreditIQ Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #080c10;
    --bg2:       #0d1219;
    --bg3:       #121820;
    --border:    #1e2730;
    --border2:   #2a3540;
    --text:      #c8d8e8;
    --muted:     #5a7080;
    --accent:    #00c8ff;
    --green:     #00e676;
    --red:       #ff3d57;
    --amber:     #ffab00;
    --card-r:    10px;
}

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg) !important;
    color: var(--text);
}

/* ── Kill default streamlit padding ── */
.main .block-container { padding: 1rem 1.5rem 2rem !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
header { display: none !important; }
footer { display: none !important; }

/* ── TOP HEADER BAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 24px; margin-bottom: 20px;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--card-r);
}
.topbar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem; font-weight: 800;
    color: #fff; letter-spacing: -0.5px;
}
.topbar-brand span { color: var(--accent); }
.topbar-meta { font-size: 0.7rem; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; }
.topbar-pills { display: flex; gap: 10px; }
.pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.7rem; letter-spacing: 0.5px;
    border: 1px solid var(--border2); color: var(--muted);
}
.pill-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 6px var(--green); }
.pill-dot-warn { width: 6px; height: 6px; border-radius: 50%; background: var(--red); box-shadow: 0 0 6px var(--red); }

/* ── SECTION LABELS ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    color: var(--muted); margin-bottom: 12px;
    padding-bottom: 8px; border-bottom: 1px solid var(--border);
}

/* ── CARDS ── */
.card {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--card-r); padding: 20px;
    margin-bottom: 16px;
}
.card-sm {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 8px; padding: 14px 16px;
    margin-bottom: 10px;
}

/* ── RISK GAUGE BAR ── */
.gauge-wrap { margin-bottom: 14px; }
.gauge-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.gauge-label { font-size: 0.72rem; color: var(--muted); }
.gauge-value { font-size: 0.78rem; font-weight: 500; }
.gauge-track {
    height: 6px; background: var(--border);
    border-radius: 3px; overflow: hidden;
}
.gauge-fill { height: 100%; border-radius: 3px; transition: width 0.4s ease; }

/* ── BIG METRIC ── */
.metric-box {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 8px; padding: 16px;
    text-align: center; margin-bottom: 10px;
}
.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800;
    line-height: 1;
}
.metric-label { font-size: 0.68rem; color: var(--muted); margin-top: 4px; letter-spacing: 1px; }

/* ── VERDICT PANEL ── */
.verdict-approved {
    background: linear-gradient(135deg, #001a0e, #002e18);
    border: 1px solid var(--green);
    border-radius: var(--card-r); padding: 24px 28px;
    margin-top: 20px;
}
.verdict-rejected {
    background: linear-gradient(135deg, #1a0005, #2e000c);
    border: 1px solid var(--red);
    border-radius: var(--card-r); padding: 24px 28px;
    margin-top: 20px;
}
.verdict-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem; font-weight: 800;
    letter-spacing: -0.5px; margin-bottom: 4px;
}
.verdict-sub { font-size: 0.78rem; color: var(--muted); margin-bottom: 16px; }
.verdict-body { font-size: 0.82rem; line-height: 1.8; color: var(--text); }
.verdict-body strong { color: #fff; }

/* ── FORM OVERRIDES ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stSlider"] label {
    font-size: 0.72rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── PREDICT BUTTON ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
}
div[data-testid="stButton"] > button:hover {
    background: #33d4ff !important;
    box-shadow: 0 0 24px rgba(0,200,255,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ── API KEY INPUT ── */
.api-row {
    display: flex; gap: 10px; align-items: flex-end;
    padding: 14px 16px;
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--card-r); margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PKL LOADER
# ══════════════════════════════════════════════════════════════
def find_pkl(filename):
    candidates = set()
    candidates.add(os.getcwd())
    try: candidates.add(os.path.dirname(os.path.abspath(__file__)))
    except: pass
    try: candidates.add(os.path.dirname(os.path.abspath(sys.argv[0])))
    except: pass
    for d in candidates:
        if d:
            p = os.path.join(d, filename)
            if os.path.exists(p):
                return p
    return None

def load_models():
    mp = find_pkl("fair_credit_rf_model.pkl")
    cp = find_pkl("model_columns.pkl")
    # credit_data_scaler.pkl contains AIF360 DisparateImpactRemover which
    # requires BlackBoxAuditing — we skip it as it's not needed for inference.
    model   = joblib.load(mp) if mp else None
    columns = joblib.load(cp) if cp else None
    return model, columns

rf_model, model_columns = load_models()
model_loaded = rf_model is not None


# ══════════════════════════════════════════════════════════════
# FEATURE BUILDER
# ══════════════════════════════════════════════════════════════
def build_feature_vector(data: dict, cols: list) -> pd.DataFrame:
    """
    Manually encode features using the exact column names from model_columns.pkl.
    This avoids the pd.get_dummies single-row bug where drop_first=True
    drops the only category present, producing wrong/missing columns.
    """
    if not cols:
        raise ValueError("model_columns is empty — cannot build feature vector.")

    train_cols = [c for c in cols if c != "credit_risk_label"]

    # Start with all zeros
    row = {c: 0.0 for c in train_cols}

    # ── Numeric fields — set directly ─────────────────────────────
    numeric_map = {
        "duration":          float(data.get("duration", 12)),
        "amount":            float(data.get("amount", 0)),
        "installment_rate":  float(data.get("installment_rate", 4)),
        "present_residence": float(data.get("present_residence", 2)),
        "number_credits":    float(data.get("number_credits", 1)),
        "people_liable":     float(data.get("people_liable", 1)),
        "age_group_num":     1.0 if int(data.get("age", 30)) > 25 else 0.0,
        "gender":            1.0 if str(data.get("gender","male")).lower() == "male" else 0.0,
    }
    for k, v in numeric_map.items():
        if k in row:
            row[k] = v

    # ── Categorical fields — match against column names ───────────
    # Column names follow pattern: fieldname_value  (from pd.get_dummies)
    cat_map = {
        "status":                  data.get("status", "no checking account"),
        "credit_history":          data.get("credit_history", "existing credits paid back duly"),
        "purpose":                 data.get("purpose", "furniture/equipment"),
        "savings":                 data.get("savings", "unknown/no savings account"),
        "employment_duration":     data.get("employment_duration", "1<=X<4 years"),
        "other_debtors":           data.get("other_debtors", "none"),
        "property":                data.get("property", "real estate"),
        "other_installment_plans": data.get("other_installment_plans", "none"),
        "housing":                 data.get("housing", "own"),
        "job":                     data.get("job", "skilled employee"),
        "telephone":               data.get("telephone", "none"),
    }

    for field, value in cat_map.items():
        # Look for column named exactly "field_value"
        col_name = f"{field}_{value}"
        if col_name in row:
            row[col_name] = 1.0
        else:
            # Try partial match (handles slight name variations)
            for col in train_cols:
                if col.startswith(f"{field}_") and value.lower() in col.lower():
                    row[col] = 1.0
                    break

    return pd.DataFrame([row])[train_cols].astype(float)


# ══════════════════════════════════════════════════════════════
# RISK INDICATOR HELPERS
# ══════════════════════════════════════════════════════════════
def credit_score_color(score):
    if score < 580: return "#ff3d57"
    if score < 670: return "#ffab00"
    if score < 740: return "#00e676"
    return "#00c8ff"

def credit_score_label(score):
    if score < 580: return "POOR"
    if score < 670: return "FAIR"
    if score < 740: return "GOOD"
    return "EXCELLENT"

def dti_color(dti):
    if dti > 35: return "#ff3d57"   # HIGH — above 35%
    if dti > 20: return "#ffab00"   # MODERATE — 20-35%
    return "#00e676"                 # ACCEPTABLE — below 20%

def dti_label(dti):
    if dti > 35: return "HIGH"
    if dti > 20: return "MODERATE"
    return "ACCEPTABLE"

def employment_risk(emp):
    risky = {"unemployed": ("HIGH", "#ff3d57", 90),
             "< 1 year":   ("MEDIUM", "#ffab00", 55)}
    ok    = {"1<=X<4 years": ("LOW", "#00e676", 25),
             "4<=X<7 years": ("LOW", "#00e676", 15),
             ">= 7 years":   ("VERY LOW", "#00c8ff", 8)}
    if emp in risky: return risky[emp]
    if emp in ok:    return ok[emp]
    return ("LOW", "#00e676", 20)

def savings_score(sav):
    m = {"< 100 DM": 15, "100<=X<500 DM": 35, "500<=X<1000 DM": 65,
         ">= 1000 DM": 90, "unknown/no savings account": 5}
    return m.get(sav, 30)

def gauge_html(label, value_label, fill_pct, color):
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


# ══════════════════════════════════════════════════════════════
# LLM EXPLANATION
# ══════════════════════════════════════════════════════════════
def get_explanation(data, pred_result, api_key):
    client = Groq(api_key=api_key)
    verdict = "APPROVED ✅" if pred_result["approved"] else "REJECTED ❌"
    prompt = f"""The Random Forest credit model returned:

VERDICT: {verdict}
Good Credit Probability: {pred_result['prob_good']}%
Default Probability: {pred_result['prob_bad']}%

Applicant: {json.dumps(data, indent=2)}

Give a concise professional explanation (5–7 sentences) covering:
- Why the model gave this verdict
- Top 2-3 positive factors
- Top 2-3 risk factors
- One actionable recommendation for the finance manager

Use **bold** for key terms. Be direct, no fluff."""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior credit analyst. Be concise, structured, and professional."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )
    return resp.choices[0].message.content


# ══════════════════════════════════════════════════════════════
# TOP BAR
# ══════════════════════════════════════════════════════════════
model_dot = '<span class="pill-dot"></span> RF Model Loaded' if model_loaded else '<span class="pill-dot-warn"></span> PKL Not Found'
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-brand">Credit<span>IQ</span></div>
        <div class="topbar-meta">Credit Eligibility Dashboard · Finance Manager View</div>
    </div>
    <div class="topbar-pills">
        <div class="pill"><span class="pill-dot"></span> Groq · Llama 3.1</div>
        <div class="pill">{model_dot}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# API key row
if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""

with st.container():
    kc1, kc2 = st.columns([5, 1])
    with kc1:
        key_in = st.text_input("GROQ API KEY", value=st.session_state.groq_key,
                               type="password", placeholder="gsk_… · Free key at console.groq.com/keys",
                               label_visibility="visible")
        if key_in: st.session_state.groq_key = key_in
    with kc2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("<a href='https://console.groq.com/keys' target='_blank' style='color:#00c8ff;font-size:0.72rem;text-decoration:none;'>↗ Get free key</a>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MAIN LAYOUT  ·  LEFT (form) | RIGHT (live indicators)
# ══════════════════════════════════════════════════════════════
left, right = st.columns([3, 2], gap="large")

# ── LEFT — FORM ────────────────────────────────────────────────
# Resolve sample flag BEFORE the form widgets reference it
_s = st.session_state.get("_sample", False)

with left:
    st.markdown('<div class="section-label">① Applicant Profile</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("Full Name", placeholder="John Doe", value="Anna Müller" if _s else "")
    with c2: age  = st.number_input("Age", min_value=18, max_value=90, value=42 if _s else 35)
    with c3: gender = st.selectbox("Gender", ["male", "female"], index=1 if _s else 0)

    st.markdown('<div class="section-label" style="margin-top:16px">② Loan Request</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4: amount   = st.number_input("Loan Amount (DM)", min_value=100, max_value=200000, value=2000 if _s else 5000, step=100)
    with c5: duration = st.number_input("Duration (months)", min_value=1, max_value=84, value=12 if _s else 24)
    with c6: purpose  = st.selectbox("Purpose", ["car (new)", "car (used)", "furniture/equipment",
                                                   "radio/television", "education", "business",
                                                   "repairs", "vacation", "other"])

    st.markdown('<div class="section-label" style="margin-top:16px">③ Financial Background</div>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        # ── Display label → raw model value maps ──────────────────────────────
        _status_labels = {
            "No Checking Account":        "no checking account",
            "🔴  Overdrawn  (< 0 DM)":    "< 0 DM",
            "🟡  Low Balance  (0 – 200 DM)":  "0<=X<200 DM",
            "🟢  Healthy  (≥ 200 DM)":    ">= 200 DM",
        }
        _savings_labels = {
            "No Savings Account":             "unknown/no savings account",
            "🔴  Minimal  (< 100 DM)":        "< 100 DM",
            "🟡  Low  (100 – 500 DM)":        "100<=X<500 DM",
            "🟢  Moderate  (500 – 1,000 DM)": "500<=X<1000 DM",
            "🟢  Strong  (≥ 1,000 DM)":       ">= 1000 DM",
        }
        _emp_labels = {
            "🔴  Unemployed":              "unemployed",
            "🟡  Less than 1 Year":        "< 1 year",
            "🟡  1 – 4 Years":             "1<=X<4 years",
            "🟢  4 – 7 Years":             "4<=X<7 years",
            "🟢  7+ Years  (Senior)":      ">= 7 years",
        }
        # Default display keys for sample load
        _status_inv  = {v: k for k, v in _status_labels.items()}
        _savings_inv = {v: k for k, v in _savings_labels.items()}
        _emp_inv     = {v: k for k, v in _emp_labels.items()}

        _status_default  = _status_inv.get(">= 200 DM",             list(_status_labels)[3]) if _s else list(_status_labels)[0]
        _savings_default = _savings_inv.get("unknown/no savings account", list(_savings_labels)[0])
        _emp_default     = _emp_inv.get(">= 7 years",               list(_emp_labels)[4])    if _s else list(_emp_labels)[2]

        status_disp = st.selectbox("Checking Account Status",
                              list(_status_labels.keys()),
                              index=list(_status_labels).index(_status_default))
        status = _status_labels[status_disp]

        savings_disp = st.selectbox("Savings Account",
                               list(_savings_labels.keys()),
                               index=list(_savings_labels).index(_savings_default))
        savings = _savings_labels[savings_disp]
        credit_history = st.selectbox("Credit History",
                                      ["existing credits paid back duly", "all credits paid back duly",
                                       "no credits taken", "delay in paying off", "critical account"])
    with c8:
        installment_rate = st.selectbox("Installment Rate (% of income)", [1, 2, 3, 4], index=0 if _s else 3)
        number_credits   = st.selectbox("Existing Credits at Bank", [1, 2, 3, 4])
        housing          = st.selectbox("Housing", ["own", "free", "rent"])

    st.markdown('<div class="section-label" style="margin-top:16px">④ Employment & Other</div>', unsafe_allow_html=True)
    c9, c10 = st.columns(2)
    with c9:
        emp_disp = st.selectbox("Employment Duration",
                                    list(_emp_labels.keys()),
                                    index=list(_emp_labels).index(_emp_default))
        emp_duration = _emp_labels[emp_disp]
        job = st.selectbox("Job Type", ["skilled employee", "management/self-employed",
                                        "unskilled resident", "unemployed/unskilled non-resident"])
    with c10:
        property_  = st.selectbox("Property", ["real estate", "building society savings",
                                               "car or other", "unknown/no property"])
        other_inst = st.selectbox("Other Installment Plans", ["none", "bank", "stores"])
        other_debt = st.selectbox("Other Debtors", ["none", "co-applicant", "guarantor"])

    telephone     = st.selectbox("Telephone Registered", ["none", "yes"])
    people_liable = st.selectbox("People Liable to Provide Maintenance", [1, 2])

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    pb1, pb2 = st.columns([2,1])
    with pb1:
        predict_btn = st.button("⚡  RUN CREDIT ASSESSMENT", use_container_width=True)
    with pb2:
        sample_btn = st.button("✅ Load Sample Approval", use_container_width=True)

    # Pre-fill ideal approval profile into session state
    if sample_btn:
        st.session_state["_sample"] = True
        st.rerun()




# ── RIGHT — LIVE RISK PANEL ────────────────────────────────────
with right:
    st.markdown('<div class="section-label">Live Risk Indicators</div>', unsafe_allow_html=True)

    # DTI proxy: installment_rate as risk signal (1=low risk, 4=high)
    dti_proxy = installment_rate * 10 + (20 if status == "< 0 DM" else 0)
    dti_col   = dti_color(dti_proxy)

    # Credit score proxy from checking + history
    score_map  = {"no checking account": 720, ">= 200 DM": 760, "0<=X<200 DM": 650, "< 0 DM": 520}
    hist_bonus = {"existing credits paid back duly": 20, "all credits paid back duly": 40,
                  "no credits taken": 0, "delay in paying off": -60, "critical account": -100}
    score_proxy = score_map.get(status, 650) + hist_bonus.get(credit_history, 0)
    score_proxy = max(300, min(850, score_proxy))
    s_col   = credit_score_color(score_proxy)
    s_label = credit_score_label(score_proxy)

    emp_label, emp_col, emp_risk_pct = employment_risk(emp_duration)
    sav_pct = savings_score(savings)
    sav_col = "#00e676" if sav_pct > 50 else ("#ffab00" if sav_pct > 20 else "#ff3d57")

    # Amount-to-duration monthly burden indicator
    monthly_burden = amount / max(duration, 1)
    burden_pct = min(monthly_burden / 500 * 100, 100)
    burden_col = "#ff3d57" if burden_pct > 70 else ("#ffab00" if burden_pct > 40 else "#00e676")

    # Metric numbers — use st.metric so Streamlit always re-renders them
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-num" style="color:{s_col}">{score_proxy}</div>
            <div class="metric-label">Est. Credit Score</div>
            <div style="font-size:0.65rem;color:{s_col};margin-top:2px">{s_label}</div>
        </div>""", unsafe_allow_html=True)
    with mc2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-num" style="color:{dti_col}">{dti_proxy}%</div>
            <div class="metric-label">DTI Estimate</div>
            <div style="font-size:0.65rem;color:{dti_col};margin-top:2px">{dti_label(dti_proxy)}</div>
        </div>""", unsafe_allow_html=True)

    # Gauge bars in a separate markdown block so they also re-render cleanly
    st.markdown(f"""
    <div class="card" style="margin-top:10px">
        {gauge_html("Employment Stability", emp_label, 100 - emp_risk_pct, emp_col)}
        {gauge_html("Savings Health", f"{sav_pct}%", sav_pct, sav_col)}
        {gauge_html("Monthly Loan Burden", f"{monthly_burden:.0f} DM/mo", burden_pct, burden_col)}
        {gauge_html("Credit Score Strength", f"{score_proxy}/850", (score_proxy - 300) / 550 * 100, s_col)}
    </div>
    """, unsafe_allow_html=True)

    # Quick summary flags
    st.markdown('<div class="section-label">Risk Flags</div>', unsafe_allow_html=True)
    flags = []
    if score_proxy < 580:   flags.append(("🔴", "Poor credit score — high default risk"))
    if dti_proxy > 35:      flags.append(("🔴", "High debt burden (DTI > 35%)"))
    elif dti_proxy > 20:   flags.append(("🟡", "Moderate debt burden (DTI 20–35%)"))
    if emp_duration == "unemployed": flags.append(("🔴", "Applicant is unemployed"))
    if emp_duration == "< 1 year":   flags.append(("🟡", "Employment under 1 year"))
    if sav_pct == 5:        flags.append(("🔴", "No savings account — high risk"))
    elif sav_pct < 20:     flags.append(("🟡", "Minimal savings buffer"))
    if status == "< 0 DM":  flags.append(("🔴", "Negative checking balance"))
    if score_proxy >= 670:  flags.append(("🟢", "Credit score in acceptable range"))
    if sav_pct >= 65:       flags.append(("🟢", "Strong savings account"))
    if emp_duration in [">= 7 years", "4<=X<7 years"]: flags.append(("🟢", "Stable employment history"))
    if housing == "own":    flags.append(("🟢", "Owns property — lower risk"))

    if not flags:
        st.markdown('<div class="card-sm" style="color:var(--muted)">Fill in the form to see risk flags.</div>', unsafe_allow_html=True)
    else:
        flag_html = "".join([f'<div class="card-sm" style="font-size:0.78rem">{icon} &nbsp;{msg}</div>' for icon, msg in flags])
        st.markdown(flag_html, unsafe_allow_html=True)

    # Loan snapshot
    st.markdown('<div class="section-label" style="margin-top:8px">Loan Snapshot</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="font-size:0.78rem;line-height:2">
        <div style="display:flex;justify-content:space-between"><span style="color:var(--muted)">Applicant</span><span>{name or '—'}</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:var(--muted)">Amount</span><span>{amount:,} DM</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:var(--muted)">Duration</span><span>{duration} months</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:var(--muted)">Purpose</span><span>{purpose}</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:var(--muted)">Monthly Est.</span><span>{monthly_burden:.0f} DM</span></div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PREDICTION + VERDICT
# ══════════════════════════════════════════════════════════════
if predict_btn:
    if not st.session_state.groq_key:
        st.error("⚠️ Please enter your Groq API key above.")
    elif not model_loaded:
        st.error(f"⚠️ PKL files not found. Looking in: `{os.getcwd()}` — place your .pkl files there and restart.")
    else:
        applicant = {
            "full_name": name, "age": age, "gender": gender,
            "duration": duration, "amount": amount, "purpose": purpose,
            "status": status, "savings": savings, "credit_history": credit_history,
            "installment_rate": installment_rate, "number_credits": number_credits,
            "housing": housing, "employment_duration": emp_duration, "job": job,
            "property": property_, "other_installment_plans": other_inst,
            "other_debtors": other_debt, "telephone": telephone,
            "people_liable": people_liable, "present_residence": 2,
        }

        with st.spinner("Running Random Forest model..."):
            X = build_feature_vector(applicant, model_columns)
            pred  = int(rf_model.predict(X)[0])
            proba = rf_model.predict_proba(X)[0]
            pred_result = {
                "approved":  pred == 1,
                "prob_good": round(float(proba[1]) * 100, 1),
                "prob_bad":  round(float(proba[0]) * 100, 1),
            }

        with st.spinner("Generating LLM explanation..."):
            explanation = get_explanation(applicant, pred_result, st.session_state.groq_key)

        # Format explanation
        import re
        explanation_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', explanation)
        explanation_html = explanation_html.replace('\n', '<br>')

        if pred_result["approved"]:
            verdict_class = "verdict-approved"
            verdict_icon  = "✅ APPROVED"
            verdict_color = "#00e676"
        else:
            verdict_class = "verdict-rejected"
            verdict_icon  = "❌ REJECTED"
            verdict_color = "#ff3d57"

        st.markdown(f"""
        <div class="{verdict_class}">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
                <div>
                    <div class="verdict-title" style="color:{verdict_color}">{verdict_icon}</div>
                    <div class="verdict-sub">Applicant: {name or 'N/A'} · Model confidence: {pred_result['prob_good']}% good credit probability</div>
                </div>
                <div style="display:flex;gap:16px;text-align:center">
                    <div class="metric-box" style="min-width:90px;padding:10px 16px">
                        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#00e676">{pred_result['prob_good']}%</div>
                        <div style="font-size:0.62rem;color:var(--muted);letter-spacing:1px">GOOD CREDIT</div>
                    </div>
                    <div class="metric-box" style="min-width:90px;padding:10px 16px">
                        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:#ff3d57">{pred_result['prob_bad']}%</div>
                        <div style="font-size:0.62rem;color:var(--muted);letter-spacing:1px">DEFAULT RISK</div>
                    </div>
                </div>
            </div>
            <hr>
            <div class="verdict-body">{explanation_html}</div>
        </div>
        """, unsafe_allow_html=True)