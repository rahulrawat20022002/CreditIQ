import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #070c18;
    --bg2:       #0c1220;
    --bg3:       #111828;
    --glass:     rgba(255,255,255,0.03);
    --glass2:    rgba(255,255,255,0.05);
    --border:    rgba(255,255,255,0.07);
    --border2:   rgba(255,255,255,0.12);
    --text:      #cdd9e5;
    --text2:     #8fa3b8;
    --muted:     #4a6272;
    --accent:    #5b9cf6;
    --accent2:   #3d7de0;
    --green:     #34d399;
    --red:       #f87171;
    --amber:     #fbbf24;
    --card-r:    12px;
    --card-r-sm: 8px;
    --shadow:    0 4px 24px rgba(0,0,0,0.4);
    --shadow-sm: 0 2px 12px rgba(0,0,0,0.3);
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text);
}

.main .block-container { padding: 1rem 1.5rem 2rem !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
header { display: none !important; }
footer { display: none !important; }

/* ── TABS ── */
div[data-testid="stTabs"] > div > div[role="tablist"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--card-r) !important;
    padding: 4px !important;
    gap: 4px !important;
    margin-bottom: 20px !important;
}
div[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    color: var(--text) !important;
    border-radius: 9px !important;
    padding: 9px 22px !important;
    /* visible chip so inactive tabs read as clickable, not plain text */
    border: 1px solid var(--border) !important;
    background: var(--glass) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
/* hover affordance: brighten + lift so it's obvious these are explorable */
div[data-testid="stTabs"] button[role="tab"]:hover:not([aria-selected="true"]) {
    color: #fff !important;
    background: var(--glass2) !important;
    border-color: rgba(91,156,246,0.45) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #fff !important;
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 12px rgba(91,156,246,0.3) !important;
}
div[data-testid="stTabs"] div[role="tabpanel"] {
    border: none !important;
    padding: 0 !important;
}

/* ── TOP HEADER BAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 26px; margin-bottom: 14px;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--card-r);
    box-shadow: var(--shadow);
}
.topbar-brand {
    font-size: 2.3rem; font-weight: 800;
    color: #fff; letter-spacing: -1px; line-height: 1.05;
}
.topbar-brand span { color: var(--accent); }
.topbar-meta { font-size: 0.8rem; color: var(--muted); letter-spacing: 0.3px; margin-top: 6px; }
.topbar-pills { display: flex; gap: 10px; }
.pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 14px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 500;
    border: 1px solid var(--border2); color: var(--text2);
    background: var(--glass);
}
.pill-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); }
.pill-dot-warn { width: 7px; height: 7px; border-radius: 50%; background: var(--red); box-shadow: 0 0 8px var(--red); }

/* ── FAIRNESS STATUS BAR ── */
.fairness-status-bar {
    background: linear-gradient(135deg, var(--bg2), #0a1628);
    border: 1px solid rgba(91,156,246,0.2);
    border-radius: var(--card-r);
    padding: 14px 26px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
}
.fairness-status-left { display: flex; align-items: center; gap: 18px; }
.fairness-badge {
    background: rgba(91,156,246,0.12);
    border: 1px solid rgba(91,156,246,0.4);
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 0.88rem; font-weight: 700;
    color: var(--accent); letter-spacing: 0.3px;
}
.fairness-status-text { font-size: 0.74rem; color: var(--text2); }
.fairness-status-text strong { color: #fff; }
.fairness-status-right {
    font-size: 0.72rem; color: var(--text2);
    display: flex; gap: 22px; flex-wrap: wrap;
}
.compliance-tag {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 4px; padding: 3px 10px;
    color: var(--green); font-size: 0.7rem; font-weight: 600;
}

/* ── SECTION LABELS ── */
.section-label {
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--muted); margin-bottom: 12px;
    padding-bottom: 8px; border-bottom: 1px solid var(--border);
}

/* ── CARDS ── */
.card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--card-r); padding: 20px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-sm);
}
.card-sm {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: var(--card-r-sm); padding: 12px 16px;
    margin-bottom: 8px;
}
.glass-card {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border2);
    border-radius: var(--card-r); padding: 20px;
    margin-bottom: 16px;
}

