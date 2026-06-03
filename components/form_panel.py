import streamlit as st

# ── Display label → model value mappings ──────────────────────
STATUS_LABELS = {
    "No Checking Account":         "no checking account",
    "Overdrawn  (below €0)":       "< 0 DM",
    "Low Balance  (€0 – €200)":    "0<=X<200 DM",
    "Healthy  (€200 or above)":    ">= 200 DM",
}

SAVINGS_LABELS = {
    "No Savings Account":          "unknown/no savings account",
    "Very Low  (under €100)":      "< 100 DM",
    "Low  (€100 – €500)":         "100<=X<500 DM",
    "Moderate  (€500 – €1,000)":  "500<=X<1000 DM",
    "Strong  (€1,000 or above)":  ">= 1000 DM",
}

EMPLOYMENT_LABELS = {
    "Unemployed":           "unemployed",
    "Less than 1 Year":     "< 1 year",
    "1 – 4 Years":          "1<=X<4 years",
    "4 – 7 Years":          "4<=X<7 years",
    "7+ Years (Senior)":    ">= 7 years",
}


def render_form_panel() -> dict:
    """Renders the applicant form. Returns a dict of all field values + predict_btn bool."""

    st.markdown('<div class="section-label">① Applicant Profile</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: name   = st.text_input("Full Name", placeholder="Jane Smith")
    with c2: age    = st.number_input("Age", min_value=18, max_value=90, value=35)
    with c3: gender = st.selectbox("Gender", ["male", "female"])

    st.markdown('<div class="section-label" style="margin-top:16px">② Loan Request</div>', unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4:
        amount = st.number_input(
            "Loan Amount (€)",
            min_value=100, max_value=200_000, value=5_000, step=100,
            help="Amounts are approximate equivalents from historical dataset values.",
        )
    with c5:
        duration = st.number_input("Repayment Period (months)", min_value=1, max_value=84, value=24)
    with c6:
        purpose = st.selectbox("Loan Purpose", [
            "car (new)", "car (used)", "furniture/equipment",
            "radio/television", "education", "business",
            "repairs", "vacation", "other",
        ])

    st.markdown('<div class="section-label" style="margin-top:16px">③ Financial Background</div>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        status_disp = st.selectbox("Checking Account Balance", list(STATUS_LABELS.keys()))
        status      = STATUS_LABELS[status_disp]

        savings_disp = st.selectbox("Savings Account", list(SAVINGS_LABELS.keys()))
        savings      = SAVINGS_LABELS[savings_disp]

        credit_history = st.selectbox("Credit History", [
            "existing credits paid back duly",
            "all credits paid back duly",
            "no credits taken",
            "delay in paying off",
            "critical account",
        ])
    with c8:
        installment_rate = st.selectbox(
            "Monthly Payment (% of take-home pay)",
            [1, 2, 3, 4], index=3,
            help="What share of monthly income will go towards repaying this loan.",
        )
        number_credits = st.selectbox(
            "Existing Loans at This Bank",
            [1, 2, 3, 4],
            help="Number of credit agreements the applicant already holds.",
        )
        housing = st.selectbox("Housing Situation", ["own", "free", "rent"])

    st.markdown('<div class="section-label" style="margin-top:16px">④ Employment & Other Details</div>', unsafe_allow_html=True)
    c9, c10 = st.columns(2)
    with c9:
        emp_disp     = st.selectbox("Employment Duration", list(EMPLOYMENT_LABELS.keys()), index=2)
        emp_duration = EMPLOYMENT_LABELS[emp_disp]
        job          = st.selectbox("Job Category", [
            "skilled employee",
            "management / self-employed",
            "unskilled resident",
            "unemployed / unskilled non-resident",
        ])
    with c10:
        property_  = st.selectbox("Main Asset / Property", [
            "real estate",
            "building society savings",
            "car or other",
            "unknown/no property",
        ])
        other_inst = st.selectbox("Other Repayment Plans", ["none", "bank", "stores"])
        other_debt = st.selectbox("Co-applicant or Guarantor", ["none", "co-applicant", "guarantor"])

    telephone     = st.selectbox("Registered Phone Number", ["none", "yes"])
    people_liable = st.selectbox(
        "Number of Dependants",
        [1, 2],
        help="How many people rely on this applicant financially.",
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    predict_btn = st.button("RUN CREDIT ASSESSMENT", use_container_width=True)

    return {
        "predict_btn":       predict_btn,
        "name":              name,
        "age":               age,
        "gender":            gender,
        "amount":            amount,
        "duration":          duration,
        "purpose":           purpose,
        "status":            status,
        "savings":           savings,
        "credit_history":    credit_history,
        "installment_rate":  installment_rate,
        "number_credits":    number_credits,
        "housing":           housing,
        "emp_duration":      emp_duration,
        "job":               job,
        "property_":         property_,
        "other_inst":        other_inst,
        "other_debt":        other_debt,
        "telephone":         telephone,
        "people_liable":     people_liable,
    }
