import streamlit as st
import pandas as pd
import io
import sys
from pathlib import Path
 
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
 
# Sidebar
from sidebar import render_sidebar
 
st.title("Tenants & Namespaces")
 
# ─────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tenants & Namespaces",
    layout="wide"
)
 
# Add custom CSS to align all inputs perfectly
st.markdown("""
    <style>
    /* Align text inputs and select boxes */
    .stTextInput, .stSelectbox {
        margin-top: -10px;
    }
   
    /* Adjust container spacing */
    .stColumn {
        vertical-align: bottom;
    }
   
    /* Make sure all form elements align properly */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
   
    /* Reduce spacing between label row and filter row */
    .stMarkdown {
        margin-bottom: -10px;
    }
    </style>
""", unsafe_allow_html=True)
 
# Render Sidebar
render_sidebar()
 
# ─────────────────────────────────────────────────────
# DATA VALIDATION
# ─────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.warning("⚠️ No data loaded yet. Please upload an HCP ZIP file.")
    st.info("👈 Use the **Upload HCP ZIP**.")
    st.stop()
 
# ─────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────
data = st.session_state["data"]
 
config = data.get("config", {})
cfgs = config.get("cluster_cfg", [])
 
settings = (
    cfgs[0].get("parsed", {}).get("settings", {})
    if cfgs else {}
)
 
tenants = data.get("tenants", [])
namespaces = data.get("namespaces", [])
 
# ─────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────
def bytes_to_human(b):
    try:
        b = int(b)
 
        if b < 0:
            return "Unlimited"
 
        if b == 0:
            return "0 B"
 
        for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
            if b < 1024:
                return f"{b:.1f} {unit}"
            b /= 1024
 
        return f"{b:.1f} PB"
 
    except Exception:
        return str(b)
 
# ─────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────
# st.title("Tenants & Namespaces")
 
st.caption(
    f"{settings.get('clname', '—')} · "
    f"{len(tenants)} tenants · "
    f"{len(namespaces)} namespaces"
)
 
# ─────────────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────────────
m1, m2, m3 = st.columns(3)
 
m1.metric("Total Tenants", len(tenants))
m2.metric("Total Namespaces", len(namespaces))
 
repl_on = sum(
    1 for t in tenants
    if t.get("replication_enabled") is True
)
 
m3.metric("Tenants with Replication", repl_on)
 
st.divider()
 
# ─────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Tenants", "Namespaces"])
 
# ====================================================
# TENANTS TAB
# ====================================================
with tab1:
 
    # Add labels in a separate row above the filters
    col_label1, col_label2 = st.columns([12, 1])
   
    with col_label1:
        st.markdown("**Search Tenants**")
   
    # Filter controls row
    col_s, col_f = st.columns([12, 1])
 
    with col_s:
        search = st.text_input(
            "Search tenants",
            placeholder="Search by tenant name...",
            key="t_search",
            label_visibility="collapsed"
        )

 
    tenant_rows = []
 
    for t in tenants:
 
        state_val = str(t.get("state", ""))
        is_active = state_val == "2"
 
        # Search filter
        if search:
            if search.lower() not in str(t.get("name", "")).lower():
                continue
 
        # Namespace count
        ns_count = sum(
            1 for n in namespaces
            if n.get("tenant") == t.get("name")
        )
 
        tenant_rows.append({
            "Name": t.get("name", "—"),
            "Replication": "✅" if t.get("replication_enabled") else "❌",
            "Search": "✅" if t.get("search_enabled") else "❌",
            "Versioning": "✅" if t.get("versioning_enabled") else "❌",
            "MAPI": "✅" if t.get("mapi_enabled") else "❌",
            "Hard Quota": bytes_to_human(t.get("hard_quota", 0)),
            "NS Quota": str(t.get("namespace_quota", "—")),
            "Auth Type": str(t.get("authentication_types", "—")),
            "Service Plan": t.get("service_plan", "—"),
            "Namespaces": ns_count,
        })
 
    df_tenants = pd.DataFrame(tenant_rows)
 
    st.dataframe(
        df_tenants,
        use_container_width=True,
        hide_index=True
    )
 
    # Export CSV
    tenant_csv = io.BytesIO()
 
    df_tenants.to_csv(
        tenant_csv,
        index=False
    )
 
    st.download_button(
    "Export Tenants CSV",
    tenant_csv.getvalue(),
    file_name=f"tenants_{settings.get('clname', 'cluster')}.csv",
    mime="text/csv"
    )
 
