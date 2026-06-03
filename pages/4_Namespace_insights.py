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
risk_report_raw  = svc.namespace_risk_assessment()
class_report = svc.namespace_classification()
 
# ── Enforce severity mapping based on score ───────────
def get_severity(score: int) -> str:
    if score >= 70:
        return "CRITICAL"
    elif score >= 40:
        return "HIGH"
    elif score >= 20:
        return "MEDIUM"
    else:
        return "LOW"
 
risk_report = []
for item in risk_report_raw:
    score = item.get("score", 0)
    item["severity"] = get_severity(score)
    risk_report.append(item)
 
# ── Header ────────────────────────────────────────────
st.title("Namespace insights")
st.caption(f"{settings.get('clname', '—')} · {len(risk_report)} namespaces analysed")
 
# ── Summary metrics + simplified legend (no highest score) ────
counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
for r in risk_report:
    counts[r.get("severity", "LOW")] += 1
 
col1, col2, col3, col4, col_legend = st.columns([1, 1, 1, 1, 1.2])
with col1: st.metric("Critical", counts["CRITICAL"])
with col2: st.metric("High",     counts["HIGH"])
with col3: st.metric("Medium",   counts["MEDIUM"])
with col4: st.metric("Low",      counts["LOW"])
with col_legend:
    st.markdown(
        """
        <div style="background:#f8f9fa; border-radius:12px; padding:8px 10px;
                    text-align:center; border:1px solid #e9ecef; margin-top: -25px;">
            <div style="font-size:14px; font-weight:600;">Severity</div>
            <div style="display:flex; justify-content:space-between; font-size:16px; margin-top:8px;">
                <span style="color:#c92a2a">🔴 CRIT (≥70)</span>
                <span style="color:#e8590c">🟠 HIGH (≥40)</span>
                <span style="color:#e67700">🟡 MED (≥20)</span>
                <span style="color:#2f9e44">🟢 LOW (&lt;20)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.divider()
 
# ── Tabs ──────────────────────────────────────────────
tab1, tab2 = st.tabs(["Risk assessment", "Classification"])
 
# ====================================================
# TAB 1 — Risk assessment with TABLE preview FIRST
# ====================================================
with tab1:
 
    # ── TABLE PREVIEW (shows scores clearly) ─────────────
    st.markdown("#### Risk assessment table")
    df_risk_preview = pd.DataFrame([{
        "Tenant":    r.get("tenant", "—"),
        "Namespace": r.get("name", "—"),
        "Severity":  r.get("severity", "LOW"),
        "Score":     r.get("score", 0),
        "Reasons":   "; ".join(r.get("reasons", []))[:100] + ("..." if len("; ".join(r.get("reasons", []))) > 100 else "")
    } for r in risk_report])
   
    st.dataframe(
        df_risk_preview,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.NumberColumn("Score", format="%d"),
            "Reasons": st.column_config.TextColumn("Reasons", width="large")
        }
    )
   
    st.markdown("---")
    st.markdown("#### Detailed risk assessment (by severity)")
   
    # ── Severity filter ─────────────────────────────────
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
 
    # Export (full risk report)
    st.divider()
    df_risk_full = pd.DataFrame([{
        "Tenant":    r.get("tenant"),
        "Namespace": r.get("name"),
        "Severity":  r.get("severity"),
        "Score":     r.get("score"),
        "Reasons":   "; ".join(r.get("reasons", [])),
    } for r in risk_report])
 
    buf = io.BytesIO()
    df_risk_full.to_csv(buf, index=False)
    st.download_button(
        "Export full risk CSV",
        data=buf.getvalue(),
        file_name=f"ns_risk_{settings.get('clname', 'cluster')}.csv",
        mime="text/csv"
    )
 
# ====================================================
# TAB 2 — Classification (unchanged)
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
 
    buf2 = io.BytesIO()
    df_class.to_csv(buf2, index=False)
    st.download_button(
        "📥 Export classification CSV",
        data=buf2.getvalue(),
        file_name=f"ns_classification_{settings.get('clname', 'cluster')}.csv",
        mime="text/csv"
    )
 