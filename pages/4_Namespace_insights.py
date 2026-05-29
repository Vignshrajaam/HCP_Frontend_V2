import streamlit as st
import pandas as pd
import io
import sys
from pathlib import Path

# ── Path fix ──────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Page config — MUST be first Streamlit call ────────
st.set_page_config(page_title="Namespace Insights", layout="wide")

# ── Sidebar ───────────────────────────────────────────
from sidebar import render_sidebar
render_sidebar()

# ── Service import ────────────────────────────────────
from services.namespace_insights_service import NamespaceInsightsService

st.title("Namespace Insights")

# ── Guard — no data loaded ────────────────────────────
if "data" not in st.session_state:
    st.warning("⚠️ No data loaded yet. Please upload an HCP ZIP file.")
    st.info("👈 Use the **Upload HCP ZIP**.")
    st.stop()

# ── Load data ─────────────────────────────────────────
data     = st.session_state["data"]
config   = data.get("config", {})
cfgs     = config.get("cluster_cfg", [])
settings = cfgs[0].get("parsed", {}).get("settings", {}) if cfgs else {}

svc          = NamespaceInsightsService(config)
risk_report  = svc.namespace_risk_assessment()
class_report = svc.namespace_classification()

# ── Header ────────────────────────────────────────────
# st.title("Namespace insights")
st.caption(f"{settings.get('clname', '—')} · {len(risk_report)} namespaces analysed")

# ── Summary metrics ───────────────────────────────────
counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
for r in risk_report:
    counts[r.get("severity", "LOW")] += 1

m1, m2, m3, m4 = st.columns(4)
m1.metric("Critical", counts["CRITICAL"])
m2.metric("High",     counts["HIGH"])
m3.metric("Medium",   counts["MEDIUM"])
m4.metric("Low",      counts["LOW"])

st.divider()

# ── Tabs ──────────────────────────────────────────────
tab1, tab2 = st.tabs(["Risk assessment", "Classification"])

# ====================================================
# TAB 1 — Risk assessment
# ====================================================
with tab1:

    sel_sev = st.multiselect(
        "Show severities",
        ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        default=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        key="risk_sev"
    )

    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_risk = sorted(
        risk_report,
        key=lambda x: sev_order.get(x.get("severity", "LOW"), 9)
    )

    badge_colors = {
        "CRITICAL": ("🔴", "#fff5f5", "#c92a2a"),
        "HIGH":     ("🟠", "#fff4e6", "#e8590c"),
        "MEDIUM":   ("🟡", "#fff9db", "#e67700"),
        "LOW":      ("🟢", "#ebfbee", "#2f9e44"),
    }

    for r in sorted_risk:
        sev = r.get("severity", "LOW")
        if sev not in sel_sev:
            continue
        icon, bg, color = badge_colors.get(sev, ("⚪", "#f8f9fa", "#495057"))
        reasons_html = "".join(
            f"<li style='font-size:12px;color:#555'>{reason}</li>"
            for reason in r.get("reasons", [])
        )
        st.markdown(
            f'<div style="background:{bg};border-left:4px solid {color};'
            f'padding:10px 14px;border-radius:4px;margin-bottom:8px">'
            f'<p style="font-weight:600;font-size:13px;margin:0">'
            f'{icon} {r.get("tenant", "—")} / {r.get("name", "—")} '
            f'<span style="display:inline-block;background:{color};color:white;'
            f'padding:4px 12px;border-radius:14px;font-size:14px;'
            f'font-weight:700;margin-left:8px">Score {r.get("score", 0)}</span></p>'
            f'{"<ul style=margin-top:6px;padding-left:18px>" + reasons_html + "</ul>" if reasons_html else ""}'
            f'</div>',
            unsafe_allow_html=True
        )

    if not any(r.get("severity") in sel_sev for r in sorted_risk):
        st.success("No risk findings match the current filter.")

    # Export
    st.divider()
    df_risk = pd.DataFrame([{
        "Tenant":    r.get("tenant"),
        "Namespace": r.get("name"),
        "Severity":  r.get("severity"),
        "Score":     r.get("score"),
        "Reasons":   "; ".join(r.get("reasons", [])),
    } for r in risk_report])

    buf = io.BytesIO()
    df_risk.to_csv(buf, index=False)
    st.download_button(
        "Export risk CSV",
        data=buf.getvalue(),
        file_name=f"ns_risk_{settings.get('clname', 'cluster')}.csv",
        mime="text/csv"
    )

# ====================================================
# TAB 2 — Classification
# ====================================================
with tab2:

    class_counts = {}
    for c in class_report:
        cl = c.get("classification", "—")
        class_counts[cl] = class_counts.get(cl, 0) + 1

    st.markdown("**Classification distribution**")
    cols = st.columns(min(len(class_counts), 4))
    for i, (cl, cnt) in enumerate(sorted(class_counts.items(), key=lambda x: -x[1])):
        cols[i % len(cols)].metric(cl.replace("_", " ").title(), cnt)

    st.divider()

    all_classes = sorted(class_counts.keys())
    sel_class = st.multiselect(
        "Filter by classification",
        all_classes,
        default=all_classes
    )

    rows = []
    for c in class_report:
        if c.get("classification") not in sel_class:
            continue
        rows.append({
            "Tenant":         c.get("tenant", "—"),
            "Namespace":      c.get("name", "—"),
            "Classification": c.get("classification", "—"),
        })

    df_class = pd.DataFrame(rows)
    st.dataframe(df_class, use_container_width=True, hide_index=True)

    # Export
    buf2 = io.BytesIO()
    df_class.to_csv(buf2, index=False)
    st.download_button(
        "Export classification CSV",
        data=buf2.getvalue(),
        file_name=f"ns_classification_{settings.get('clname', 'cluster')}.csv",
        mime="text/csv"
    )