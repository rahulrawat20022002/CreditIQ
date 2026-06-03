import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


# ── Dark theme to match the app (ag-grid renders in its own DOM) ──
_GRID_CSS = {
    ".ag-root-wrapper": {
        "background-color": "#0c1220 !important",
        "border": "1px solid rgba(255,255,255,0.07) !important",
        "border-radius": "10px !important",
    },
    ".ag-header": {
        "background-color": "#111828 !important",
        "border-bottom": "1px solid rgba(255,255,255,0.07) !important",
    },
    ".ag-header-cell-text": {
        "color": "#4a6272 !important",
        "font-size": "11px !important",
        "letter-spacing": "1px !important",
        "text-transform": "uppercase !important",
        "font-weight": "700 !important",
    },
    ".ag-row": {
        "background-color": "#0c1220 !important",
        "color": "#cdd9e5 !important",
        "border-bottom": "1px solid rgba(255,255,255,0.05) !important",
    },
    ".ag-row-hover": {"background-color": "rgba(255,255,255,0.03) !important"},
    ".ag-cell": {
        "display": "flex !important",
        "align-items": "center !important",
        "font-size": "13px !important",
    },
    ".ag-paging-panel": {"color": "#8fa3b8 !important", "border-top": "1px solid rgba(255,255,255,0.07) !important"},
}

# Pill renderer for the Decision column — mirrors the badge style elsewhere.
# Must return a DOM element: ag-grid (v31) escapes HTML strings returned by a renderer.
_VERDICT_RENDERER = JsCode("""
class VerdictRenderer {
    init(params) {
        var approved = params.value === 'APPROVED';
        var color  = approved ? '#34d399' : '#f87171';
        var bg     = approved ? 'rgba(52,211,153,0.12)' : 'rgba(248,113,113,0.12)';
        var border = approved ? 'rgba(52,211,153,0.35)' : 'rgba(248,113,113,0.35)';
        var el = document.createElement('span');
        el.textContent = params.value;
        el.style.cssText = 'background:' + bg + ';color:' + color + ';border:1px solid ' + border +
            ';padding:2px 12px;border-radius:20px;font-size:11px;font-weight:700;letter-spacing:0.5px';
        this.eGui = el;
    }
    getGui() { return this.eGui; }
}
""")

_MONO = {"fontFamily": "'IBM Plex Mono', monospace"}


def render_audit_log():
    log        = st.session_state.audit_log
    total      = len(log)
    approved_n = sum(1 for r in log if r["verdict"] == "APPROVED")
    rejected_n = total - approved_n
    approval_rate = f"{approved_n / total * 100:.0f}%" if total > 0 else "—"

    # ── Summary Stats ──
    st.markdown(f"""
    <div class="audit-summary">
        <div class="audit-stat">
            <div class="audit-stat-num" style="color:#5b9cf6">{total}</div>
            <div class="audit-stat-label">Total Decisions</div>
        </div>
        <div class="audit-stat">
            <div class="audit-stat-num" style="color:#34d399">{approved_n}</div>
            <div class="audit-stat-label">Approved</div>
        </div>
        <div class="audit-stat">
            <div class="audit-stat-num" style="color:#f87171">{rejected_n}</div>
            <div class="audit-stat-label">Rejected</div>
        </div>
        <div class="audit-stat">
            <div class="audit-stat-num" style="color:#fbbf24">{approval_rate}</div>
            <div class="audit-stat-label">Approval Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Decision History — Current Session</div>', unsafe_allow_html=True)

    if not log:
        st.markdown("""
        <div class="card">
            <div class="audit-empty">
                No decisions recorded yet.<br>
                <span style="font-size:0.72rem;color:#4a6272;display:block;margin-top:6px">
                    Run a credit assessment in the first tab to populate this log.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Build dataframe (most recent first) ──
    df = pd.DataFrame([
        {
            "Time":           r["time"],
            "Applicant":      r["name"],
            "Age · Gender":   f"{r['age']} · {r['gender']}",
            "Loan Amount":    r["amount"],
            "Purpose":        r["purpose"],
            "Decision":       r["verdict"],
            "Credit Score":   r["prob_good"],
            "Fairness Group": r["branch"],
            "Threshold":      r["threshold"],
        }
        for r in reversed(log)
    ])

    # ── Grid options ──
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        resizable=True, sortable=True, filter=True,
        cellStyle={"color": "#cdd9e5"},
    )
    gb.configure_grid_options(domLayout="autoHeight", rowHeight=46, headerHeight=42)
    gb.configure_column("Time",         cellStyle={"color": "#4a6272", **_MONO}, maxWidth=110)
    gb.configure_column("Applicant",    cellStyle={"color": "#cdd9e5", "fontWeight": "600"})
    gb.configure_column("Age · Gender", cellStyle={"color": "#8fa3b8"})
    gb.configure_column("Loan Amount",  cellStyle=_MONO)
    gb.configure_column("Purpose",      cellStyle={"color": "#8fa3b8"})
    gb.configure_column("Decision",     cellRenderer=_VERDICT_RENDERER, filter=False, maxWidth=150)
    gb.configure_column("Credit Score", cellStyle={"color": "#5b9cf6", **_MONO}, minWidth=140, maxWidth=180)
    gb.configure_column("Threshold",    cellStyle={"color": "#4a6272", **_MONO}, minWidth=120, maxWidth=160)

    AgGrid(
        df,
        gridOptions=gb.build(),
        custom_css=_GRID_CSS,
        theme="balham",
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        update_mode="no_update",
        key="audit_grid",
    )

    col_btn, col_dl, _ = st.columns([2, 2, 3])
    with col_btn:
        if st.button("Clear Session Log", use_container_width=True):
            st.session_state.audit_log = []
            st.rerun()
    with col_dl:
        st.download_button(
            "Export CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="creditiq_audit_log.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("""
    <div style="font-size:0.7rem;color:#4a6272;margin-top:10px;line-height:1.6">
        The audit log persists for the duration of this browser session. Each entry records the
        demographic group and approval threshold applied, demonstrating the fairness engine in operation.
        Columns are sortable and filterable. This log supports Art. 13 (Transparency) and
        Art. 14 (Human Oversight) under the EU AI Act.
    </div>
    """, unsafe_allow_html=True)
