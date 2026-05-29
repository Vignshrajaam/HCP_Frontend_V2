import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Access Log Analysis", layout="wide")

from sidebar import render_sidebar, load_access_logs
render_sidebar()

st.markdown("""
<style>
.anomaly-box{background:#fff5f5;border-left:4px solid #e03131;padding:10px 14px;
             border-radius:4px;margin-bottom:6px;font-size:13px}
.ok-box{background:#ebfbee;border-left:4px solid #2f9e44;padding:10px 14px;
        border-radius:4px;margin-bottom:6px;font-size:13px}
.info-box{background:#e8f4fd;border-left:4px solid #1971c2;padding:10px 14px;
          border-radius:4px;margin-bottom:6px;font-size:13px}
</style>
""", unsafe_allow_html=True)

st.title("Access Log Analysis")

# ── guard: config data ────────────────────────────────
if "data" not in st.session_state:
    st.warning("⚠️ No data loaded yet. Please upload an HCP ZIP file.")
    st.info("👈 Use the **Upload HCP ZIP**.")
    st.stop()

data     = st.session_state["data"]
config   = data.get("config", {})
cfgs     = config.get("cluster_cfg", [])
settings = cfgs[0].get("parsed", {}).get("settings", {}) if cfgs else {}
cname    = settings.get("clname", "—")
st.caption(f"{cname} · HTTP gateway request log analysis")

# ── chart helpers ─────────────────────────────────────
def _col(df, preferred, fallback_pos):
    """Return preferred col if present, else column at fallback_pos.
    Handles pandas 1.x vs 2.x value_counts() column naming differences."""
    if preferred in df.columns:
        return preferred
    if fallback_pos < len(df.columns):
        return df.columns[fallback_pos]
    return df.columns[0]

