import streamlit as st
import pandas as pd
import io
import sys
from pathlib import Path

# ── Path fix ──────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Page config — MUST be first Streamlit call ────────
st.set_page_config(page_title="Config Insights", layout="wide")

# ── Sidebar ───────────────────────────────────────────
from sidebar import render_sidebar
render_sidebar()

# ── Service import ────────────────────────────────────
from services.hcp_configuration_analysis_service import HCPConfigurationAnalysisService

# ── Styles ────────────────────────────────────────────
st.markdown("""
<style>
.finding-CRITICAL{background:#fff5f5;border-left:4px solid #e03131;padding:10px 14px;border-radius:4px;margin-bottom:8px}
.finding-WARNING{background:#fff9db;border-left:4px solid #f59f00;padding:10px 14px;border-radius:4px;margin-bottom:8px}
.finding-INFO{background:#e8f4fd;border-left:4px solid #1971c2;padding:10px 14px;border-radius:4px;margin-bottom:8px}
.finding-HEALTHY{background:#ebfbee;border-left:4px solid #2f9e44;padding:10px 14px;border-radius:4px;margin-bottom:8px}
.finding-title{font-weight:600;font-size:13px;margin:0}
.finding-detail{font-size:12px;color:#555;margin:3px 0 0}
.score-box{text-align:center;padding:2rem;border-radius:12px;border:1px solid #e9ecef}
.score-number{font-size:64px;font-weight:700;line-height:1}
.score-rating{font-size:22px;font-weight:600;margin-top:6px}
.score-label{font-size:13px;color:#6c757d;margin-top:4px}
</style>
""", unsafe_allow_html=True)

st.title("Config Insights")

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

svc        = HCPConfigurationAnalysisService(config)
findings   = svc.analyze()
score_data = svc.calculate_hcp_score(findings)
score, rating = score_data["score"], score_data["rating"]

# ── Header ────────────────────────────────────────────
# st.title("Config Insights")
st.caption(f"{settings.get('clname', '—')} — automated health-check findings")

# ── Score + counts ────────────────────────────────────
score_color = "#2f9e44" if score >= 75 else "#f59f00" if score >= 50 else "#e03131"
col_score, col_counts = st.columns([1, 3])

with col_score:
    st.markdown(
        f'<div class="score-box">'
        f'<div class="score-number" style="color:{score_color}">{score}</div>'
        f'<div class="score-rating" style="color:{score_color}">{rating}</div>'
        f'<div class="score-label">/ 100</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_counts:
    severity_order = ["CRITICAL", "WARNING", "INFO", "HEALTHY"]
    counts = {s: sum(1 for f in findings if f.get("severity") == s) for s in severity_order}
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Critical", counts["CRITICAL"])
    c2.metric("Warnings",  counts["WARNING"])
    c3.metric("Info",      counts["INFO"])
    c4.metric("Healthy",   counts["HEALTHY"])

    st.markdown("""
    **Score key**  
    90–100 = Excellent · 75–89 = Good · 50–74 = Fair · 25–49 = Poor · 0–24 = Critical
    """)

st.divider()

# ── Filter controls ───────────────────────────────────
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    categories = sorted(set(f.get("category", "") for f in findings))
    sel_cats = st.multiselect("Filter by category", categories, default=categories)
with col_f2:
    sel_sev = st.multiselect(
        "Filter by severity",
        ["CRITICAL", "WARNING", "INFO", "HEALTHY"],
        default=["CRITICAL", "WARNING", "INFO", "HEALTHY"]
    )

filtered = [
    f for f in findings
    if f.get("severity") in sel_sev and f.get("category", "") in sel_cats
]

# ── Sort: critical first ──────────────────────────────
sev_order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2, "HEALTHY": 3}
filtered.sort(key=lambda f: sev_order.get(f.get("severity", "INFO"), 9))

st.markdown(f"**{len(filtered)} findings**")

# ── Findings list ─────────────────────────────────────
icon_map = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵", "HEALTHY": "🟢"}

for f in filtered:
    sev     = f.get("severity", "INFO")
    cat     = f.get("category", "")
    msg     = f.get("message", "")
    details = f.get("details", "")
    icon    = icon_map.get(sev, "⚪")
    detail_html = (
        f'<p class="finding-detail">{cat} — {details}</p>'
        if details else
        f'<p class="finding-detail">{cat}</p>'
    )
    st.markdown(
        f'<div class="finding-{sev}">'
        f'<p class="finding-title">{icon} {msg}</p>'
        f'{detail_html}'
        f'</div>',
        unsafe_allow_html=True
    )

if not filtered:
    st.success("No findings match the current filters.")

# ── Export ────────────────────────────────────────────
st.divider()

df_export = pd.DataFrame([{
    "Severity": f.get("severity"),
    "Category": f.get("category"),
    "Message":  f.get("message"),
    "Details":  f.get("details", ""),
} for f in findings])

buf = io.BytesIO()
df_export.to_csv(buf, index=False)
st.download_button(
    "Export findings CSV",
    data=buf.getvalue(),
    file_name=f"hcp_findings_{settings.get('clname', 'cluster')}.csv",
    mime="text/csv"
)