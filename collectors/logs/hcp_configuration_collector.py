from pathlib import Path
import configparser
import ast
import xml.etree.ElementTree as ET


class HCPConfigurationCollector:

    def __init__(self, base_path):

        self.base_path = Path(base_path)

    # ---------------------------------
    # Parse cluster.cfg
    # ---------------------------------
    def parse_cluster_cfg(self, file_path):

        parser = configparser.ConfigParser()

        try:

            parser.read(file_path)

            config_data = {}

            for section in parser.sections():

                config_data[section] = {}

                for key, value in parser.items(section):

                    config_data[section][key] = value

            return config_data

        except Exception as e:

            print(f"Error parsing {file_path}: {e}")

            return {}

    # ---------------------------------
    # Main collector
    # ---------------------------------
    def collect(self):

        return {

            "cluster_cfg": self.collect_cluster_cfg(),
            "networks": self.collect_networks(),
            "bond_configuration": self.collect_bond_configuration(),
            "jvm_status": self.collect_jvm_status(),
            "certificates": self.collect_certificates(),
            "replications": self.collect_replication(),
            "service_plans": self.collect_service_plans(),
            "tenants": self.collect_tenants(),
            "namespaces": self.collect_namespaces(),
            "storage_components": self.collect_storage_components(),
            "storage_pools": self.collect_storage_pools(),
            "nodes": self.collect_node_summary(),
            "physical_interfaces": self.collect_physical_interface_summary(),
            "network_interfaces": self.collect_network_interface_summary(),
            
                        
        }
    
    # ---------------------------------
    # Collect cluster.cfg
    # ---------------------------------
    def collect_cluster_cfg(self):

        cluster_configs = []

        print("\n🔍 Searching for cluster.cfg ...")

        for cluster_cfg in self.base_path.rglob("cluster.cfg"):

            print(f"📄 Found cluster.cfg: {cluster_cfg}")

            parsed_config = self.parse_cluster_cfg(cluster_cfg)

            cluster_configs.append({

                "file": str(cluster_cfg),

                "parsed": parsed_config
            })

            # cluster.cfg is cluster-wide
            # one copy is enough
            break

        return cluster_configs

    # ---------------------------------
    # Collect network-list.txt
    # ---------------------------------
    def collect_networks(self):

        networks = []

        print("\n🔍 Searching for network-list.txt ...")

        for network_file in self.base_path.rglob("network-list.txt"):

            print(f"📄 Found network-list.txt: {network_file}")

            parsed = self.parse_hcp_file(network_file)

            for uuid, net in parsed.items():

                networks.append({

                    "uuid": uuid,

                    "name": net.get("networkName"),

                    "domain": net.get("domain"),

                    "dns_notify": net.get("dnsNotify"),

                    "dns_refresh_rate": net.get("dnsRefreshRate"),

                    "subnet": net.get("subnets"),

                    "gateway": net.get("gateways"),

                    "mtu": net.get("mtu"),

                    "vlan": net.get("vlanID"),

                    "enabled": net.get("enabled"),

                    "replication_network": (
                        net.get("isReplicationNetwork")
                    ),

                    "dns_servers": net.get("dnsServers"),

                    # raw full data
                    "raw": net
                })

            # one copy enough
            break

        return networks


    # ---------------------------------
    # Read text file
    # ---------------------------------
    def read_text_file(self, file_path):

        try:

            with open(file_path, "r", errors="ignore") as f:

                return f.read()

        except Exception as e:

            print(f"Error reading {file_path}: {e}")

            return None


    # ---------------------------------
    # Parse HCP key-value file
    # ---------------------------------
    def parse_hcp_file(self, file_path):

        try:

            with open(file_path, "r", errors="ignore") as f:

                content = f.read()

            return ast.literal_eval(content)

        except Exception as e:

            print(f"Error parsing {file_path}: {e}")

            return {}

    # ---------------------------------
    # Collect bond configuration
    # ---------------------------------
    def collect_bond_configuration(self):

        bonds = []

        bond_files = {

            "bond0": "Front-End",

            "bond1": "Back-End"
        }

        print("\n🔍 Searching for bond files ...")

        for bond_file, bond_name in bond_files.items():

            for file_path in self.base_path.rglob(bond_file):

                print(f"📄 Found {bond_file}: {file_path}")

                try:

                    with open(
                        file_path,
                        "r",
                        errors="ignore"
                    ) as f:

                        lines = f.readlines()

                    bond_data = {

                        "bond_name": bond_name,

                        "bond_file": bond_file,

                        "bonding_mode": None,

                        "hash_policy": None,

                        "primary_slave": None,

                        "interfaces": []
                    }

                    current_interface = None

                    for line in lines:

                        line = line.strip()

                        # Bonding Mode
                        if line.startswith(
                            "Bonding Mode:"
                        ):

                            bond_data[
                                "bonding_mode"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

                        # Hash Policy
                        elif line.startswith(
                            "Transmit Hash Policy:"
                        ):

                            bond_data[
                                "hash_policy"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

                        # Primary Slave
                        elif line.startswith(
                            "Primary Slave:"
                        ):

                            bond_data[
                                "primary_slave"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

                        # Slave Interface
                        elif line.startswith(
                            "Slave Interface:"
                        ):

                            current_interface = {

                                "interface": line.split(
                                    ":", 1
                                )[1].strip(),

                                "speed": None
                            }

                            bond_data[
                                "interfaces"
                            ].append(
                                current_interface
                            )

                        # Speed
                        elif (
                            line.startswith("Speed:")
                            and current_interface
                        ):

                            current_interface[
                                "speed"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

                    bonds.append(bond_data)

                except Exception as e:

                    print(
                        f"Error parsing {bond_file}: {e}"
                    )

                # one copy enough
                break

        return bonds


    
    # ---------------------------------
    # Collect JVM status
    # ---------------------------------
    def collect_jvm_status(self):

        import re

        result = {

            "cluster_name": None,

            "map_version": None,
            "map_size": None,

            "map_settled": None,
            "map_read_only": None,

            "nodes": [],

            "metrics": {},

            "replication_links": [],

            "zcf_enabled": None,

            "postgres_autovacuum": None
        }

        print("\n🔍 Searching for jvm-status.txt ...")

        for status_file in self.base_path.rglob("jvm-status.txt"):

            print(f"📄 Found jvm-status.txt: {status_file}")

            try:

                with open(status_file, "r", errors="ignore") as f:

                    lines = f.readlines()

                for line in lines:

                    line = line.strip()

                    # ---------------------------------
                    # Cluster
                    # ---------------------------------
                    if line.startswith("Cluster:"):

                        result["cluster_name"] = (
                            line.split(":", 1)[1].strip()
                        )

                    # ---------------------------------
                    # Map version
                    # ---------------------------------
                    elif line.startswith("Map Version:"):

                        match = re.search(
                            r"Map Version:\s*(\S+), map size:\s*(\S+)",
                            line
                        )

                        if match:

                            result["map_version"] = match.group(1)

                            result["map_size"] = match.group(2)

                    # ---------------------------------
                    # Map state
                    # ---------------------------------
                    elif line.startswith("mapSettled:"):

                        result["map_settled"] = (
                            "true" in line.lower()
                        )

                    elif line.startswith("mapReadOnly:"):

                        result["map_read_only"] = (
                            "true" in line.lower()
                        )

                    # ---------------------------------
                    # Node state
                    # ---------------------------------
                    elif line.startswith("Node:"):

                        match = re.search(

                            r"Node:\s*(\d+).*Status:\s*(\S+)",

                            line
                        )

                        if match:

                            result["nodes"].append({

                                "node": match.group(1),

                                "status": match.group(2)
                            })

                    # ---------------------------------
                    # Capacity / archive metrics
                    # ---------------------------------
                    elif any(

                        metric in line for metric in [

                            "Archived Files",
                            "Indexed Files",

                            "Archive Total Size",
                            "Archive Physical Used",
                            "Archive Logical Used",

                            "Archive Active License Capacity",
                            "Archive Extended License Capacity",

                            "Archive Active Used Capacity",
                            "Archive Extended Used Capacity"
                        ]
                    ):

                        key, value = line.split(":", 1)

                        result["metrics"][key.strip()] = value.strip()

                    # ---------------------------------
                    # Replication links
                    # ---------------------------------
                    elif line.startswith("Link Name:"):

                        result["replication_links"].append(line)

                    # ---------------------------------
                    # ZCF
                    # ---------------------------------
                    elif line.startswith("ZCF enabled:"):

                        result["zcf_enabled"] = (
                            "true" in line.lower()
                        )

                    # ---------------------------------
                    # Postgres autovacuum
                    # ---------------------------------
                    elif line.startswith("Postgres auto-vacuum:"):

                        result["postgres_autovacuum"] = (
                            "true" in line.lower()
                        )

            except Exception as e:

                print(f"Error parsing jvm-status.txt: {e}")

            # one file enough
            break

        return result

    # ---------------------------------
    # Collect certificates
    # ---------------------------------
    def collect_certificates(self):

        import ast

        certificates = []

        print("\n🔍 Searching for certificate-list.txt ...")

        for cert_file in self.base_path.rglob("certificate-list.txt"):

            print(f"📄 Found certificate-list.txt: {cert_file}")

            try:

                with open(cert_file, "r", errors="ignore") as f:

                    lines = f.readlines()

                current_section = None

                collecting = False

                brace_count = 0

                block_lines = []

                valid_sections = [

                    "SERVER",
                    "STORAGE",
                    "KEYSTONE",
                    "REPLICATION",
                    "ACTIVE DIRECTORY",
                    "STORAGE ACCOUNT"
                ]

                for line in lines:

                    stripped = line.strip()

                    # Skip blank lines
                    if not stripped:
                        continue

                    # Detect section
                    if stripped in valid_sections:

                        current_section = stripped
                        continue

                    # Start block
                    if stripped == "{":

                        collecting = True
                        brace_count = 1
                        block_lines = ["{"]

                        continue

                    # Collect lines
                    if collecting:

                        block_lines.append(line)

                        brace_count += line.count("{")
                        brace_count -= line.count("}")

                        # Finished full dictionary
                        if brace_count == 0:

                            collecting = False

                            try:

                                parsed = ast.literal_eval(
                                    "".join(block_lines)
                                )

                                for uuid, cert in parsed.items():

                                    certificates.append({

                                        "type": current_section,

                                        "alias": cert.get("alias"),

                                        "subject_dn": cert.get("subjectDN"),

                                        "raw": cert
                                    })

                            except Exception as e:

                                print(
                                    f"Error parsing certificate block: {e}"
                                )

                            block_lines = []

            except Exception as e:

                print(f"Error reading certificates: {e}")

            # one file enough
            break

        return certificates


    # ---------------------------------
    # Collect replication configuration
    # ---------------------------------
    def collect_replication(self):

        import ast

        replications = []

        print("\n🔍 Searching for replication-list.txt ...")

        for repl_file in self.base_path.rglob("replication-list.txt"):

            print(f"📄 Found replication-list.txt: {repl_file}")

            try:

                parsed = self.parse_hcp_file(repl_file)

                for uuid, repl in parsed.items():

                    tenants = []

                    tenant_cfg = (
                        repl.get("tenantNamespaceSelections", {})
                            .get("tenantLinkConfig", {})
                    )

                    for tenant_uuid, tenant_data in tenant_cfg.items():

                        tenant_name = tenant_data.get("name")

                        namespaces = []

                        ns_cfg = tenant_data.get(
                            "namespaceLinkConfig", {}
                        )

                        for ns_uuid, ns_data in ns_cfg.items():

                            namespaces.append(
                                ns_data.get("name")
                            )

                        tenants.append({

                            "tenant": tenant_name,

                            "namespaces": namespaces
                        })

                    replications.append({

                        "link_name": repl.get("linkName"),

                        "link_status": repl.get("linkStatus"),

                        "link_type": repl.get("linkType"),

                        "master_cluster": repl.get(
                            "masterClusterName"
                        ),

                        "target_cluster": repl.get(
                            "nonMasterClusterName"
                        ),

                        "replication_algorithm": repl.get(
                            "replicationAlgorithm"
                        ),

                        "suspend_state": repl.get(
                            "suspendState"
                        ),

                        "tenants": tenants,

                        "raw": repl
                    })

            except Exception as e:

                print(f"Error parsing replication-list.txt: {e}")

            # one file enough
            break

        return replications


    # ---------------------------------
    # Collect service plans
    # ---------------------------------
    def collect_service_plans(self):

        service_plans = []

        print("\n🔍 Searching for servicePlan-list.txt ...")

        for sp_file in self.base_path.rglob("servicePlan-list.txt"):

            print(f"📄 Found servicePlan-list.txt: {sp_file}")

            try:

                parsed = self.parse_hcp_file(sp_file)

                for plan_name, plan in parsed.items():

                    tiers_summary = []

                    for tier in plan.get("tiers", []):

                        pools_summary = []

                        for pool_uuid, pool in tier.get(
                            "pools", {}
                        ).items():

                            pools_summary.append({

                                "pool_name": pool.get("name"),

                                "data_copies": pool.get(
                                    "dataCopies"
                                ),

                                "metadata_copies": pool.get(
                                    "metadataCopies"
                                )
                            })

                        tiers_summary.append({

                            "tier_index": tier.get(
                                "tierIndex"
                            ),

                            "days_after_ingest": tier.get(
                                "daysAfterIngest"
                            ),

                            "current_primary_copies": tier.get(
                                "currentPrimaryCopies"
                            ),

                            "rehydrate_time": tier.get(
                                "rehydrateTime"
                            ),

                            "replication_before_tiering": tier.get(
                                "replicationBeforeTiering"
                            ),

                            "pools": pools_summary
                        })

                    service_plans.append({

                        "name": plan.get("name"),

                        "description": plan.get(
                            "description"
                        ),

                        "encryption": plan.get(
                            "encryption"
                        ),

                        "retired": plan.get(
                            "retired"
                        ),

                        "tiers": tiers_summary,

                        "raw": plan
                    })

            except Exception as e:

                print(f"Error parsing servicePlan-list.txt: {e}")

            # one file enough
            break

        return service_plans


    # ---------------------------------
    # Collect tenants
    # ---------------------------------
    def collect_tenants(self):

        tenants = []

        print("\n🔍 Searching for tenant-list.txt ...")

        for tenant_file in self.base_path.rglob("tenant-list.txt"):

            print(f"📄 Found tenant-list.txt: {tenant_file}")

            try:

                parsed = self.parse_hcp_file(tenant_file)

                for uuid, tenant in parsed.items():

                    tenants.append({

                        # ---------------------------------
                        # Identity
                        # ---------------------------------
                        "uuid":
                        uuid,

                        "name":
                        tenant.get("name"),

                        "description":
                        tenant.get(
                            "description"
                        ),

                        "state":
                        tenant.get("state"),

                        # ---------------------------------
                        # Authentication
                        # ---------------------------------
                        "authentication_types":
                        tenant.get(
                            "authenticationTypes"
                        ),

                        # ---------------------------------
                        # Networks
                        # ---------------------------------
                        "data_network":
                        tenant.get(
                            "dataNetwork"
                        ),

                        "management_network":
                        tenant.get(
                            "managementNetwork"
                        ),

                        # ---------------------------------
                        # Quotas
                        # ---------------------------------
                        "hard_quota":
                        tenant.get(
                            "hardQuota"
                        ),

                        "namespace_quota":
                        tenant.get(
                            "namespaceQuota"
                        ),

                        # ---------------------------------
                        # Features
                        # ---------------------------------
                        "replication_enabled":
                        tenant.get(
                            "isReplicationEnabled"
                        ),

                        "search_enabled":
                        tenant.get(
                            "isSearchEnabled"
                        ),

                        "versioning_enabled":
                        tenant.get(
                            "isVersioningEnabled"
                        ),

                        "mapi_enabled":
                        tenant.get(
                            "mapiEnabled"
                        ),

                        # ---------------------------------
                        # Service Plan
                        # ---------------------------------
                        "service_plan":
                        tenant.get(
                            "servicePlanEffective"
                        ),

                        # ---------------------------------
                        # Protocols
                        # ---------------------------------
                        "http_enabled":
                        tenant.get(
                            "isHttpEnabled"
                        ),

                        "https_enabled":
                        tenant.get(
                            "isHttpsEnabled"
                        ),

                        "s3_enabled":
                        tenant.get(
                            "isS3Enabled"
                        ),

                        "nfs_enabled":
                        tenant.get(
                            "isNfsEnabled"
                        ),

                        "cifs_enabled":
                        tenant.get(
                            "isCifsEnabled"
                        ),

                        # ---------------------------------
                        # RAW
                        # ---------------------------------
                        "raw":
                        tenant
                    })

            except Exception as e:

                print(f"Error parsing tenant-list.txt: {e}")

            # one file enough
            break

        return tenants

    # ---------------------------------
    # Collect namespaces
    # ---------------------------------
    def collect_namespaces(self):

        namespaces = []

        print("\n🔍 Searching for namespace-list.txt ...")

        for ns_file in self.base_path.rglob("namespace-list.txt"):

            print(f"📄 Found namespace-list.txt: {ns_file}")

            try:

                parsed = self.parse_hcp_file(ns_file)

                for uuid, ns in parsed.items():

                    namespaces.append({

                            # ---------------------------------
                            # Identity
                            # ---------------------------------
                            "uuid":
                            uuid,

                            "name":
                            ns.get("name"),

                            "tenant":
                            ns.get(
                                "namespace.tenant"
                            ),

                            "owner":
                            ns.get("owner"),

                            "state":
                            ns.get("state"),

                            # ---------------------------------
                            # Protocols
                            # ---------------------------------
                            "s3_enabled":
                            ns.get(
                                "isS3Enabled"
                            ),

                            "http_enabled":
                            ns.get(
                                "isHttpEnabled"
                            ),

                            "https_enabled":
                            ns.get(
                                "isHttpsEnabled"
                            ),

                            "nfs_enabled":
                            ns.get(
                                "isNfsEnabled"
                            ),

                            "cifs_enabled":
                            ns.get(
                                "isCifsEnabled"
                            ),

                            "webdav_enabled":
                            ns.get(
                                "isWebdavEnabled"
                            ),

                            # ---------------------------------
                            # Compliance / Governance
                            # ---------------------------------
                            "retention_type":
                            ns.get(
                                "retentionType"
                            ),

                            "retention_default":
                            ns.get(
                                "retentionDefault"
                            ),

                            "s3_objectlock":
                            ns.get(
                                "s3ObjectLock"
                            ),

                            "delete_marker":
                            ns.get(
                                "deleteMarkerEnabled"
                            ),

                            # ---------------------------------
                            # Protection
                            # ---------------------------------
                            "replication_enabled":
                            ns.get(
                                "replicationEnabled"
                            ),

                            "dpl":
                            ns.get("dpl"),

                            "versioning_enabled":
                            ns.get(
                                "versioningEnabled"
                            ),

                            "versioning_pruning_enabled":
                            ns.get(
                                "versioningPruningEnabled"
                            ),

                            # ---------------------------------
                            # Search / Metadata
                            # ---------------------------------
                            "search_enabled":
                            ns.get(
                                "searchEnabled"
                            ),

                            "indexing_enabled":
                            ns.get(
                                "indexingEnabled"
                            ),

                            "custom_metadata_indexing_enabled":
                            ns.get(
                                "customMetadataIndexingEnabled"
                            ),

                            "custom_metadata_fulltext_enabled":
                            ns.get(
                                "customMetadataFullTextIndexingEnabled"
                            ),

                            # ---------------------------------
                            # Cloud / Modern App
                            # ---------------------------------
                            "cloud_optimized":
                            ns.get(
                                "cloudOptimized"
                            ),

                            "enterprise_mode":
                            ns.get(
                                "enterpriseMode"
                            ),

                            "allow_erasure_coding":
                            ns.get(
                                "allowErasureCoding"
                            ),

                            # ---------------------------------
                            # ACL / Security
                            # ---------------------------------
                            "acls_enabled":
                            ns.get(
                                "aclsEnabled"
                            ),

                            "acls_honored":
                            ns.get(
                                "aclsHonored"
                            ),

                            "allow_permission_changes":
                            ns.get(
                                "allowPermissionAndOwnershipChanges"
                            ),

                            # ---------------------------------
                            # Quotas / Capacity
                            # ---------------------------------
                            "soft_quota":
                            ns.get(
                                "softQuota"
                            ),

                            "hard_quota":
                            ns.get(
                                "hardQuota"
                            ),

                            # ---------------------------------
                            # Service Plan
                            # ---------------------------------
                            "service_plan":
                            ns.get(
                                "servicePlan"
                            ),

                            "service_plan_effective":
                            ns.get(
                                "servicePlanEffective"
                            ),

                            # ---------------------------------
                            # Additional
                            # ---------------------------------
                            "description":
                            ns.get(
                                "description"
                            ),

                            "tags":
                            ns.get("tags"),

                            # ---------------------------------
                            # RAW
                            # ---------------------------------
                            "raw":
                            ns
                    })

            except Exception as e:

                print(f"Error parsing namespace-list.txt: {e}")

            # one file enough
            break

        return namespaces

    # ---------------------------------
    # Collect storage components
    # ---------------------------------
    def collect_storage_components(self):

        components = []

        print("\n🔍 Searching for StorageComponent-list.txt ...")

        for sc_file in self.base_path.rglob(
            "StorageComponent-list.txt"
        ):

            print(f"📄 Found StorageComponent-list.txt: {sc_file}")

            try:

                parsed = self.parse_hcp_file(sc_file)

                for uuid, comp in parsed.items():

                    properties = comp.get(
                        "properties", {}
                    )

                    metrics = properties.get(
                        "metrics", {}
                    )

                    components.append({

                        "connection": comp.get(
                            "connection"
                        ),

                        "description": comp.get(
                            "description"
                        ),

                        "in_use": comp.get(
                            "inUse"
                        ),

                        "name": comp.get(
                            "name"
                        ),

                        "network": comp.get(
                            "network"
                        ),

                        "free_capacity": metrics.get(
                            "freeCapacity"
                        ),

                        "percent_used": metrics.get(
                            "percentUsed"
                        ),

                        "total_capacity": metrics.get(
                            "totalCapacity"
                        ),

                        "model_number": properties.get(
                            "modelNumber"
                        ),

                        "software_version": properties.get(
                            "softwareVersion"
                        ),

                        "raw": comp
                    })

            except Exception as e:

                print(
                    f"Error parsing StorageComponent-list.txt: {e}"
                )

            # one file enough
            break

        return components


    # ---------------------------------
    # Collect storage pools
    # ---------------------------------
    def collect_storage_pools(self):

        pools = []

        print("\n🔍 Searching for StoragePool-list.txt ...")

        for pool_file in self.base_path.rglob(
            "StoragePool-list.txt"
        ):

            print(f"📄 Found StoragePool-list.txt: {pool_file}")

            try:

                parsed = self.parse_hcp_file(pool_file)

                for uuid, pool in parsed.items():

                    volumes = []

                    storage_volumes = pool.get(
                        "storageVolumes", {}
                    )

                    for vol_uuid, vol in storage_volumes.items():

                        metrics = vol.get(
                            "componentMetrics", {}
                        )

                        volumes.append({

                            "component_name": vol.get(
                                "componentName"
                            ),

                            "distribution": vol.get(
                                "distribution"
                            ),

                            "volume": vol.get(
                                "volume"
                            ),

                            "free_capacity": metrics.get(
                                "freeCapacity"
                            ),

                            "percent_used": metrics.get(
                                "percentUsed"
                            ),

                            "total_capacity": metrics.get(
                                "totalCapacity"
                            )
                        })

                    pools.append({

                        "name": pool.get(
                            "name"
                        ),

                        "availability": pool.get(
                            "availability"
                        ),

                        "balancing_enabled": pool.get(
                            "balancingEnabled"
                        ),

                        "balancing_percent_complete": pool.get(
                            "balancingPercentComplete"
                        ),

                        "balancing_status": pool.get(
                            "balancingStatus"
                        ),

                        "compressed": pool.get(
                            "compressed"
                        ),

                        "content_verification": pool.get(
                            "contentVerification"
                        ),

                        "description": pool.get(
                            "description"
                        ),

                        "in_use": pool.get(
                            "inUse"
                        ),

                        "status": pool.get(
                            "status"
                        ),

                        "volumes": volumes,

                        "raw": pool
                    })

            except Exception as e:

                print(
                    f"Error parsing StoragePool-list.txt: {e}"
                )

            # one file enough
            break

        return pools

    # ---------------------------------
    # Collect node summary & BE Switch 
    # ---------------------------------

    def collect_node_summary(self):
        
        import xml.etree.ElementTree as ET

        nodes = []

        backend_switches = []

        print("\n🔍 Searching for getAdminView.xml ...")

        for xml_file in self.base_path.rglob(
            "getAdminView.xml"
        ):

            print(f"📄 Found getAdminView.xml: {xml_file}")

            try:

                tree = ET.parse(xml_file)

                root = tree.getroot()

                # ---------------------------------
                # Collect Node Details
                # ---------------------------------
                for node in root.findall("node"):

                    private_ip = "-"

                    private_elem = node.find(
                        "privateIpAddress"
                    )

                    if private_elem is not None:

                        private_ip = private_elem.attrib.get(
                            "hostAddress"
                        )

                    system_ip = "-"

                    system_elem = node.find(
                        "systemIpv4Address"
                    )

                    if system_elem is not None:

                        system_ip = system_elem.attrib.get(
                            "hostAddress"
                        )

                    nodes.append({

                        "node_number": node.attrib.get(
                            "nodeNumber"
                        ),

                        "hardware_type": (
                            node.attrib.get(
                                "nodeHardwareType"
                            )
                            or
                            node.attrib.get(
                                "nodeModel"
                            )
                        ),

                        "state": node.attrib.get(
                            "stateString"
                        ),

                        "removed": node.attrib.get(
                            "removed"
                        ),

                        "private_ip": private_ip,

                        "system_ip": system_ip,

                        "raw": node.attrib
                    })


                # ---------------------------------
                # Collect Backend Switch Details
                # ---------------------------------
                for elem in root.iter():

                    tag = elem.tag.split(
                        "}"
                    )[-1]

                    if tag == "backendSwitch":

                        backend_switch = {}

                        for child in elem:

                            child_tag = (
                                child.tag.split(
                                    "}"
                                )[-1]
                            )

                            backend_switch[
                                child_tag
                            ] = child.text

                        backend_switches.append({

                            "index":
                            backend_switch.get(
                                "index",
                                "-"
                            ),

                            "ip_address":
                            backend_switch.get(
                                "ipAddress",
                                "-"
                            ),

                            "model":
                            backend_switch.get(
                                "model",
                                "-"
                            ),

                            "vendor":
                            backend_switch.get(
                                "vendor",
                                "-"
                            ),

                            "state":
                            backend_switch.get(
                                "state",
                                "-"
                            )
                        })
                        
            except Exception as e:

                print(
                    f"Error parsing getAdminView.xml: {e}"
                )

            # one file enough
            break

        return {

            "nodes": nodes,

            "backend_switches": backend_switches
        }


    # ---------------------------------
    # Collect physical interface summary
    # ---------------------------------
    def collect_physical_interface_summary(self):

        interfaces = []

        print("\n🔍 Searching for ethtool ...")

        for file_path in self.base_path.rglob(
            "ethtool"
        ):

            print(
                f"📄 Found ethtool: "
                f"{file_path}"
            )

            try:

                current_interface = None

                with open(
                    file_path,
                    "r",
                    errors="ignore"
                ) as f:

                    for line in f:

                        line = line.strip()

                        # ---------------------------------
                        # Interface start
                        # Example:
                        # Settings for eth2::
                        # ---------------------------------
                        if line.startswith(
                            "Settings for"
                        ):

                            interface_name = (
                                line.replace(
                                    "Settings for",
                                    ""
                                )
                                .replace(":", "")
                                .strip()
                            )

                            # Only collect eth0-eth3
                            if interface_name not in [
                                "eth0",
                                "eth1",
                                "eth2",
                                "eth3"
                            ]:

                                current_interface = None

                                continue

                            current_interface = {

                                "interface": interface_name,

                                "supported_ports": None,

                                "supported_link_modes": [],

                                "speed": None,

                                "port": None
                            }

                            interfaces.append(
                                current_interface
                            )

                        
                        # ---------------------------------
                        # Supported Ports
                        # ---------------------------------
                        elif (
                            current_interface
                            and line.lower().startswith(
                                "supported ports:"
                            )
                        ):

                            current_interface[
                                "supported_ports"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

                        # ---------------------------------
                        # Supported Link Modes
                        # ---------------------------------
                        elif (
                            current_interface
                            and line.startswith(
                                "Supported link modes:"
                            )
                        ):

                            mode = line.split(
                                ":", 1
                            )[1].strip()

                            if (
                                mode
                                and mode not in current_interface[
                                    "supported_link_modes"
                                ]
                            ):

                                current_interface[
                                    "supported_link_modes"
                                ].append(mode)

                        # Continuation lines
                        elif (
                            current_interface
                            and (
                                "baseT/" in line
                                or "baseSR/" in line
                                or "baseCR/" in line
                            )
                        ):

                            mode = line.strip()

                            # Skip advertised modes
                            if (
                                "Advertised"
                                in mode
                            ):

                                continue

                            if (
                                mode
                                not in current_interface[
                                    "supported_link_modes"
                                ]
                            ):

                                current_interface[
                                    "supported_link_modes"
                                ].append(mode)

                        # ---------------------------------
                        # Speed
                        # ---------------------------------
                        elif (
                            current_interface
                            and line.startswith(
                                "Speed:"
                            )
                        ):

                            current_interface[
                                "speed"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

                        
                        # ---------------------------------
                        # Port
                        # ---------------------------------
                        elif (
                            current_interface
                            and line.lower().startswith(
                                "port:"
                            )
                        ):
                            
                            current_interface[
                                "port"
                            ] = line.split(
                                ":", 1
                            )[1].strip()

            except Exception as e:

                print(
                    f"Error parsing ethtool: {e}"
                )

            # one file enough
            break

        return interfaces


    # ---------------------------------
    # Collect network interface summary
    # ---------------------------------
    def collect_network_interface_summary(self):

        interfaces = []

        print("\n🔍 Searching for networks.txt ...")

        for file_path in self.base_path.rglob(
            "networks.txt"
        ):

            print(
                f"📄 Found networks.txt: "
                f"{file_path}"
            )

            try:

                with open(
                    file_path,
                    "r",
                    errors="ignore"
                ) as f:

                    for line in f:

                        line = line.strip()

                        # Skip comments
                        if (
                            not line
                            or line.startswith("#")
                            or line.startswith("%")
                        ):

                            continue

                        parts = line.split()

                        # Expected network line
                        if len(parts) < 15:

                            continue

                        interfaces.append({

                            "node_number": parts[0],

                            "node_name": parts[1],

                            "network_name": parts[2],

                            "domain": parts[4],

                            "vlan": parts[5],

                            "ip_address": parts[6],

                            "gateway": parts[7],

                            "multicast": parts[8],

                            "mtu": parts[9],

                            "enabled": parts[10],

                            "uuid": parts[11],

                            "replication_network": parts[12]
                        })

            except Exception as e:

                print(
                    f"Error parsing networks.txt: {e}"
                )

            # one file enough
            break

        return interfaces