def line_chart(df, x_col, y_col, title, color="#1971c2"):
    """Render a matplotlib line chart inline via st.pyplot."""
    if df is None or df.empty:
        st.info("No data for this chart.")
        return
    x = _col(df, x_col, 0)
    y = _col(df, y_col, 1)
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(df[x], df[y], color=color, linewidth=1.6)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel(x); ax.set_ylabel(y)
    plt.xticks(rotation=35, ha="right", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def bar_chart(df, x_col, y_col, title, color="#339af0", horizontal=False):
    if df is None or df.empty:
        st.info("No data for this chart.")
        return
    # horizontal: x=count(pos 1), y=label(pos 0)
    # vertical:   x=label(pos 0), y=count(pos 1)
    if horizontal:
        x = _col(df, x_col, 1)
        y = _col(df, y_col, 0)
    else:
        x = _col(df, x_col, 0)
        y = _col(df, y_col, 1)
    fig, ax = plt.subplots(figsize=(10, 3.5))
    if horizontal:
        ax.barh(df[y].astype(str), df[x], color=color)
        ax.set_xlabel(x); ax.set_ylabel(y)
    else:
        ax.bar(df[x].astype(str), df[y], color=color)
        ax.set_xlabel(x); ax.set_ylabel(y)
        plt.xticks(rotation=35, ha="right", fontsize=8)
    ax.set_title(title, fontsize=11, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def multi_line_chart(df, x_col, y_col, series_col, title):
    if df is None or df.empty:
        st.info("No data for this chart.")
        return
    try:
        x_col = _col(df, x_col, 0)
        y_col = _col(df, y_col, 2) if len(df.columns) > 2 else _col(df, y_col, 1)
        series_col = _col(df, series_col, 1)
        pivot = df.pivot(index=x_col, columns=series_col, values=y_col)
        fig, ax = plt.subplots(figsize=(10, 4))
        for col in pivot.columns[:12]:
            ax.plot(pivot.index, pivot[col], label=str(col), linewidth=1.3)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.legend(fontsize=7, loc="upper left", ncol=2)
        plt.xticks(rotation=35, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    except Exception as e:
        st.info(f"Could not render chart: {e}")

def stacked_area_chart(df, x_col, y_col, series_col, title):
    if df is None or df.empty:
        st.info("No data for this chart.")
        return
    try:
        x_col = _col(df, x_col, 0)
        y_col = _col(df, y_col, 2) if len(df.columns) > 2 else _col(df, y_col, 1)
        series_col = _col(df, series_col, 1)
        pivot = df.pivot(index=x_col, columns=series_col, values=y_col).fillna(0)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.stackplot(pivot.index, pivot.T, labels=pivot.columns[:12])
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.legend(fontsize=7, loc="upper left", ncol=2)
        plt.xticks(rotation=35, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    except Exception as e:
        st.info(f"Could not render chart: {e}")

def safe_df(fn, *args, **kwargs):
    """Call a service method safely; return empty DataFrame on error."""
    try:
        result = fn(*args, **kwargs)
        return result if result is not None else pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def show_df(df, max_rows=100):
    if df is not None and not df.empty:
        st.dataframe(df.head(max_rows), use_container_width=True, hide_index=True)
    else:
        st.success("No records found.")

# ── load access logs ──────────────────────────────────
st.markdown("---")
col_btn, col_status = st.columns([2, 3])
with col_btn:
    st.markdown("**Load access logs**")
    st.caption("Parses `http_gateway_request.log.*` files from the same ZIP.")
    load_btn = st.button("📂 Parse access logs", type="primary",
                         disabled=not st.session_state.get("file_loaded", False))
with col_status:
    status_slot = st.empty()

if load_btn:
    fb = st.session_state.get("uploaded_file_bytes")
    fn = st.session_state.get("uploaded_file_name", "upload.zip")
    if fb:
        with st.spinner("Extracting and parsing access logs…"):
            try:
                df_logs = load_access_logs(fb, fn)
                if df_logs is not None and not df_logs.empty:
                    if "datetime" in df_logs.columns:
                        df_logs["datetime"] = pd.to_datetime(df_logs["datetime"], errors="coerce")
                    st.session_state["access_logs"]        = df_logs
                    st.session_state["access_logs_loaded"] = True
                    nodes = df_logs["node"].nunique() if "node" in df_logs.columns else "?"
                    status_slot.success(f"✅ {len(df_logs):,} records parsed across {nodes} node(s)")
                else:
                    st.session_state["access_logs_loaded"] = False
                    status_slot.warning("⚠️ No `http_gateway_request.log.*` files found in the ZIP.")
            except Exception as e:
                st.session_state["access_logs_loaded"] = False
                status_slot.error(f"❌ {e}")
    else:
        status_slot.error("Re-upload the ZIP file first.")

if not st.session_state.get("access_logs_loaded", False):
    st.info("Click **Parse access logs** above to begin analysis.")
    st.stop()

df = st.session_state["access_logs"]

from services.hcp_access_log_insights_service import HCPAccessLogInsightsService
from services.anomaly_detection_service import HCPAnomalyDetectionService

ins = HCPAccessLogInsightsService(df)
anom = HCPAnomalyDetectionService(df)

# ── summary metrics ───────────────────────────────────
st.markdown("### Overview")
total    = len(df)
uniq_ip  = df["ip"].nunique()   if "ip"     in df.columns else "—"
uniq_u   = df["user"].nunique() if "user"   in df.columns else "—"
uniq_n   = df["node"].nunique() if "node"   in df.columns else "—"
err_pct  = round(len(df[df["status"].astype(str).str.startswith(("4","5"))]) / total * 100, 1) if total else 0

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Total requests",    f"{total:,}")
m2.metric("Unique client IPs",  uniq_ip)
m3.metric("Unique users",       uniq_u)
m4.metric("Nodes",              uniq_n)
m5.metric("Error rate",         f"{err_pct}%")

st.markdown("---")

# ── tabs ──────────────────────────────────────────────
tabs = st.tabs(["Traffic", "Timeline", "Errors", "Security", "Performance", "Anomalies"])

# ════════════════════════════════════════════════════
# TAB 1 · TRAFFIC (SINGLE COLUMN)
# ════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("Traffic insights")
    
    # Top client IPs
    st.markdown("**Top client IPs**")
    top_ips = safe_df(ins.top_ips)
    bar_chart(top_ips, "requests", "ip", "Top Client IPs", horizontal=True)
    show_df(top_ips)
    
    st.divider()
    
    # Top tenants
    st.markdown("**Top tenants**")
    top_tenants = safe_df(ins.top_tenants)
    bar_chart(top_tenants, "requests", "tenant", "Top Tenants", color="#74c0fc", horizontal=True)
    show_df(top_tenants)
    
    st.divider()
    
    # HTTP methods
    st.markdown("**HTTP methods**")
    top_methods = safe_df(ins.top_methods)
    bar_chart(top_methods, "method", "requests", "HTTP Methods", color="#a9e34b")
    show_df(top_methods)
    
    st.divider()
    
    # Top extensions
    st.markdown("**Top extensions**")
    top_ext = safe_df(ins.top_extensions)
    show_df(top_ext)
    
    st.divider()
    
    # Top users
    st.markdown("**Top users**")
    top_users = safe_df(ins.top_users)
    bar_chart(top_users, "requests", "user", "Top Users", color="#ffa94d", horizontal=True)
    show_df(top_users)
    
    st.divider()
    
    # Top namespaces
    st.markdown("**Top namespaces**")
    top_ns = safe_df(ins.top_namespaces)
    bar_chart(top_ns, "requests", "namespace", "Top Namespaces", color="#f783ac", horizontal=True)
    show_df(top_ns)
    
    st.divider()
    
    # HTTP status codes
    st.markdown("**HTTP status codes**")
    top_sc = safe_df(ins.top_status_codes)
    bar_chart(top_sc, "status", "requests", "Status Codes", color="#cc5de8")
    show_df(top_sc)
    
    st.divider()
    
    # Top tenants by reads (GET) vs writes (PUT)
    st.markdown("**Top tenants by reads (GET) vs writes (PUT)**")
    
    st.markdown("*Reads*")
    reads = safe_df(ins.top_tenants_reads)
    bar_chart(reads, "requests", "tenant", "Top Tenants — Reads", color="#339af0", horizontal=True)
    show_df(reads)
    
    st.markdown("*Writes*")
    writes = safe_df(ins.top_tenants_writes)
    bar_chart(writes, "requests", "tenant", "Top Tenants — Writes", color="#ff6b6b", horizontal=True)
    show_df(writes)
    
    st.divider()
    
    # Top IPs by reads vs writes
    st.markdown("**Top IPs by reads vs writes**")
    
    st.markdown("*Reads*")
    ip_reads = safe_df(ins.top_ips_reads)
    bar_chart(ip_reads, "requests", "ip", "Top IPs — Reads", color="#339af0", horizontal=True)
    show_df(ip_reads)
    
    st.markdown("*Writes*")
    ip_writes = safe_df(ins.top_ips_writes)
    bar_chart(ip_writes, "requests", "ip", "Top IPs — Writes", color="#ff6b6b", horizontal=True)
    show_df(ip_writes)