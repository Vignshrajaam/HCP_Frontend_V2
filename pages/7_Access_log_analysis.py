import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go 
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
    bar_chart(top_ips, "count", "requests", "Top Client IPs", horizontal=True)
    show_df(top_ips)
    
    st.divider()
    
    # Top tenants
    st.markdown("**Top tenants**")
    top_tenants = safe_df(ins.top_tenants)
    bar_chart(top_tenants, "tenant", "requests", "Top Tenants", color="#74c0fc", horizontal=True)
    show_df(top_tenants)
    
    st.divider()
    
    # HTTP methods
    st.markdown("**HTTP methods**")
    top_methods = safe_df(ins.top_methods)
    bar_chart(top_methods, "requests", "method", "HTTP Methods", color="#a9e34b")
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
    bar_chart(top_users, "users", "requests", "Top Users", color="#ffa94d", horizontal=True)
    show_df(top_users)
    
    st.divider()
    
    # Top namespaces
    st.markdown("**Top namespaces**")
    top_ns = safe_df(ins.top_namespaces)
    bar_chart(top_ns, "namespace", "requests", "Top Namespaces", color="#f783ac", horizontal=True)
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
    st.divider()

    # Read / Write Ratio By Tenant

    st.markdown("**Read / write ratio by tenant**")
    rwr = safe_df(ins.read_write_ratio)
    bar_chart(rwr, "read_write_ratio", "tenant", "Read / Write Ratio by Tenant", color="#845ef7", horizontal=True)
    show_df(rwr)
    st.divider()
    
    st.divider()

    st.markdown("**Top response times**")
    top_rt = safe_df(ins.get_top_responsetime)
    show_df(top_rt)

    # Object Size Distribution

    st.markdown("**Object size distribution**")
    osd = safe_df(ins.object_size_distribution)
    bar_chart(osd, "size_bucket", "requests", "Object Size Distribution", color="#f76707")
    show_df(osd)
 
    #  # Export
    # st.divider()
    # buf = io.BytesIO(); df.head(5000).to_csv(buf, index=False)
    # st.download_button("Export log sample CSV (5 000 rows)", buf.getvalue(),
    #                    file_name=f"access_log_{cname}.csv", mime="text/csv")

