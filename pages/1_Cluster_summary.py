import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Cluster Summary", layout="wide")  # MUST be first

from sidebar import render_sidebar
render_sidebar()  # This now hides deploy button + fixes sidebar nav on all pages

st.title("Cluster Summary")

if "data" not in st.session_state:
    st.warning("⚠️ No data loaded yet. Please upload an HCP ZIP file.")
    st.info("👈 Use the **Upload HCP ZIP**.")
    st.stop()

data     = st.session_state["data"]
config   = data.get("config", {})
cfgs     = config.get("cluster_cfg", [])
settings = cfgs[0].get("parsed", {}).get("settings", {}) if cfgs else {}
nodes_raw    = config.get("nodes", {})
nodes        = nodes_raw.get("nodes", []) if isinstance(nodes_raw, dict) else []
active       = [n for n in nodes if str(n.get("removed", "")).lower() != "true"]
be_switches  = nodes_raw.get("backend_switches", []) if isinstance(nodes_raw, dict) else []

# st.title("Cluster Summary")
st.caption(f"{settings.get('clname', '—')} · HCP {settings.get('software_version', '?')}")

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Nodes",      len(active))
m2.metric("Tenants",    len(data.get("tenants", [])))
m3.metric("Namespaces", len(data.get("namespaces", [])))
m4.metric("Version",    settings.get("software_version", "—"))
m5.metric("Serial",     settings.get("serial_number", "—"))
m6.metric("Timezone",   settings.get("timezone", "—"))

st.divider()

with st.expander("Nodes", expanded=True):
    if nodes:
        rows = [{"Node": n.get("node_number", "—"), "Hardware": n.get("hardware_type", "—"),
                 "State": n.get("state", "—"), "Removed": "Yes" if str(n.get("removed", "")).lower() == "true" else "No",
                 "Private IP": n.get("private_ip", "—"), "System IP": n.get("system_ip", "—")} for n in nodes]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No node data.")
    if be_switches:
        st.markdown("**Backend switches**")
        st.dataframe(pd.DataFrame([{"Index": s.get("index"), "Vendor": s.get("vendor"),
            "Model": s.get("model"), "State": s.get("state"), "IP": s.get("ip_address")} for s in be_switches]),
            use_container_width=True, hide_index=True)