# ====================================================
# NAMESPACES TAB
# ====================================================
with tab2:
 
    # Add labels in a separate row above the filters
    col_label1, col_label2, col_label3 = st.columns([2, 1, 1])
   
    with col_label1:
        st.markdown("**Search**")
   
    with col_label2:
        st.markdown("**Tenant**")
   
    with col_label3:
        st.markdown("**Protocol**")
   
    # Filter controls row
    col_s2, col_f2, col_f3 = st.columns([2, 1, 1])
 
    with col_s2:
        ns_search = st.text_input(
            "Search namespaces",
            placeholder="Search namespace or tenant...",
            key="ns_search",
            label_visibility="collapsed"
        )
 
    with col_f2:
        tenant_list = ["All"] + sorted(
            set(
                n.get("tenant", "")
                for n in namespaces
                if n.get("tenant")
            )
        )
 
        sel_tenant = st.selectbox(
            "Tenant",
            tenant_list,
            key="ns_tenant",
            label_visibility="collapsed"
        )
 
    with col_f3:
        proto_filter = st.selectbox(
            "Protocol",
            ["All", "S3", "HTTPS only", "HTTP enabled"],
            key="ns_proto",
            label_visibility="collapsed"
        )
 
    ns_rows = []
 
    for n in namespaces:
 
        combined_text = (
            f"{n.get('name', '')} "
            f"{n.get('tenant', '')}"
        ).lower()
 
        # Search filter
        if ns_search:
            if ns_search.lower() not in combined_text:
                continue
 
        # Tenant filter
        if sel_tenant != "All":
            if n.get("tenant") != sel_tenant:
                continue
 
        # Protocol filters
        if proto_filter == "S3" and not n.get("s3_enabled"):
            continue
 
        if proto_filter == "HTTPS only" and not n.get("https_enabled"):
            continue
 
        if proto_filter == "HTTP enabled" and not n.get("http_enabled"):
            continue
 
        ns_rows.append({
            "Name": n.get("name", "—"),
            "Tenant": n.get("tenant", "—"),
            "S3": "✅" if n.get("s3_enabled") else "❌",
            "HTTPS": "✅" if n.get("https_enabled") else "❌",
            "HTTP": "✅" if n.get("http_enabled") else "❌",
            "Versioning": "✅" if n.get("versioning_enabled") else "❌",
            "Replication": "✅" if n.get("replication_enabled") else "❌",
            "Object Lock": str(n.get("s3_objectlock", "—")),
            "DPL": n.get("dpl", "—"),
            "Retention Type": str(n.get("retention_type", "—")),
            "Hard Quota": bytes_to_human(n.get("hard_quota", 0)),
            "Service Plan": n.get("service_plan", "—"),
            "Cloud Optimized": "✅" if n.get("cloud_optimized") else "❌",
            "ACLs": "✅" if n.get("acls_enabled") else "❌",
        })
 
    df_namespaces = pd.DataFrame(ns_rows)
 
    st.dataframe(
        df_namespaces,
        use_container_width=True,
        hide_index=True
    )
 
    # Export CSV
    namespace_csv = io.BytesIO()
 
    df_namespaces.to_csv(
        namespace_csv,
        index=False
    )
 
    st.download_button(
        " Export Namespaces CSV",
        namespace_csv.getvalue(),
        file_name=f"namespaces_{settings.get('clname', 'cluster')}.csv",
        mime="text/csv"
    )
 