# ════════════════════════════════════════════════════
# TAB 2 · TIMELINE (SINGLE COLUMN)
# ════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("Timeline insights")
    
    st.markdown("**Requests per day**")
    rpd = safe_df(ins.requests_per_day)
    line_chart(rpd, "day", "requests", "Requests Per Day")
    show_df(rpd)
    
    st.divider()
    
    st.markdown("**Requests per hour**")
    rph = safe_df(ins.requests_per_hour)
    line_chart(rph, "hour", "requests", "Requests Per Hour", color="#2f9e44")
    show_df(rph)
    
    st.divider()
    
    st.markdown("**Errors over time**")
    eot = safe_df(ins.errors_over_time)
    line_chart(eot, "hour", "errors", "Errors Over Time", color="#e03131")
    show_df(eot)
    
    st.divider()
    
    st.markdown("**4xx errors over time**")
    e4 = safe_df(ins.errors_4xx_over_time)
    line_chart(e4, "hour", "errors", "4xx Errors Over Time", color="#f59f00")
    show_df(e4)
    
    st.divider()
    
    st.markdown("**5xx errors over time**")
    e5 = safe_df(ins.errors_5xx_over_time)
    line_chart(e5, "hour", "errors", "5xx Errors Over Time", color="#e03131")
    show_df(e5)
    
    st.divider()
    
    st.markdown("**S3 activity over time**")
    s3 = safe_df(ins.s3_activity_over_time)
    line_chart(s3, "hour", "s3_requests", "S3 Activity Over Time", color="#1971c2")
    show_df(s3)
    
    st.divider()
    
    st.markdown("**REST activity over time**")
    rest = safe_df(ins.rest_activity_over_time)
    line_chart(rest, "hour", "rest_requests", "REST Activity Over Time", color="#5c7cfa")
    show_df(rest)
    
    st.divider()
    
    st.markdown("**DELETE activity over time**")
    da = safe_df(ins.delete_activity_over_time)
    line_chart(da, "hour", "requests", "DELETE Activity Over Time", color="#e03131")
    show_df(da)
    
    st.divider()
    
    st.markdown("**PUT activity over time**")
    pa = safe_df(ins.put_activity_over_time)
    line_chart(pa, "hour", "requests", "PUT Activity Over Time", color="#f59f00")
    show_df(pa)
    
    st.divider()
    
    st.markdown("**Average response time over time**")
    art = safe_df(ins.average_resptime_over_time)
    line_chart(art, "hour", "avg_resptime", "Average Response Time (ms) Over Time", color="#ae3ec9")
    show_df(art)
    
    st.divider()
    
    st.markdown("**After-hours activity** (requests by hour of day)")
    aha = safe_df(ins.after_hours_activity)
    bar_chart(aha, "hour_of_day", "requests", "After-Hours Activity (Hour of Day)", color="#f59f00")
    show_df(aha)
    
    st.divider()
    
    st.markdown("**Requests per node over time**")
    rpn = safe_df(ins.requests_per_node_over_time)
    multi_line_chart(rpn, "hour", "requests", "node", "Requests Per Node Over Time")
    show_df(rpn)
    
    st.divider()
    
    st.markdown("**Tenant activity over time**")
    tat = safe_df(ins.tenant_activity_over_time)
    stacked_area_chart(tat, "hour", "requests", "tenant", "Tenant Activity Over Time")
    show_df(tat)
    
    st.divider()
    
    st.markdown("**Namespace activity over time**")
    nat = safe_df(ins.namespace_activity_over_time)
    stacked_area_chart(nat, "hour", "requests", "namespace", "Namespace Activity Over Time")
    show_df(nat)
    st.divider()
    # # Peak Traffic Hours
    # st.markdown("**Peak traffic hours**")
    # pth = safe_df(ins.peak_traffic_hours)
    
    # bar_chart(pth, "hour", "requests", "Peak Traffic Hours", color="#f76707")
    # show_df(pth)
    # st.divider()
    
    
    # st.markdown("**Peak traffic hours**")
    # pth = safe_df(ins.peak_traffic_hours)

    # if not pth.empty and "hour" in pth.columns:
    #     dt = pd.to_datetime(pth["hour"], errors="coerce")
    #     pth["hour"] = dt  # keep as datetime for smart tick spacing

    #     fig, ax = plt.subplots(figsize=(12, 4))
    #     ax.bar(pth["hour"], pth["requests"], color="#f76707", width=0.015)  # width in days
    #     ax.set_title("Peak Traffic Hours", fontsize=11, fontweight="bold")
    #     ax.set_xlabel("hour")
    #     ax.set_ylabel("requests")

    #     # ✅ Show only ~8 ticks regardless of how many bars exist
    #     ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:00"))

    #     plt.xticks(fontsize=8)
    #     plt.tight_layout()
    #     st.pyplot(fig, use_container_width=True)
    #     plt.close(fig)
    # else:
    #     bar_chart(pth, "hour", "requests", "Peak Traffic Hours", color="#f76707")

    # show_df(pth)
    # st.divider()
    
    st.markdown("**Peak traffic hours**")
    pth = safe_df(ins.peak_traffic_hours)
    if not pth.empty and "hour" in pth.columns:
        dt = pd.to_datetime(pth["hour"], errors="coerce")

        fig = go.Figure(go.Bar(
            x=dt,
            y=pth["requests"],
            marker_color="#f76707",
            customdata=pth["hour"],
            hovertemplate=(
                "<b>%{x|%b %d, %H:%M}</b><br>"
                "Requests: <b>%{y:,}</b><br>"
                "Raw: %{customdata}<extra></extra>"
            )
        ))

        fig.update_layout(
            title=dict(text="Peak Traffic Hours", x=0.5, xanchor="center"),
            xaxis=dict(
                title="Hour",
                tickformat="%b %d\n%H:00",
                nticks=8,
            ),
            yaxis=dict(title="Requests"),
            hoverlabel=dict(bgcolor="white", font_size=12),
            margin=dict(t=40, b=40, l=40, r=20),
            height=380,
            bargap=0.1,
        )

        fig.update_xaxes(
            range=[
                dt.min() - pd.Timedelta(hours=1),
                dt.max() + pd.Timedelta(hours=1)
            ]
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        bar_chart(pth, "hour", "requests", "Peak Traffic Hours", color="#f76707")

    show_df(pth)
    st.divider()

    # Traffic Trend By Tenant
    st.markdown("**Traffic trend by tenant (top 10)**")
    ttt = safe_df(ins.traffic_trend_by_tenant)
    stacked_area_chart(ttt, "hour", "requests", "tenant", "Traffic Trend by Tenant")
    show_df(ttt)

# ════════════════════════════════════════════════════
# TAB 3 · ERRORS (SINGLE COLUMN)
# ════════════════════════════════════════════════════
with tabs[2]:
    st.subheader("Error analysis")
    
    st.markdown("**Top failed paths**")
    fp = safe_df(ins.get_top_failed_paths)
    bar_chart(fp, "path", "failures", "Top Failed Paths", color="#e03131", horizontal=True)
    show_df(fp)
    
    st.divider()
    
    st.markdown("**Top failed tenants**")
    ft = safe_df(ins.get_top_failed_tenants)
    bar_chart(ft, "failures", "count", "Top Failed Tenants", color="#f59f00", horizontal=True)
    show_df(ft)
    
    st.divider()
    
    st.markdown("**Error rate by tenant**")
    ert = safe_df(ins.error_rate_by_tenant)
    show_df(ert)
    
    st.divider()
    
    st.markdown("**Top failing IPs**")
    fi = safe_df(ins.get_top_failed_ips)
    bar_chart(fi, "count", "failures", "Top Failing IPs", color="#ff6b6b", horizontal=True)
    show_df(fi)
    
    st.divider()
    
    st.markdown("**Top 404 objects**")
    o404 = safe_df(ins.top_404_objects)
    show_df(o404)
    
    st.divider()
    
    st.markdown("**Failure percentage**")
    fpc = safe_df(ins.failure_percentage)
    show_df(fpc)
    
    st.divider()
    
    st.markdown("**4xx errors (latest 100)**")
    show_df(safe_df(ins.get_4xx_errors))
    
    st.divider()
    
    st.markdown("**5xx errors (latest 100)**")
    show_df(safe_df(ins.get_5xx_errors))
    
    
    # In tabs[2] (Errors tab), after the "Top failing IPs" block:

st.divider()

st.markdown("**Top users with 403 errors**")
u403 = safe_df(ins.top_403_users)
bar_chart(u403, "403_count", "user", "Top Users with 403 Errors", color="#e03131", horizontal=True)
show_df(u403)

# ════════════════════════════════════════════════════
# TAB 4 · SECURITY (SINGLE COLUMN)
# ════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("Security insights")
    
    st.markdown("**High 403 activity (users)**")
    h403 = safe_df(ins.get_high_403_activity)
    bar_chart(h403, "failures", "user", "High 403 Activity by User", color="#e03131", horizontal=True)
    show_df(h403)
    
    st.divider()
    
    # st.markdown("**Top 403 users**")
    # u403 = safe_df(ins.top_403_users)
    # show_df(u403)
    
    st.divider()
    
    st.markdown("**Suspicious IPs** (≥100 failures)")
    susp = safe_df(ins.get_suspicious_ips)
    if not susp.empty:
        for _, row in susp.iterrows():
            st.markdown(
                f'<div class="anomaly-box">🔴 <strong>{row.get("ip","—")}</strong> — '
                f'{row.get("failures","?")} failed requests</div>',
                unsafe_allow_html=True)
    else:
        st.markdown('<div class="ok-box">✅ No suspicious IPs detected</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("**Failed login patterns**")
    flp = safe_df(ins.get_failed_login_patterns)
    show_df(flp)
    
    st.divider()
    
    st.markdown("**Anonymous access (latest 100)**")
    show_df(safe_df(ins.get_anonymous_access))
    
    st.divider()
    
    st.markdown("**Large uploads (≥100 MB)**")
    lu = safe_df(ins.get_large_uploads)
    show_df(lu)
    
    st.divider()
    
    st.markdown("**Delete operations (latest 100)**")
    show_df(safe_df(ins.get_delete_operations))
    
    st.divider()
    
    st.markdown("**Deletes by tenant**")
    dbt = safe_df(ins.get_delete_by_tenant)
    bar_chart(dbt, "deletes", "tenant", "Deletes by Tenant", color="#e03131", horizontal=True)
    show_df(dbt)
    
    st.divider()
    
    st.markdown("**Deletes by user**")
    dbu = safe_df(ins.get_delete_by_user)
    bar_chart(dbu, "deletes", "user", "Deletes by User", color="#f59f00", horizontal=True)
    show_df(dbu)

# ════════════════════════════════════════════════════
# TAB 5 · PERFORMANCE (SINGLE COLUMN)
# ════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("Performance insights")
    
    avg_rt = safe_df(ins.get_average_response_time)
    if not avg_rt.empty:
        val = avg_rt.iloc[0]["value"]
        st.metric("Average response time (ms)", f"{val:,.1f}")
    
    st.divider()
    
    st.markdown("**Slowest requests (top 100)**")
    show_df(safe_df(ins.get_slowest_requests))
    
    st.divider()
    
    st.markdown("**High latency paths (avg)**")
    hlp = safe_df(ins.get_high_latency_paths)
    bar_chart(hlp, "avg_resptime", "path", "High Latency Paths (avg ms)", color="#ae3ec9", horizontal=True)
    show_df(hlp)
    
    st.divider()
    
    st.markdown("**High latency nodes**")
    hln = safe_df(ins.get_high_latency_nodes)
    bar_chart(hln, "avg_resptime", "node", "High Latency Nodes (avg ms)", color="#e64980", horizontal=True)
    show_df(hln)
    
    st.divider()
    
    st.markdown("**High latency tenants (avg)**")
    hlt = safe_df(ins.get_high_latency_tenants)
    bar_chart(hlt, "avg_resptime", "tenant", "High Latency Tenants (avg ms)", color="#f59f00", horizontal=True)
    show_df(hlt)
    
    st.divider()
    
    st.markdown("**High request volume nodes**")
    hrn = safe_df(ins.get_high_requests_nodes)
    bar_chart(hrn, "requests", "node", "High Request Volume Nodes", color="#2f9e44", horizontal=True)
    show_df(hrn)
    
    st.divider()
    
    st.markdown("**Slow PUTs**")
    show_df(safe_df(ins.slow_puts))
    
    st.divider()
    
    st.markdown("**Slow GETs**")
    show_df(safe_df(ins.slow_gets))

# ════════════════════════════════════════════════════
# TAB 6 · ANOMALIES (SINGLE COLUMN)
# ════════════════════════════════════════════════════
with tabs[5]:
    st.subheader("Anomaly detection")
    st.caption("Spikes detected using a 3× standard-deviation threshold above the hourly mean.")

    ANOMALIES = [
        ("DELETE spikes",         anom.detect_delete_spikes,   "hour",  "requests",    "DELETE Spikes per Hour",            "#e03131"),
        ("Response time spikes",  anom.detect_resptime_spikes, "hour",  "avg_resptime","Response Time Spikes (avg ms/hour)", "#ae3ec9"),
        ("403 burst detection",    anom.detect_403_bursts,      "hour",  "requests",    "403 Bursts per Hour",                "#f59f00"),
        ("REST flood detection",   anom.detect_rest_floods,     "hour",  "requests",    "REST Floods per Hour",               "#1971c2"),
        ("Tenant activity spikes", anom.detect_tenant_spikes,   None,    None,           "Tenant Spikes",                     None),
    ]

    for title, fn, x, y, chart_title, color in ANOMALIES:
        st.markdown(f"**{title}**")
        result = safe_df(fn)
        if not result.empty:
            st.markdown(
                f'<div class="anomaly-box">⚠️ {len(result)} anomalous period(s) detected</div>',
                unsafe_allow_html=True)
            if x and y and color:
                line_chart(result, x, y, chart_title, color=color)
            show_df(result)
        else:
            st.markdown('<div class="ok-box">✅ No anomalies detected</div>', unsafe_allow_html=True)
        st.divider()

    # ── investigation drill-down ──────────────────────
    st.subheader("Investigation drill-down")
    st.caption("Trace activity by IP, user, namespace, or object path.")

    inv_type = st.selectbox("Trace by", ["IP", "User", "Namespace", "Object path"])
    inv_val  = st.text_input(f"Enter {inv_type} value", placeholder="e.g. 10.0.0.5")
    if st.button("▶ Trace", type="primary") and inv_val.strip():
        try:
            if   inv_type == "IP":          result = ins.trace_ip_activity(inv_val)
            elif inv_type == "User":        result = ins.trace_user_activity(inv_val)
            elif inv_type == "Namespace":   result = ins.trace_namespace_activity(inv_val)
            else:                           result = ins.trace_object_activity(inv_val)
            if result is not None and not result.empty:
                st.success(f"{len(result):,} records matched")
                show_df(result)
                buf2 = io.BytesIO(); result.to_csv(buf2, index=False)
                st.download_button("📥 Export CSV", buf2.getvalue(),
                                   file_name=f"trace_{inv_type.lower()}_{inv_val}.csv", mime="text/csv")
            else:
                st.info("No records found for that value.")
        except Exception as e:
            st.error(f"Error: {e}")