/* ── RISK GAUGE BAR ── */
.gauge-wrap { margin-bottom: 16px; }
.gauge-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.gauge-label { font-size: 0.74rem; color: var(--text2); font-weight: 500; }
.gauge-value { font-size: 0.76rem; font-weight: 600; }
.gauge-track { height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.gauge-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }

/* ── BIG METRIC ── */
.metric-box {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: var(--card-r-sm); padding: 16px;
    text-align: center; margin-bottom: 10px;
}
.metric-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.1rem; font-weight: 500; line-height: 1;
}
.metric-label { font-size: 0.66rem; color: var(--muted); margin-top: 5px; letter-spacing: 0.8px; text-transform: uppercase; font-weight: 600; }

/* ── VERDICT PANEL ── */
.verdict-approved {
    background: linear-gradient(135deg, #001c10, #00321b);
    border: 1px solid rgba(52,211,153,0.4);
    border-radius: var(--card-r); padding: 26px 30px;
    margin-top: 22px;
    box-shadow: 0 4px 32px rgba(52,211,153,0.1);
}
.verdict-rejected {
    background: linear-gradient(135deg, #1c0007, #330010);
    border: 1px solid rgba(248,113,113,0.4);
    border-radius: var(--card-r); padding: 26px 30px;
    margin-top: 22px;
    box-shadow: 0 4px 32px rgba(248,113,113,0.1);
}
.verdict-title {
    font-size: 1.6rem; font-weight: 800;
    letter-spacing: -0.5px; margin-bottom: 4px;
}
.verdict-sub { font-size: 0.78rem; color: var(--text2); margin-bottom: 18px; }
.verdict-body { font-size: 0.84rem; line-height: 1.8; color: var(--text); }
.verdict-body strong { color: #fff; }

/* ── STATUS BADGES (no emoji) ── */
.badge-pass {
    display: inline-block; padding: 2px 9px; border-radius: 4px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px;
    background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3);
    color: var(--green);
}
.badge-warn {
    display: inline-block; padding: 2px 9px; border-radius: 4px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px;
    background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3);
    color: var(--amber);
}
.badge-fail {
    display: inline-block; padding: 2px 9px; border-radius: 4px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px;
    background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3);
    color: var(--red);
}
.badge-approved {
    display: inline-block; padding: 3px 10px; border-radius: 4px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;
    background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3);
    color: var(--green);
}
.badge-rejected {
    display: inline-block; padding: 3px 10px; border-radius: 4px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;
    background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3);
    color: var(--red);
}

/* ── FAIRNESS TRANSPARENCY CARD ── */
.fairness-card {
    background: linear-gradient(135deg, var(--bg2), #0a1628);
    border: 1px solid rgba(91,156,246,0.25);
    border-radius: var(--card-r); padding: 22px 26px;
    margin-top: 18px;
    box-shadow: 0 4px 24px rgba(91,156,246,0.08);
}
.fairness-title {
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--accent); margin-bottom: 16px;
}
.threshold-display {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem; font-weight: 400;
    color: #fff; margin: 4px 0;
}
.fairness-row { display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap; }
.fairness-col { flex: 1; min-width: 120px; }
.fairness-col-label { font-size: 0.64rem; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; font-weight: 600; }

/* ── FAIRNESS BRANCH EXPLANATION ── */
.branch-explain-card {
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: var(--card-r); padding: 18px 20px;
    margin-bottom: 14px;
}
.branch-explain-who {
    font-size: 0.88rem; font-weight: 600; color: #fff;
    margin-bottom: 4px;
}
.branch-explain-group {
    font-size: 1.1rem; font-weight: 700; color: var(--accent);
    margin: 8px 0 4px;
}
.branch-explain-body {
    font-size: 0.76rem; color: var(--text2); line-height: 1.7;
    border-top: 1px solid var(--border);
    padding-top: 10px; margin-top: 10px;
}

