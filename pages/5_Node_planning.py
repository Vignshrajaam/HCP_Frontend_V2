# import streamlit as st
# import pandas as pd
# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent.parent))

# st.set_page_config(page_title="Node Addition Planning", layout="wide")

# from sidebar import render_sidebar
# render_sidebar()

# from services.hcp_techrefresh_service import HCPTechRefreshService
# from services.hcp_node_addition_service import HCPNodeAdditionService

# st.title("Node Addition Planning")

# if "data" not in st.session_state:
#     st.warning("⚠️ No data loaded yet. Please upload an HCP ZIP file.")
#     st.info("👈 Use the **Upload HCP ZIP**.")
#     st.stop()

# data     = st.session_state["data"]
# config   = data.get("config", {})
# cfgs     = config.get("cluster_cfg", [])
# settings = cfgs[0].get("parsed", {}).get("settings", {}) if cfgs else {}

# tr_svc  = HCPTechRefreshService(config)
# profile = tr_svc.collect_cluster_profile()

# # st.title("Node planning")
# st.caption(f"{settings.get('clname', '—')} · Tech refresh & node addition wizard")

# # ── Current cluster profile ──────────────────────────
# with st.expander("🛠️ Current cluster profile", expanded=True):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("**Cluster**")
#         st.markdown(f"**Architecture:** {profile.get('cluster_architecture', '—')}")
#         st.markdown(f"**Storage type:** {profile.get('storage_type', '—')}")
#         st.markdown(f"**Software version:** {profile.get('software_version', '—')}")
#         st.markdown(f"**Node count:** {profile.get('node_count', '—')}")
#         st.markdown(f"**Node models:** {', '.join(profile.get('node_models', []))}")
#     with col2:
#         st.markdown("**Map / JVM**")
#         st.markdown(f"**Map version:** {profile.get('map_version', '—')}")
#         st.markdown(f"**Region count:** {profile.get('map_size', '—')}")
#         st.markdown(f"**FE bond mode:** {profile.get('fe_bond_mode', '—')}")
#         st.markdown(f"**BE bond mode:** {profile.get('be_bond_mode', '—')}")

#     node_details = profile.get("node_details", [])
#     if node_details:
#         st.markdown("**Node details**")
#         st.dataframe(pd.DataFrame(node_details), use_container_width=True, hide_index=True)

#     col_fe, col_be = st.columns(2)
#     with col_fe:
#         fe_ports = profile.get("fe_ports", [])
#         if fe_ports:
#             st.markdown("**Front-end ports**")
#             st.dataframe(pd.DataFrame(fe_ports), use_container_width=True, hide_index=True)
#     with col_be:
#         be_ports = profile.get("be_ports", [])
#         if be_ports:
#             st.markdown("**Back-end ports**")
#             st.dataframe(pd.DataFrame(be_ports), use_container_width=True, hide_index=True)

#     networks = profile.get("networks", [])
#     if networks:
#         st.markdown("**Network interfaces**")
#         grouped = {}
#         for n in networks:
#             grouped.setdefault(n.get("network_name", "—"), []).append(n)
#         for net_name, entries in grouped.items():
#             st.caption(f"Network: {net_name}")
#             st.dataframe(pd.DataFrame(entries), use_container_width=True, hide_index=True)

# st.divider()

# # ── Node addition wizard ────────────────────────────
# st.subheader("Node addition wizard")

# col1, col2 = st.columns(2)
# with col1:
#     node_count = st.number_input(
#         "Number of nodes to add",
#         min_value=2, max_value=10, value=2, step=2,
#         help="Must be an even number"
#     )
#     node_model = st.selectbox("Node model", ["HCP G11", "HCP O12"])
# with col2:
#     if node_model == "HCP G11":
#         st.info("HCP G11 supports 10G SFP+ only.")
#         switch_speed = "10G"
#         st.markdown("**NIC speed:** 10G SFP+")
#     else:
#         speed_choice = st.selectbox("NIC card port speed", ["10G SFP+", "25G SFP+"])
#         switch_speed = "10G" if "10G" in speed_choice else "25G"

# run_validation = st.button("▶ Run validation", type="primary")

# if run_validation:
#     if node_count % 2 != 0:
#         st.error("Node count must be an even number.")
#         st.stop()

#     if switch_speed == "10G":
#         expected_be_port = {"supported_ports": "[ FIBRE ]", "speed": "10000Mb/s", "port": "Direct Attach Copper"}
#     else:
#         expected_be_port = {"supported_ports": "[ FIBRE ]", "speed": "25000Mb/s", "port": "Direct Attach Copper"}

