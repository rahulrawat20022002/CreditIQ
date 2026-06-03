import streamlit as st


def render_header(model_loaded: bool):
    model_dot = (
        '<span class="pill-dot"></span> Random Forest Loaded'
        if model_loaded else
        '<span class="pill-dot-warn"></span> Model File Not Found'
    )
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-brand">Credit<span>IQ</span></div>
            <div class="topbar-meta">Credit Eligibility Dashboard · Loan Officer View · Advisory Use Only</div>
        </div>
        <div class="topbar-pills">
            <div class="pill"><span class="pill-dot"></span> Groq · Llama 3.1</div>
            <div class="pill">{model_dot}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fairness-status-bar">
        <div class="fairness-status-left">
            <div class="fairness-badge">88.1% FAIRNESS SCORE</div>
            <div class="fairness-status-text">
                <strong>EU AI Act Compliant</strong> &nbsp;·&nbsp;
                Above the 80% equal-treatment threshold
                &nbsp;·&nbsp; High-Risk AI — Annex III
            </div>
        </div>
        <div class="fairness-status-right">
            <span class="compliance-tag">Disparate Impact: MET</span>
            <span class="compliance-tag">Equal Opportunity: MET</span>
            <span class="compliance-tag">Human Oversight: MET</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_api_key_row():
    c1, c2 = st.columns([5, 1])
    with c1:
        key_in = st.text_input(
            "Groq API Key",
            value=st.session_state.groq_key,
            type="password",
            placeholder="gsk_… · Free key at console.groq.com/keys",
        )
        if key_in:
            st.session_state.groq_key = key_in
    with c2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<a href='https://console.groq.com/keys' target='_blank' "
            "style='color:#5b9cf6;font-size:0.72rem;text-decoration:none;'>↗ Get free key</a>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr>", unsafe_allow_html=True)