/* ── EXEC DASHBOARD ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px; }
.kpi-card {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--card-r); padding: 22px 18px;
    text-align: center;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: var(--border2); }
.kpi-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.3rem; font-weight: 500; line-height: 1;
    margin-bottom: 8px;
}
.kpi-label { font-size: 0.64rem; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
.kpi-sub { font-size: 0.70rem; margin-top: 5px; font-weight: 500; }

.reg-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.reg-table th { font-size: 0.64rem; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; padding: 8px 14px; border-bottom: 1px solid var(--border); text-align: left; font-weight: 700; }
.reg-table td { padding: 11px 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.reg-table tr:last-child td { border-bottom: none; }
.reg-table tr:hover td { background: var(--glass); }

.comparison-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.comparison-table th { font-size: 0.64rem; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; padding: 8px 14px; border-bottom: 1px solid var(--border); text-align: left; font-weight: 700; }
.comparison-table td { padding: 11px 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.comparison-table tr:last-child td { border-bottom: none; }
.comparison-table tr.best-row { background: rgba(91,156,246,0.05); }
.comparison-table tr.best-row td:first-child { color: #fff; font-weight: 600; }

/* ── AUDIT LOG ── */
.audit-summary {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
    margin-bottom: 22px;
}
.audit-stat {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--card-r); padding: 20px;
    text-align: center;
}
.audit-stat-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem; font-weight: 500; line-height: 1; margin-bottom: 6px;
}
.audit-stat-label { font-size: 0.64rem; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
.audit-empty { text-align: center; padding: 40px; color: var(--muted); font-size: 0.82rem; }
.audit-table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
.audit-table th { font-size: 0.62rem; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; padding: 10px 14px; border-bottom: 1px solid var(--border); text-align: left; font-weight: 700; white-space: nowrap; background: var(--bg3); }
.audit-table td { padding: 11px 14px; border-bottom: 1px solid var(--border); vertical-align: middle; white-space: nowrap; }
.audit-table tr:last-child td { border-bottom: none; }
.audit-table tr:hover td { background: var(--glass); }
.audit-branch {
    font-size: 0.68rem; font-weight: 600; padding: 2px 8px;
    background: rgba(91,156,246,0.1); border: 1px solid rgba(91,156,246,0.2);
    border-radius: 4px; color: var(--accent);
}

/* ── FORM OVERRIDES ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
    font-size: 0.72rem !important;
    color: var(--text2) !important;
    letter-spacing: 0.3px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.84rem !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
}

/* ── BUTTONS ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 14px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
    box-shadow: 0 4px 16px rgba(91,156,246,0.25) !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--accent2) !important;
    box-shadow: 0 6px 24px rgba(91,156,246,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── BRANCH MATRIX TABLE ── */
.branch-row {
    display: grid;
    grid-template-columns: 150px 80px 1fr;
    align-items: center; gap: 14px;
    padding: 11px 16px;
    border-radius: 6px;
    margin-bottom: 3px;
    cursor: default;          /* read-only reference table — not clickable */
    pointer-events: none;     /* disable hover/active affordances */
}
.branch-row-active {
    background: rgba(91,156,246,0.08);
    border-left: 3px solid var(--accent);
}
.branch-row-inactive { border-left: 3px solid transparent; }
.branch-header {
    display: grid;
    grid-template-columns: 150px 80px 1fr;
    gap: 14px; padding: 6px 16px 8px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 6px;
}

hr { border-color: var(--border) !important; margin: 18px 0 !important; }

/* ── API KEY INPUT ── */
.api-key-row { margin-bottom: 12px; }
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