#     validations    = []
#     existing_models  = profile.get("node_models", [])
#     existing_version = str(profile.get("software_version", ""))
#     be_ports         = profile.get("be_ports", [])

#     # Check 1: G10 + O12 mix
#     if "HCP G10" in existing_models and node_model == "HCP O12":
#         validations.append({"status": "FAILED",  "message": "Cannot mix HCP G10 and HCP O12 nodes"})
#     else:
#         validations.append({"status": "PASSED",  "message": "Node model mix validation passed"})

#     # Check 2: Recommended version
#     if existing_version != "10.0.1.4":
#         validations.append({"status": "WARNING", "message": f"Recommended version for node addition is 10.0.1.4 (current: {existing_version})"})
#     else:
#         validations.append({"status": "PASSED",  "message": "HCP version validation passed (10.0.1.4)"})

#     # Check 3: O12 needs 10.x
#     if node_model == "HCP O12":
#         if not existing_version.startswith("10."):
#             validations.append({"status": "WARNING", "message": "Cluster must be on HCP 10.x to add O12 nodes"})
#         else:
#             validations.append({"status": "PASSED",  "message": "HCP version supports O12 nodes"})

#     # Check 4: BE port validation
#     for port in be_ports:
#         iface = port.get("interface", "—")
#         ex_ports = str(port.get("supported_ports", "")).strip()
#         ex_speed = str(port.get("speed", "")).strip()
#         ex_port  = str(port.get("port", "")).strip()
#         if ex_ports != expected_be_port["supported_ports"]:
#             validations.append({"status": "FAILED",  "message": f"{iface}: supported ports mismatch"})
#         elif ex_speed != expected_be_port["speed"]:
#             validations.append({"status": "WARNING", "message": f"{iface}: speed mismatch — existing={ex_speed}, required={expected_be_port['speed']}"})
#         elif ex_port != expected_be_port["port"]:
#             validations.append({"status": "WARNING", "message": f"{iface}: port type mismatch — existing={ex_port}"})
#         else:
#             validations.append({"status": "PASSED",  "message": f"{iface}: backend NIC matches expected configuration"})

#     if not be_ports:
#         validations.append({"status": "INFO", "message": "No back-end port data available for validation"})

#     st.markdown("### Validation results")
#     icon_map   = {"PASSED": "✅", "WARNING": "⚠️", "FAILED": "❌", "INFO": "ℹ️"}
#     color_map  = {"PASSED": "#ebfbee", "WARNING": "#fff9db", "FAILED": "#fff5f5", "INFO": "#e8f4fd"}
#     border_map = {"PASSED": "#2f9e44", "WARNING": "#f59f00", "FAILED": "#e03131", "INFO": "#1971c2"}

#     for v in validations:
#         vs = v["status"]
#         st.markdown(
#             f'<div style="background:{color_map.get(vs,"#f8f9fa")};border-left:4px solid {border_map.get(vs,"#adb5bd")};'
#             f'padding:8px 14px;border-radius:4px;margin-bottom:6px;font-size:13px">'
#             f'{icon_map.get(vs,"⚪")} {v["message"]}</div>',
#             unsafe_allow_html=True
#         )

#     failed = [v for v in validations if v["status"] == "FAILED"]
#     if not failed:
#         st.divider()
#         st.markdown("### Projected cluster profile")

#         existing_nodes   = list(profile.get("node_details", []))
#         existing_numbers = [int(n.get("node_number", 0)) for n in existing_nodes if str(n.get("node_number", "")).isdigit()]
#         last_node        = max(existing_numbers) if existing_numbers else 100

#         new_nodes = existing_nodes + [
#             {"node_number": str(last_node + i + 1), "hardware_type": node_model, "private_ip": "TO_BE_ASSIGNED"}
#             for i in range(node_count)
#         ]

#         new_total = profile.get("node_count", 0) + node_count
#         if   2 <= new_total <= 4: rec_map = 64
#         elif 5 <= new_total <= 8: rec_map = 128
#         elif new_total >= 9:      rec_map = 256
#         else:                     rec_map = 32

#         cp1, cp2 = st.columns(2)
#         cp1.metric("Projected node count", new_total)
#         cp2.metric("Recommended region map size", rec_map,
#                    delta=f"current: {profile.get('map_size', '?')}", delta_color="off")
#         st.dataframe(pd.DataFrame(new_nodes), use_container_width=True, hide_index=True)
#     else:
#         st.error(f"{len(failed)} validation(s) failed — review findings above before proceeding.")