with st.expander("Cluster configuration", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**General**")
        for lbl, k in [("Cluster name", "clname"), ("Hostname prefix", "hostname_prefix"),
                       ("Gateway", "gateway"), ("DNS servers", "dns_servers"),
                       ("Timeserver", "timeserver"), ("Timezone", "timezone")]:
            st.markdown(f"**{lbl}:** {settings.get(k, '—')}")
    with col2:
        st.markdown("**Network / storage**")
        for lbl, k in [("Frontend MTU", "frontend_mtu"), ("Backend MTU", "backend_mtu"),
                       ("Storage type", "storage_type"), ("Filesystem", "filesystem"),
                       ("Region map size", "regionmapsize"), ("Max simultaneous nodes", "max_simul_nodes")]:
            st.markdown(f"**{lbl}:** {settings.get(k, '—')}")

with st.expander("Security", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        enc = str(settings.get("encryption", "")).lower()
        enc_flight = str(settings.get("encryption_flight", "")).lower()
        st.markdown(f"**Encryption at rest:** {'✅ Enabled' if enc == 'true' else '❌ Disabled'}")
        st.markdown(f"**Encryption in-flight:** {'✅ Enabled' if enc_flight == 'true' else '❌ Disabled'}")
        st.markdown(f"**Cipher:** {settings.get('encryption_cipher', '—')}")
        st.markdown(f"**Key length:** {settings.get('encryption_key_length', '—')}")
    with col2:
        tls = settings.get("minimum_ssl_protocol", "—")
        repl = str(settings.get("enable_replication", "")).lower()
        lockdown = str(settings.get("lockdown", "")).lower()
        st.markdown(f"**Min TLS:** {'✅' if tls in ('TLSv1.2', 'TLSv1.3') else '⚠️'} {tls}")
        st.markdown(f"**Replication:** {'✅ Enabled' if repl == 'true' else '❌ Disabled'}")
        st.markdown(f"**Lockdown mode:** {'✅ On' if lockdown == 'true' else '⚠️ Off'}")
        st.markdown(f"**Encryption management:** {settings.get('encryption_management', '—')}")

with st.expander("Networks"):
    nets = config.get("networks", [])
    if nets:
        st.dataframe(pd.DataFrame([{"Name": n.get("name"), "Domain": n.get("domain"),
            "Subnet": n.get("subnet"), "Gateway": n.get("gateway"), "VLAN": n.get("vlan"),
            "MTU": n.get("mtu"), "Enabled": n.get("enabled"), "Repl network": n.get("replication_network")} for n in nets]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No network data.")

with st.expander("Network interfaces"):
    ifaces = config.get("network_interfaces", [])
    if ifaces:
        st.dataframe(pd.DataFrame([{"Network": i.get("network_name"), "Node": i.get("node_number"),
            "IP": i.get("ip_address"), "Gateway": i.get("gateway"), "MTU": i.get("mtu"), "VLAN": i.get("vlan")} for i in ifaces]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No interface data.")

with st.expander("Bond configuration"):
    bonds = config.get("bond_configuration", [])
    if bonds:
        rows = []
        for b in bonds:
            for iface in b.get("interfaces", []):
                rows.append({"Bond": b.get("bond_name"), "File": b.get("bond_file"),
                    "Mode": b.get("bonding_mode"), "Interface": iface.get("interface"), "Speed": iface.get("speed")})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No bond data.")

with st.expander("Physical interfaces"):
    phys = config.get("physical_interfaces", [])
    if phys:
        st.dataframe(pd.DataFrame([{"Interface": p.get("interface"), "Speed": p.get("speed"),
            "Port": p.get("port"), "Supported ports": p.get("supported_ports")} for p in phys]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No physical interface data.")

with st.expander("JVM status"):
    jvm = config.get("jvm_status", {})
    if jvm:
        col1, col2 = st.columns(2)
        with col1:
            for lbl, k in [("Cluster", "cluster_name"), ("Map version", "map_version"), ("Map size", "map_size"),
                           ("Map settled", "map_settled"), ("Map read-only", "map_read_only")]:
                st.markdown(f"**{lbl}:** {jvm.get(k, '—')}")
        with col2:
            for lbl, k in [("ZCF enabled", "zcf_enabled"), ("Postgres autovacuum", "postgres_autovacuum")]:
                st.markdown(f"**{lbl}:** {jvm.get(k, '—')}")
        jvm_nodes = jvm.get("nodes", [])
        if jvm_nodes:
            st.dataframe(pd.DataFrame(jvm_nodes), use_container_width=True, hide_index=True)
    else:
        st.info("No JVM data.")

with st.expander("Certificates"):
    certs = config.get("certificates", [])
    if certs:
        st.dataframe(pd.DataFrame([{"Type": c.get("type"), "Alias": c.get("alias"),
            "Subject DN": c.get("subject_dn")} for c in certs]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No certificate data.")

with st.expander("Replication links"):
    repls = config.get("replications", [])
    if repls:
        for r in repls:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Link:** {r.get('link_name', '—')} | **Status:** {r.get('link_status', '—')} | **Type:** {r.get('link_type', '—')}")
            with col2:
                st.markdown(f"**Master:** {r.get('master_cluster', '—')} → **Target:** {r.get('target_cluster', '—')} | **Suspend:** {r.get('suspend_state', '—')}")
            ns_list = [f"{t.get('tenant')}/{ns}" for t in r.get("tenants", []) for ns in t.get("namespaces", [])]
            if ns_list:
                st.caption("Namespaces: " + ", ".join(ns_list))
            st.divider()
    else:
        st.info("No replication configuration.")

with st.expander("Service plans"):
    plans = config.get("service_plans", [])
    if plans:
        st.dataframe(pd.DataFrame([{"Name": p.get("name"), "Encryption": p.get("encryption"),
            "Retired": p.get("retired"), "Tiers": len(p.get("tiers", []))} for p in plans]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No service plans.")

with st.expander("Storage pools"):
    pools = config.get("storage_pools", [])
    if pools:
        st.dataframe(pd.DataFrame([{"Name": p.get("name"), "Status": p.get("status"),
            "In use": p.get("in_use"), "Availability": p.get("availability"),
            "Balancing": p.get("balancing_enabled"), "Compressed": p.get("compressed")} for p in pools]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No storage pool data.")

with st.expander("Storage components"):
    comps = config.get("storage_components", [])
    if comps:
        st.dataframe(pd.DataFrame([{"Name": c.get("name"), "In use": c.get("in_use"),
            "Total": c.get("total_capacity"), "Free": c.get("free_capacity"),
            "% used": c.get("percent_used"), "Model": c.get("model_number")} for c in comps]),
            use_container_width=True, hide_index=True)
    else:
        st.info("No storage components.")