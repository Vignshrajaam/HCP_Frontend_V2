import streamlit as st
from pathlib import Path
import zipfile
import tarfile
import tempfile
# archive_utils imported inside load_access_logs to keep sidebar fast
import os
import sys

sys.path.insert(0, str(Path(__file__).parent))
from services.hcp_data_service import HCPDataService


@st.cache_data(show_spinner="Parsing HCP configuration data…")
def load_hcp_data(file_bytes, filename):

    with tempfile.TemporaryDirectory() as tmpdir:

        tmp_zip = os.path.join(tmpdir, filename)

        with open(tmp_zip, "wb") as f:
            f.write(file_bytes)

        with zipfile.ZipFile(tmp_zip, "r") as z:
            z.extractall(tmpdir)

        node_archives = sorted([
            os.path.join(r, fn)
            for r, _, files in os.walk(tmpdir)
            for fn in files
            if fn.endswith(".tar") or fn.endswith(".tar.xz")
        ])

        if node_archives:

            first = node_archives[0]

            node_dir = os.path.join(
                tmpdir,
                Path(first).stem
            )

            os.makedirs(node_dir, exist_ok=True)

            with tarfile.open(first, "r:*") as t:
                t.extractall(node_dir)

        svc = HCPDataService(tmpdir)

        data = svc.gather_all()

    return data


@st.cache_data(show_spinner="Parsing access logs (this may take a moment)…")
def load_access_logs(file_bytes, filename):
    """
    Separate cached loader for access logs.
    Uses recursive archive extraction so deeply nested
    access log tarballs are found.
    """

    from utils.archive_utils import extract_all_archives_recursive

    with tempfile.TemporaryDirectory() as tmpdir:

        tmp_zip = os.path.join(tmpdir, filename)

        with open(tmp_zip, "wb") as f:
            f.write(file_bytes)

        # Full recursive extraction
        extract_all_archives_recursive(
            tmp_zip,
            tmpdir
        )

        svc = HCPDataService(tmpdir)

        data = svc.gather_all(
            include_access_logs=True
        )

    return data.get("access_logs")


def load_css():
    """Load custom CSS."""

    css_path = Path(__file__).parent / "styles.css"

    if css_path.exists():

        try:

            with open(css_path, "r", encoding="utf-8") as f:

                st.markdown(
                    f"<style>{f.read()}</style>",
                    unsafe_allow_html=True
                )

        except Exception:
            pass


def render_sidebar():

    load_css()

    st.markdown(
        """
        <style>

        /* Sidebar top spacing */
        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        /* Logo spacing */
        .stImage {
            margin-bottom: -1rem;
        }

        /* Divider spacing */
        hr {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Navigation spacing */
        .stPageLink {
            margin-top: -0.3rem !important;
            margin-bottom: -0.3rem !important;
        }

        /* Markdown spacing */
        .stMarkdown {
            margin-top: -0.5rem;
        }

        /* Upload status styling */
        .upload-status-box {
            padding: 10px;
            border-radius: 8px;
            margin-top: 7px;
            font-size: 15px;
        }

        /* Hide dataframe toolbar */
        [data-testid="stDataFrameToolbar"] {
            display: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:

        # LOGO
        logo_path = (
            Path(__file__).parent
            / "static"
            / "HV-Logo.png"
        )

        if logo_path.exists() and logo_path.is_file():

            st.image(
                str(logo_path),
                use_container_width=True
            )

        # TITLE
        st.markdown(
            '<div style="text-align:center; padding:25px 0 5px;">'
            '<span style="font-size:16px;font-weight:700;color:#1a1a1a;">'
            'HCP SmartAnalytics'
            '</span><br>'
            '<span style="font-size:12px;color:#888;">'
            'V2.0'
            '</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        # NAVIGATION
        st.page_link(
            "app.py",
            label=" Home"
        )

        st.divider()

        st.page_link(
            "pages/1_Cluster_summary.py",
            label="1 · Cluster summary"
        )

        st.page_link(
            "pages/2_Config_insights.py",
            label="2 · Config insights"
        )

        st.page_link(
            "pages/3_Tenants_namespaces.py",
            label="3 · Tenants & namespaces"
        )

        st.page_link(
            "pages/4_Namespace_insights.py",
            label="4 · Namespace insights"
        )

        st.page_link(
            "pages/5_Node_planning.py",
            label="5 · Node Addition Planning"
        )

        st.page_link(
            "pages/6_Query_engine.py",
            label="6 · Query engine"
        )

        st.page_link(
            "pages/7_Access_log_analysis.py",
            label="7 · Access log analysis"
        )

        st.divider()

        # FILE UPLOAD
        st.markdown("**📁 Upload HCP ZIP**")

        uploaded = st.file_uploader(
            "Upload HCP ZIP",
            type=["zip"],
            label_visibility="collapsed"
        )

        status_slot = st.empty()

        # NEW FILE UPLOADED
        if uploaded:

            try:

                data = load_hcp_data(
                    uploaded.getvalue(),
                    uploaded.name
                )

                st.session_state["data"] = data

                st.session_state["uploaded_file_bytes"] = (
                    uploaded.getvalue()
                )

                st.session_state["uploaded_file_name"] = (
                    uploaded.name
                )

                # Reset access logs
                st.session_state.pop(
                    "access_logs",
                    None
                )

                st.session_state["access_logs_loaded"] = False

                config = data.get("config", {})
                cfgs = config.get("cluster_cfg", [])

                if cfgs:

                    s = (
                        cfgs[0]
                        .get("parsed", {})
                        .get("settings", {})
                    )

                    cname = s.get(
                        "clname",
                        Path(uploaded.name).stem
                    )

                    ver = s.get(
                        "software_version",
                        "?"
                    )

                else:

                    cname = Path(uploaded.name).stem
                    ver = "?"

                st.session_state.update({
                    "cluster_name": cname,
                    "version": ver,
                    "file_loaded": True,
                    "file_name": uploaded.name,
                })

                # SUCCESS MESSAGE
                status_slot.markdown(
                    (
                        '<div class="upload-status-box" '
                        'style="background:#f0fdf4; border:1px solid #bbf7d0;">'
                        '✅ <strong>Loaded</strong><br>'
                        f'<span style="color:#555; font-size:11px; '
                        f'word-break:break-all;">{uploaded.name}</span>'
                        '</div>'
                    ),
                    unsafe_allow_html=True,
                )

            except Exception as e:

                st.session_state.pop("data", None)

                st.session_state["file_loaded"] = False

                # ERROR MESSAGE
                status_slot.markdown(
                    (
                        '<div class="upload-status-box" '
                        'style="background:#fef2f2; border:1px solid #fecaca;">'
                        '❌ <strong>Parse error</strong><br>'
                        f'<span style="color:#555; font-size:11px; '
                        f'word-break:break-all;">{str(e)}</span>'
                        '</div>'
                    ),
                    unsafe_allow_html=True,
                )

        # EXISTING FILE IN SESSION
        elif st.session_state.get("file_loaded", False):

            file_name = st.session_state.get(
                "file_name",
                ""
            )

            status_slot.markdown(
                (
                    '<div class="upload-status-box" '
                    'style="background:#f0fdf4; border:1px solid #bbf7d0;">'
                    '✅ <strong>Loaded</strong><br>'
                    f'<span style="color:#555; font-size:11px; '
                    f'word-break:break-all;">{file_name}</span>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

        # EMPTY STATE
        else:

            status_slot.markdown(
                (
                    '<div class="upload-status-box" '
                    'style="background:transparent; border:none;">'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )