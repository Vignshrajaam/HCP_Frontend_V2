import streamlit as st
import pandas as pd
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Query Engine", layout="wide")

from sidebar import render_sidebar
render_sidebar()

from services.query_engine import NamespaceQueryEngine

st.title("Query Engine")

if "data" not in st.session_state:
    st.warning("⚠️ No data loaded yet. Please upload an HCP ZIP file.")
    st.info("👈 Use the **Upload HCP ZIP**.")
    st.stop()

data       = st.session_state["data"]
config     = data.get("config", {})
cfgs       = config.get("cluster_cfg", [])
settings   = cfgs[0].get("parsed", {}).get("settings", {}) if cfgs else {}
namespaces = data.get("namespaces", [])
qe         = NamespaceQueryEngine(namespaces)

# st.title("Query engine")
st.caption(f"{settings.get('clname', '—')} · {len(namespaces)} namespaces available")

# ── Quick-filter chips ────────────────────────────────
st.markdown("**Quick filters** — click any to instantly populate the query box")

QUICK_FILTERS = [
    ("S3 enabled",       "isS3Enabled=true"),
    ("S3 disabled",      "isS3Enabled=false"),
    ("Versioning on",    "versioningEnabled=true"),
    ("Replication off",  "replicationEnabled=false"),
    ("HTTP enabled",     "isHttpEnabled=true"),
    ("Cloud optimized",  "cloudOptimized=true"),
    ("DPL = 1",          "dpl=1"),
    ("Object lock on",   "s3ObjectLock!=NONE"),
    ("Search enabled",   "searchEnabled=true"),
    ("Delete marker on", "deleteMarkerEnabled=true"),
]

cols = st.columns(5)
for i, (label, q) in enumerate(QUICK_FILTERS):
    if cols[i % 5].button(label, key=f"qf_{i}", use_container_width=True):
        st.session_state["query_text"] = q

# ── Query input ───────────────────────────────────────
st.divider()
col_q, col_run = st.columns([4, 1])
with col_q:
    query_text = st.text_input(
        "Custom query",
        value=st.session_state.get("query_text", ""),
        placeholder="e.g.  replicationEnabled=false and isS3Enabled=true",
        label_visibility="collapsed",
        key="query_text"
    )
with col_run:
    run = st.button("▶ Run", use_container_width=True, type="primary")

# ── Field reference ───────────────────────────────────
with st.expander("📋 Available query fields & examples"):
    st.markdown("""
**Syntax:** `field=value` or `field!=value` · combine with `and`

| Field | Example |
|---|---|
| `replicationEnabled` | `replicationEnabled=false` |
| `isS3Enabled` | `isS3Enabled=true` |
| `versioningEnabled` | `versioningEnabled=true` |
| `cloudOptimized` | `cloudOptimized=false` |
| `dpl` | `dpl=1` |
| `s3ObjectLock` | `s3ObjectLock!=NONE` |
| `searchEnabled` | `searchEnabled=true` |
| `deleteMarkerEnabled` | `deleteMarkerEnabled=true` |
| `isHttpEnabled` | `isHttpEnabled=true` |
| `retentionType` | `retentionType=HCP` |
| `enterpriseMode` | `enterpriseMode=true` |
| `aclsEnabled` | `aclsEnabled=true` |
| `indexingEnabled` | `indexingEnabled=false` |

**Multi-condition:** `dpl=1 and replicationEnabled=false`  
**Negation:** `s3ObjectLock!=NONE`
""")

# ── Run query ─────────────────────────────────────────
if run or query_text:
    if not query_text.strip():
        results = namespaces
        st.info(f"No query — showing all {len(results)} namespaces.")
    else:
        try:
            results = qe.search(query_text)
            if results:
                st.success(f"**{len(results)}** namespace(s) matched `{query_text}`")
            else:
                st.warning(f"No namespaces matched `{query_text}`")
        except Exception as e:
            st.error(f"Query error: {e}")
            results = []

    if results:
        rows = [{
            "Namespace":   r.get("name", "—"),
            "Tenant":      r.get("tenant", "—"),
            "S3":          "✅" if r.get("s3_enabled") else "❌",
            "Versioning":  "✅" if r.get("versioning_enabled") else "❌",
            "Replication": "✅" if r.get("replication_enabled") else "❌",
            "Cloud opt.":  "✅" if r.get("cloud_optimized") else "❌",
            "DPL":         r.get("dpl", "—"),
            "Object lock": r.get("s3_objectlock", "—"),
            "Retention":   r.get("retention_type", "—"),
            "HTTP":        "✅" if r.get("http_enabled") else "❌",
        } for r in results]

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        buf = io.BytesIO()
        df.to_csv(buf, index=False)
        st.download_button(
            " Export results CSV",
            buf.getvalue(),
            file_name=f"query_results_{settings.get('clname', 'cluster')}.csv",
            mime="text/csv"
        )
