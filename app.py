import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sidebar import render_sidebar
from services.hcp_configuration_analysis_service import HCPConfigurationAnalysisService

st.set_page_config(
    page_title="HCP SmartAnalytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

render_sidebar()

st.title("HCP SmartAnalytics")

if "data" not in st.session_state:
    st.markdown("Upload your HCP diagnostic ZIP on the left to get started.")
    st.markdown("""
| Slides | Contents |
|---|---|
| **1 · Cluster summary** | Nodes, network, security, storage |
| **2 · Config insights** | Health-check findings + HCP score |
| **3 · Tenants & namespaces** | Filterable tables, CSV export |
| **4 · Namespace insights** | Risk assessment & classification |
| **5 · Query engine** | Namespace query with custom filters |
| **6 · Access log analysis** | Traffic, errors, security, anomalies |
""")

else:
    data       = st.session_state["data"]
    config     = data.get("config", {})
    cfgs       = config.get("cluster_cfg", [])
    s          = cfgs[0].get("parsed", {}).get("settings", {}) if cfgs else {}
    nodes_raw  = config.get("nodes", {})
    nodes      = nodes_raw.get("nodes", []) if isinstance(nodes_raw, dict) else []
    active     = [n for n in nodes if str(n.get("removed", "")).lower() != "true"]
    tenants    = data.get("tenants", [])
    namespaces = data.get("namespaces", [])

    analysis_svc = HCPConfigurationAnalysisService(config)
    findings     = analysis_svc.analyze()
    score_data   = analysis_svc.calculate_hcp_score(findings)
    score, rating = score_data["score"], score_data["rating"]
    score_color  = "#2f9e44" if score >= 75 else "#f59f00" if score >= 50 else "#e03131"

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Cluster",      s.get("clname", "—"))
    c2.metric("HCP version",  s.get("software_version", "—"))
    c3.metric("Active nodes", len(active))
    c4.metric("Tenants",      len(tenants))
    c5.metric("Namespaces",   len(namespaces))

    st.divider()
    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.markdown(
            f'<div class="score-box">'
            f'<div class="score-number" style="color:{score_color}">{score}</div>'
            f'<div style="font-size:22px;font-weight:600;color:{score_color};margin-top:4px">{rating}</div>'
            f'<div class="score-label">HCP configuration score / 100</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown("**Finding summary**")
        fc, fw, fp = st.columns(3)
        fc.metric("Critical",       sum(1 for f in findings if f.get("severity") == "CRITICAL"))
        fw.metric("Warnings",       sum(1 for f in findings if f.get("severity") == "WARNING"))
        fp.metric("Info / healthy", sum(1 for f in findings if f.get("severity") in ("INFO", "HEALTHY")))
        st.caption("Use the sidebar to navigate to any analysis page.")


#5 · Node planning** | Tech refresh & node addition wizard