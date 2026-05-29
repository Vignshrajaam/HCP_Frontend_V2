import pandas as pd
class HCPConfigurationInsightsService:

    def __init__(self, config_data):

        self.config_data = config_data

    # ---------------------------------
    # Analyze cluster configuration
    # ---------------------------------
    def analyze(self):

        report = {

            "replication_disabled": [],
            "encryption_disabled": [],
            "weak_tls": [],
            "single_node_cluster": []
        }

        cluster_cfgs = self.config_data.get("cluster_cfg", [])

        for cfg in cluster_cfgs:

            parsed = cfg.get("parsed", {})

            settings = parsed.get("settings", {})

            cluster_name = settings.get("clname")

            # ---------------------------------
            # Replication disabled
            # ---------------------------------
            if settings.get("enable_replication", "").lower() != "true":

                report["replication_disabled"].append(cluster_name)

            # ---------------------------------
            # Encryption disabled
            # ---------------------------------
            if settings.get("encryption", "").lower() != "true":

                report["encryption_disabled"].append(cluster_name)

            # ---------------------------------
            # Weak TLS
            # ---------------------------------
            tls = settings.get("minimum_ssl_protocol")

            if tls not in ["TLSv1.2", "TLSv1.3"]:

                report["weak_tls"].append(cluster_name)

            # ---------------------------------
            # Single node cluster
            # ---------------------------------
            if settings.get("single_node", "").lower() == "true":

                report["single_node_cluster"].append(cluster_name)

        return report

    # ---------------------------------
    # Print report
    # ---------------------------------
    def print_report(self, report):

        print("\n🔍 CLUSTER CONFIGURATION INSIGHTS\n")

        # Replication
        if report["replication_disabled"]:

            print("🔴 Clusters with replication disabled")

            for cluster in report["replication_disabled"]:
                print(f"  - {cluster}")

            print()

        # Encryption
        if report["encryption_disabled"]:

            print("🔴 Clusters with encryption disabled")

            for cluster in report["encryption_disabled"]:
                print(f"  - {cluster}")

            print()

        # Weak TLS
        if report["weak_tls"]:

            print("🟡 Clusters using weak TLS")

            for cluster in report["weak_tls"]:
                print(f"  - {cluster}")

            print()

        # Single node
        if report["single_node_cluster"]:

            print("🟡 Single-node clusters detected")

            for cluster in report["single_node_cluster"]:
                print(f"  - {cluster}")

            print()


    # ---------------------------------
    # Print cluster configuration summary
    # ---------------------------------
    def print_cluster_summary(self):

        cluster_cfgs = self.config_data.get("cluster_cfg", [])

        #print(cluster_cfgs)

        print("\n🔧 HCP CLUSTER CONFIGURATION SUMMARY\n")

        for cfg in cluster_cfgs:

            parsed = cfg.get("parsed", {})

            settings = parsed.get("settings", {})
            arc_nodes = parsed.get("arc_nodes", {})
            removed_nodes = parsed.get("removed_nodes", {})

            print(f"Cluster Name            : {settings.get('clname')}")
            print(f"Software Version        : {settings.get('software_version')}")
            print(f"Serial Number           : {settings.get('serial_number')}")

            print()

            print(f"DNS Servers             : {settings.get('dns_servers')}")
            print(f"DNS Enabled             : {settings.get('dns_enabled')}")
            print(f"Gateway                 : {settings.get('gateway')}")

            print()

            print(f"Frontend MTU            : {settings.get('frontend_mtu')}")
            print(f"Backend MTU             : {settings.get('backend_mtu')}")

            print()

            print(f"Timezone                : {settings.get('timezone')}")
            print(f"Time Server             : {settings.get('timeserver')}")

            print()

            print(f"Replication Enabled     : {settings.get('enable_replication')}")
            print(f"Storage Type            : {settings.get('storage_type')}")
            print(f"Zero Copy Failover      : {settings.get('zero_copy_failover')}")

            print()

            print(f"Encryption Enabled      : {settings.get('encryption')}")
            print(f"Encryption Management   : {settings.get('encryption_management')}")
            print(f"Encryption In Flight    : {settings.get('encryption_flight')}")
            print(f"Encryption Cipher       : {settings.get('encryption_cipher')}")
            print(f"Encryption Key Length   : {settings.get('encryption_key_length')}")

            print()

            print(f"Minimum SSL Protocol    : {settings.get('minimum_ssl_protocol')}")

            print()

            print("ARC Nodes:")

            if arc_nodes:

                for node, ip in arc_nodes.items():

                    print(f"  - {node}: {ip}")

            else:

                print("  None")

            print()

            print("Removed Nodes:")

            if removed_nodes:

                for node, ip in removed_nodes.items():

                    print(f"  - {node}: {ip}")

            else:

                print("  None")

            print("\n" + "=" * 70 + "\n")
    # ---------------------------------
    # Get cluster configuration summary
    # ---------------------------------
    def get_cluster_summary(

        self
    ):

        cluster_cfgs = self.config_data.get(

            "cluster_cfg",

            []
        )

        rows = []

        for cfg in cluster_cfgs:

            parsed = cfg.get(

                "parsed",

                {}
            )

            settings = parsed.get(

                "settings",

                {}
            )

            arc_nodes = parsed.get(

                "arc_nodes",

                {}
            )

            removed_nodes = parsed.get(

                "removed_nodes",

                {}
            )

            rows.append({

                "cluster_name":
                    settings.get(
                        "clname"
                    ),

                "software_version":
                    settings.get(
                        "software_version"
                    ),

                "serial_number":
                    settings.get(
                        "serial_number"
                    ),

                "dns_servers":
                    settings.get(
                        "dns_servers"
                    ),

                "dns_enabled":
                    settings.get(
                        "dns_enabled"
                    ),

                "gateway":
                    settings.get(
                        "gateway"
                    ),

                "frontend_mtu":
                    settings.get(
                        "frontend_mtu"
                    ),

                "backend_mtu":
                    settings.get(
                        "backend_mtu"
                    ),

                "timezone":
                    settings.get(
                        "timezone"
                    ),

                "timeserver":
                    settings.get(
                        "timeserver"
                    ),

                "replication_enabled":
                    settings.get(
                        "enable_replication"
                    ),

                "storage_type":
                    settings.get(
                        "storage_type"
                    ),

                "zero_copy_failover":
                    settings.get(
                        "zero_copy_failover"
                    ),

                "encryption":
                    settings.get(
                        "encryption"
                    ),

                "encryption_management":
                    settings.get(
                        "encryption_management"
                    ),

                "encryption_flight":
                    settings.get(
                        "encryption_flight"
                    ),

                "encryption_cipher":
                    settings.get(
                        "encryption_cipher"
                    ),

                "encryption_key_length":
                    settings.get(
                        "encryption_key_length"
                    ),

                "minimum_ssl_protocol":
                    settings.get(
                        "minimum_ssl_protocol"
                    ),

                "arc_nodes":
                    ", ".join(

                        [

                            f"{node}:{ip}"

                            for node, ip in (

                                arc_nodes.items()
                            )
                        ]
                    ),

                "removed_nodes":
                    ", ".join(

                        [

                            f"{node}:{ip}"

                            for node, ip in (

                                removed_nodes.items()
                            )
                        ]
                    )
            })

        return pd.DataFrame(

            rows
        )



    # ---------------------------------
    # Print network summary
    # ---------------------------------
    def print_network_summary(self):

        networks = self.config_data.get("networks", [])

        print("\n🌐 HCP NETWORK SUMMARY\n")

        if not networks:

            print("No network information found\n")
            return

        for net in networks:

            print(f"Network Name          : {net.get('name')}")
            print(f"Domain                : {net.get('domain')}")


            print()

            print(f"Gateway               : {net.get('gateway')}")
            print(f"Subnet                : {net.get('subnet')}")
            print(f"VLAN ID               : {net.get('vlan')}")
            print(f"MTU                   : {net.get('mtu')}")

            print()

            print(f"Enabled               : {net.get('enabled')}")
            print(f"Replication Network   : {net.get('replication_network')}")

            print()

            print(f"DNS Servers           : {net.get('dns_servers')}")
            print(f"DNS Notify            : {net.get('dns_notify')}")
            print(f"DNS Refresh Rate      : {net.get('dns_refresh_rate')}")

            print("\n" + "=" * 70 + "\n")
    

    # ---------------------------------
    # Get network summary
    # ---------------------------------
    def get_network_summary(

        self
    ):

        networks = self.config_data.get(

            "networks",

            []
        )

        rows = []

        for net in networks:

            rows.append({

                "network_name":
                    net.get(
                        "name"
                    ),

                "domain":
                    net.get(
                        "domain"
                    ),

                "gateway":
                    net.get(
                        "gateway"
                    ),

                "subnet":
                    net.get(
                        "subnet"
                    ),

                "vlan_id":
                    net.get(
                        "vlan"
                    ),

                "mtu":
                    net.get(
                        "mtu"
                    ),

                "enabled":
                    net.get(
                        "enabled"
                    ),

                "replication_network":
                    net.get(
                        "replication_network"
                    ),

                "dns_servers":
                    net.get(
                        "dns_servers"
                    ),

                "dns_notify":
                    net.get(
                        "dns_notify"
                    ),

                "dns_refresh_rate":
                    net.get(
                        "dns_refresh_rate"
                    )
            })

        return pd.DataFrame(

            rows
        )


    # ---------------------------------
    # Print bond summary
    # ---------------------------------
    def print_bond_summary(self):

        bonds = self.config_data.get(
            "bond_configuration", []
        )

        print("\n🔗 HCP BOND CONFIGURATION\n")

        if not bonds:

            print("No bond configuration found\n")
            return

        for bond in bonds:

            print(
                f"{bond.get('bond_file')} "
                f"({bond.get('bond_name')})"
            )

            print()

            print(
                f"Bonding Mode         : "
                f"{bond.get('bonding_mode')}"
            )

            if bond.get("hash_policy"):

                print(
                    f"Hash Policy          : "
                    f"{bond.get('hash_policy')}"
                )

            if bond.get("primary_slave"):

                print(
                    f"Primary Slave        : "
                    f"{bond.get('primary_slave')}"
                )

            print()

            for interface in bond.get(
                "interfaces", []
            ):

                print(
                    f"Slave Interface      : "
                    f"{interface.get('interface')}"
                )

                print(
                    f"Speed                : "
                    f"{interface.get('speed')}"
                )

                print()

            print("=" * 70 + "\n")
    
    # ---------------------------------
    # Get bond summary
    # ---------------------------------
    def get_bond_summary(

        self
    ):

        bonds = self.config_data.get(

            "bond_configuration",

            []
        )

        rows = []

        for bond in bonds:

            interfaces = bond.get(

                "interfaces",

                []
            )

            # ---------------------------------
            # No interfaces
            # ---------------------------------
            if not interfaces:

                rows.append({

                    "bond_file":
                        bond.get(
                            "bond_file"
                        ),

                    "bond_name":
                        bond.get(
                            "bond_name"
                        ),

                    "bonding_mode":
                        bond.get(
                            "bonding_mode"
                        ),

                    "hash_policy":
                        bond.get(
                            "hash_policy"
                        ),

                    "primary_slave":
                        bond.get(
                            "primary_slave"
                        ),

                    "slave_interface":
                        None,

                    "speed":
                        None
                })

            # ---------------------------------
            # One row per interface
            # ---------------------------------
            for interface in interfaces:

                rows.append({

                    "bond_file":
                        bond.get(
                            "bond_file"
                        ),

                    "bond_name":
                        bond.get(
                            "bond_name"
                        ),

                    "bonding_mode":
                        bond.get(
                            "bonding_mode"
                        ),

                    "hash_policy":
                        bond.get(
                            "hash_policy"
                        ),

                    "primary_slave":
                        bond.get(
                            "primary_slave"
                        ),

                    "slave_interface":
                        interface.get(
                            "interface"
                        ),

                    "speed":
                        interface.get(
                            "speed"
                        )
                })

        return pd.DataFrame(

            rows
        )


    # ---------------------------------
    # Print JVM status summary
    # ---------------------------------
    def print_jvm_summary(self):

        jvm = self.config_data.get("jvm_status", {})

        print("\n🖥️ HCP JVM STATUS SUMMARY\n")

        if not jvm:

            print("No JVM status information found\n")
            return

        # ---------------------------------
        # Cluster info
        # ---------------------------------
        print(f"Cluster Name           : {jvm.get('cluster_name')}")
        print(f"Map Version            : {jvm.get('map_version')}")
        print(f"Map Size               : {jvm.get('map_size')}")

        print()

        print(f"Map Settled            : {jvm.get('map_settled')}")
        print(f"Map Read Only          : {jvm.get('map_read_only')}")

        print("\n" + "=" * 70)

        # ---------------------------------
        # Nodes
        # ---------------------------------
        print("\n📦 NODE STATUS\n")

        nodes = jvm.get("nodes", [])

        if not nodes:

            print("No node information found")

        else:

            for node in nodes:

                print(
                    f"Node {node['node']} "
                    f"Status={node['status']}"
                )

        print("\n" + "=" * 70)

        # ---------------------------------
        # Capacity metrics
        # ---------------------------------
        print("\n💾 CAPACITY METRICS\n")

        metrics = jvm.get("metrics", {})

        if not metrics:

            print("No capacity metrics found")

        else:

            for key, value in metrics.items():

                print(f"{key:<40} {value}")

        print("\n" + "=" * 70)

        # ---------------------------------
        # Replication links
        # ---------------------------------
        print("\n🔗 REPLICATION LINKS\n")

        links = jvm.get("replication_links", [])

        if not links:

            print("No replication links found")

        else:

            for link in links:

                print(link)

        print("\n" + "=" * 70)

        # ---------------------------------
        # Additional settings
        # ---------------------------------
        print("\n⚙️ ADDITIONAL SETTINGS\n")

        print(f"ZCF Enabled            : {jvm.get('zcf_enabled')}")
        print(
            f"Postgres Auto Vacuum   : "
            f"{jvm.get('postgres_autovacuum')}"
        )

        print("\n" + "=" * 70 + "\n")
    
    # ---------------------------------
    # Get JVM summary
    # ---------------------------------
    def get_jvm_summary(

        self
    ):

        jvm = self.config_data.get(

            "jvm_status",

            {}
        )

        rows = []

        if not jvm:

            return pd.DataFrame()

        # ---------------------------------
        # Flatten Nodes
        # ---------------------------------
        nodes = ", ".join(

            [

                f"Node {node.get('node')} "
                f"Status={node.get('status')}"

                for node in jvm.get(

                    "nodes",

                    []
                )
            ]
        )

        # ---------------------------------
        # Flatten Metrics
        # ---------------------------------
        metrics = ", ".join(

            [

                f"{key}={value}"

                for key, value in (

                    jvm.get(

                        "metrics",

                        {}

                    ).items()
                )
            ]
        )

        # ---------------------------------
        # Flatten Replication Links
        # ---------------------------------
        replication_links = ", ".join(

            [

                str(link)

                for link in jvm.get(

                    "replication_links",

                    []
                )
            ]
        )

        rows.append({

            "cluster_name":
                jvm.get(
                    "cluster_name"
                ),

            "map_version":
                jvm.get(
                    "map_version"
                ),

            "map_size":
                jvm.get(
                    "map_size"
                ),

            "map_settled":
                jvm.get(
                    "map_settled"
                ),

            "map_read_only":
                jvm.get(
                    "map_read_only"
                ),

            "nodes":
                nodes,

            "metrics":
                metrics,

            "replication_links":
                replication_links,

            "zcf_enabled":
                jvm.get(
                    "zcf_enabled"
                ),

            "postgres_autovacuum":
                jvm.get(
                    "postgres_autovacuum"
                )
        })

        return pd.DataFrame(

            rows
        )


    # ---------------------------------
    # Print certificate summary
    # ---------------------------------
    def print_certificate_summary(self):

        certificates = self.config_data.get("certificates", [])

        print("\n🔐 HCP CERTIFICATE SUMMARY\n")

        if not certificates:

            print("No certificates found\n")
            return

        for cert in certificates:

            print(f"Certificate Type      : {cert.get('type')}")
            print(f"Alias                 : {cert.get('alias')}")
            print(f"Subject DN            : {cert.get('subject_dn')}")

            print("\n" + "=" * 70 + "\n")
    
    # ---------------------------------
    # Get certificate summary
    # ---------------------------------
    def get_certificate_summary(

        self
    ):

        certificates = self.config_data.get(

            "certificates",

            []
        )

        rows = []

        for cert in certificates:

            rows.append({

                "certificate_type":
                    cert.get(
                        "type"
                    ),

                "alias":
                    cert.get(
                        "alias"
                    ),

                "subject_dn":
                    cert.get(
                        "subject_dn"
                    )
            })

        return pd.DataFrame(

            rows
        )

    # ---------------------------------
    # Print replication summary
    # ---------------------------------
    def print_replication_summary(self):

        replications = self.config_data.get(
            "replications", []
        )

        print("\n🔄 HCP REPLICATION SUMMARY\n")

        if not replications:

            print("No replication configuration found\n")
            return

        for repl in replications:

            print(f"Link Name             : {repl.get('link_name')}")
            print(f"Link Status           : {repl.get('link_status')}")
            print(f"Link Type             : {repl.get('link_type')}")

            print()

            print(f"Master Cluster        : {repl.get('master_cluster')}")
            print(f"Target Cluster        : {repl.get('target_cluster')}")

            print()

            print(
                f"Replication Algorithm : "
                f"{repl.get('replication_algorithm')}"
            )

            print(
                f"Suspend State         : "
                f"{repl.get('suspend_state')}"
            )

            print()

            print("Replicated Namespaces:")

            tenants = repl.get("tenants", [])

            if not tenants:

                print("  None")

            else:

                for tenant in tenants:

                    tenant_name = tenant.get("tenant")

                    for namespace in tenant.get(
                        "namespaces", []
                    ):

                        print(
                            f"  - {tenant_name} / {namespace}"
                        )

            print("\n" + "=" * 70 + "\n")
    
    # ---------------------------------
    # Get replication summary
    # ---------------------------------
    def get_replication_summary(

        self
    ):

        replications = self.config_data.get(

            "replications",

            []
        )

        rows = []

        for repl in replications:

            replicated_namespaces = []

            tenants = repl.get(

                "tenants",

                []
            )

            for tenant in tenants:

                tenant_name = tenant.get(

                    "tenant"
                )

                for namespace in tenant.get(

                    "namespaces",

                    []
                ):

                    replicated_namespaces.append(

                        f"{tenant_name}/"
                        f"{namespace}"
                    )

            rows.append({

                "link_name":
                    repl.get(
                        "link_name"
                    ),

                "link_status":
                    repl.get(
                        "link_status"
                    ),

                "link_type":
                    repl.get(
                        "link_type"
                    ),

                "master_cluster":
                    repl.get(
                        "master_cluster"
                    ),

                "target_cluster":
                    repl.get(
                        "target_cluster"
                    ),

                "replication_algorithm":
                    repl.get(
                        "replication_algorithm"
                    ),

                "suspend_state":
                    repl.get(
                        "suspend_state"
                    ),

                "replicated_namespaces":
                    ", ".join(

                        replicated_namespaces
                    )
            })

        return pd.DataFrame(

            rows
        )

    # ---------------------------------
    # Print service plan summary
    # ---------------------------------
    def print_service_plan_summary(self):

        plans = self.config_data.get(
            "service_plans", []
        )

        print("\n📦 HCP SERVICE PLAN SUMMARY\n")

        if not plans:

            print("No service plans found\n")
            return

        for plan in plans:

            print(f"Service Plan          : {plan.get('name')}")
            print(f"Description           : {plan.get('description')}")
            print(f"Encryption            : {plan.get('encryption')}")
            print(f"Retired               : {plan.get('retired')}")

            print()

            print("Tiers:")

            for tier in plan.get("tiers", []):

                print(
                    f"  Tier {tier.get('tier_index')}"
                )

                print(
                    f"    Days After Ingest : "
                    f"{tier.get('days_after_ingest')}"
                )

                print(
                    f"    Primary Copies    : "
                    f"{tier.get('current_primary_copies')}"
                )

                print(
                    f"    Rehydrate Time    : "
                    f"{tier.get('rehydrate_time')}"
                )

                print(
                    f"    Replication Before Tiering : "
                    f"{tier.get('replication_before_tiering')}"
                )

                print()

                print("    Pools:")

                for pool in tier.get("pools", []):

                    print(
                        f"      - {pool.get('pool_name')} "
                        f"(Data={pool.get('data_copies')}, "
                        f"Metadata={pool.get('metadata_copies')})"
                    )

                print()

            print("=" * 70 + "\n")
    
    # ---------------------------------
    # Get service plan summary
    # ---------------------------------
    def get_service_plan_summary(

        self
    ):

        plans = self.config_data.get(

            "service_plans",

            []
        )

        rows = []

        for plan in plans:

            tiers = plan.get(

                "tiers",

                []
            )

            # ---------------------------------
            # No tiers
            # ---------------------------------
            if not tiers:

                rows.append({

                    "service_plan":
                        plan.get(
                            "name"
                        ),

                    "description":
                        plan.get(
                            "description"
                        ),

                    "encryption":
                        plan.get(
                            "encryption"
                        ),

                    "retired":
                        plan.get(
                            "retired"
                        ),

                    "tier_index":
                        None,

                    "days_after_ingest":
                        None,

                    "primary_copies":
                        None,

                    "rehydrate_time":
                        None,

                    "replication_before_tiering":
                        None,

                    "pools":
                        None
                })

            # ---------------------------------
            # One row per tier
            # ---------------------------------
            for tier in tiers:

                pools = []

                for pool in tier.get(

                    "pools",

                    []
                ):

                    pools.append(

                        f"{pool.get('pool_name')} "
                        f"(Data={pool.get('data_copies')}, "
                        f"Metadata={pool.get('metadata_copies')})"
                    )

                rows.append({

                    "service_plan":
                        plan.get(
                            "name"
                        ),

                    "description":
                        plan.get(
                            "description"
                        ),

                    "encryption":
                        plan.get(
                            "encryption"
                        ),

                    "retired":
                        plan.get(
                            "retired"
                        ),

                    "tier_index":
                        tier.get(
                            "tier_index"
                        ),

                    "days_after_ingest":
                        tier.get(
                            "days_after_ingest"
                        ),

                    "primary_copies":
                        tier.get(
                            "current_primary_copies"
                        ),

                    "rehydrate_time":
                        tier.get(
                            "rehydrate_time"
                        ),

                    "replication_before_tiering":
                        tier.get(
                            "replication_before_tiering"
                        ),

                    "pools":
                        ", ".join(
                            pools
                        )
                })

        return pd.DataFrame(

            rows
        )

    # ---------------------------------
    # Print tenant summary
    # ---------------------------------
    def print_tenant_summary(self):

        tenants = self.config_data.get(
            "tenants", []
        )

        print("\n👥 HCP TENANT SUMMARY\n")

        if not tenants:

            print("No tenants found\n")
            return

        for tenant in tenants:

            print(f"Tenant Name           : {tenant.get('name')}")

            print()

            print(
                f"Authentication Type   : "
                f"{tenant.get('authentication_types')}"
            )

            print(
                f"Data Network          : "
                f"{tenant.get('data_network')}"
            )

            print(
                f"Management Network    : "
                f"{tenant.get('management_network')}"
            )

            print()

            print(
                f"Hard Quota            : "
                f"{tenant.get('hard_quota')}"
            )

            print(
                f"Namespace Quota       : "
                f"{tenant.get('namespace_quota')}"
            )

            print()

            print(
                f"Replication Enabled   : "
                f"{tenant.get('replication_enabled')}"
            )

            print(
                f"Search Enabled        : "
                f"{tenant.get('search_enabled')}"
            )

            print(
                f"Versioning Enabled    : "
                f"{tenant.get('versioning_enabled')}"
            )

            print(
                f"MAPI Enabled          : "
                f"{tenant.get('mapi_enabled')}"
            )

            print()

            print(
                f"Service Plan          : "
                f"{tenant.get('service_plan')}"
            )

            print("\n" + "=" * 70 + "\n")


    # ---------------------------------
    # Print namespace summary
    # ---------------------------------
    def print_namespace_summary(self):

        namespaces = self.config_data.get(
            "namespaces", []
        )

        print("\n🗂️ HCP NAMESPACE SUMMARY\n")

        if not namespaces:

            print("No namespaces found\n")
            return

        for ns in namespaces:

            print(f"Namespace Name        : {ns.get('name')}")
            print(f"Tenant                : {ns.get('tenant')}")

            print()

            print(
                f"S3 Enabled            : "
                f"{ns.get('s3_enabled')}"
            )

            print(
                f"S3 Objectlock         : "
                f"{ns.get('s3_objectlock')}"
            )

            print(
                f"Replication Enabled   : "
                f"{ns.get('replication_enabled')}"
            )

            print(
                f"Search Enabled        : "
                f"{ns.get('search_enabled')}"
            )

            print()

            print(
                f"Cloud Optimized       : "
                f"{ns.get('cloud_optimized')}"
            )

            print(
                f"DPL                   : "
                f"{ns.get('dpl')}"
            )

            print()

            print(
                f"Retention Default     : "
                f"{ns.get('retention_default')}"
            )

            print(
                f"Retention Type        : "
                f"{ns.get('retention_type')}"
            )
            

            print(
                f"Service Plan          : "
                f"{ns.get('service_plan')}"
            )

            print()

            print(
                f"Versioning Enabled    : "
                f"{ns.get('versioning_enabled')}"
            )

            print(
                f"Versioning Pruning    : "
                f"{ns.get('versioning_pruning_enabled')}"
            )

            print(
                f"Delete Marker         : "
                f"{ns.get('delete_marker')}"
            )

            

            print()

            print(
                f"ACLs Enabled          : "
                f"{ns.get('acls_enabled')}"
            )

            print(
                f"ACLs Honored          : "
                f"{ns.get('acls_honored')}"
            )

            print("\n" + "=" * 70 + "\n")

    # ---------------------------------
    # Print storage component summary
    # ---------------------------------
    def print_storage_component_summary(self):

        components = self.config_data.get(
            "storage_components", []
        )

        print("\n💽 HCP STORAGE COMPONENT SUMMARY\n")

        if not components:

            print("No storage components found\n")
            return

        for comp in components:

            print(f"Name                  : {comp.get('name')}")

            print(
                f"Connection            : "
                f"{comp.get('connection')}"
            )

            print(
                f"Description           : "
                f"{comp.get('description')}"
            )

            print()

            print(
                f"In Use                : "
                f"{comp.get('in_use')}"
            )

            print(
                f"Network               : "
                f"{comp.get('network')}"
            )

            print()

            print(
                f"Free Capacity         : "
                f"{comp.get('free_capacity')}"
            )

            print(
                f"Percent Used          : "
                f"{comp.get('percent_used')}"
            )

            print(
                f"Total Capacity        : "
                f"{comp.get('total_capacity')}"
            )

            print()

            print(
                f"Model Number          : "
                f"{comp.get('model_number')}"
            )

            print(
                f"Software Version      : "
                f"{comp.get('software_version')}"
            )

            print("\n" + "=" * 70 + "\n")
    
    # ---------------------------------
    # Get storage component summary
    # ---------------------------------
    def get_storage_component_summary(

        self
    ):

        components = self.config_data.get(

            "storage_components",

            []
        )

        rows = []

        for comp in components:

            rows.append({

                "name":
                    comp.get(
                        "name"
                    ),

                "connection":
                    comp.get(
                        "connection"
                    ),

                "description":
                    comp.get(
                        "description"
                    ),

                "in_use":
                    comp.get(
                        "in_use"
                    ),

                "network":
                    comp.get(
                        "network"
                    ),

                "free_capacity":
                    comp.get(
                        "free_capacity"
                    ),

                "percent_used":
                    comp.get(
                        "percent_used"
                    ),

                "total_capacity":
                    comp.get(
                        "total_capacity"
                    ),

                "model_number":
                    comp.get(
                        "model_number"
                    ),

                "software_version":
                    comp.get(
                        "software_version"
                    )
            })

        return pd.DataFrame(

            rows
        )


    # ---------------------------------
    # Print storage pool summary
    # ---------------------------------
    def print_storage_pool_summary(self):

        pools = self.config_data.get(
            "storage_pools", []
        )

        print("\n🗄️ HCP STORAGE POOL SUMMARY\n")

        if not pools:

            print("No storage pools found\n")
            return

        for pool in pools:

            print(f"Pool Name             : {pool.get('name')}")

            print(
                f"Availability          : "
                f"{pool.get('availability')}"
            )

            print(
                f"Balancing Enabled     : "
                f"{pool.get('balancing_enabled')}"
            )

            print(
                f"Balancing Complete    : "
                f"{pool.get('balancing_percent_complete')}"
            )

            print(
                f"Balancing Status      : "
                f"{pool.get('balancing_status')}"
            )

            print()

            print(
                f"Compressed            : "
                f"{pool.get('compressed')}"
            )

            print(
                f"Content Verification  : "
                f"{pool.get('content_verification')}"
            )

            print(
                f"In Use                : "
                f"{pool.get('in_use')}"
            )

            print(
                f"Status                : "
                f"{pool.get('status')}"
            )

            print()

            print("Storage Volumes:")

            volumes = pool.get("volumes", [])

            if not volumes:

                print("  None")

            else:

                for vol in volumes:

                    print(
                        f"  - Component         : "
                        f"{vol.get('component_name')}"
                    )

                    print(
                        f"    Distribution      : "
                        f"{vol.get('distribution')}"
                    )

                    print(
                        f"    Volume            : "
                        f"{vol.get('volume')}"
                    )

                    print(
                        f"    Free Capacity     : "
                        f"{vol.get('free_capacity')}"
                    )

                    print(
                        f"    Percent Used      : "
                        f"{vol.get('percent_used')}"
                    )

                    print(
                        f"    Total Capacity    : "
                        f"{vol.get('total_capacity')}"
                    )

                    print()

            print("=" * 70 + "\n")
    # ---------------------------------
    # Get storage pool summary
    # ---------------------------------
    def get_storage_pool_summary(

        self
    ):

        pools = self.config_data.get(

            "storage_pools",

            []
        )

        rows = []

        for pool in pools:

            volumes = pool.get(

                "volumes",

                []
            )

            # ---------------------------------
            # No Volumes
            # ---------------------------------
            if not volumes:

                rows.append({

                    "pool_name":
                        pool.get(
                            "name"
                        ),

                    "availability":
                        pool.get(
                            "availability"
                        ),

                    "balancing_enabled":
                        pool.get(
                            "balancing_enabled"
                        ),

                    "balancing_percent_complete":
                        pool.get(
                            "balancing_percent_complete"
                        ),

                    "balancing_status":
                        pool.get(
                            "balancing_status"
                        ),

                    "compressed":
                        pool.get(
                            "compressed"
                        ),

                    "content_verification":
                        pool.get(
                            "content_verification"
                        ),

                    "in_use":
                        pool.get(
                            "in_use"
                        ),

                    "status":
                        pool.get(
                            "status"
                        ),

                    "component_name":
                        None,

                    "distribution":
                        None,

                    "volume":
                        None,

                    "free_capacity":
                        None,

                    "percent_used":
                        None,

                    "total_capacity":
                        None
                })

            # ---------------------------------
            # One Row Per Volume
            # ---------------------------------
            for vol in volumes:

                rows.append({

                    "pool_name":
                        pool.get(
                            "name"
                        ),

                    "availability":
                        pool.get(
                            "availability"
                        ),

                    "balancing_enabled":
                        pool.get(
                            "balancing_enabled"
                        ),

                    "balancing_percent_complete":
                        pool.get(
                            "balancing_percent_complete"
                        ),

                    "balancing_status":
                        pool.get(
                            "balancing_status"
                        ),

                    "compressed":
                        pool.get(
                            "compressed"
                        ),

                    "content_verification":
                        pool.get(
                            "content_verification"
                        ),

                    "in_use":
                        pool.get(
                            "in_use"
                        ),

                    "status":
                        pool.get(
                            "status"
                        ),

                    "component_name":
                        vol.get(
                            "component_name"
                        ),

                    "distribution":
                        vol.get(
                            "distribution"
                        ),

                    "volume":
                        vol.get(
                            "volume"
                        ),

                    "free_capacity":
                        vol.get(
                            "free_capacity"
                        ),

                    "percent_used":
                        vol.get(
                            "percent_used"
                        ),

                    "total_capacity":
                        vol.get(
                            "total_capacity"
                        )
                })

        return pd.DataFrame(

            rows
        )


    # ---------------------------------
    # Print node summary & BE Switch
    # ---------------------------------
    def print_node_summary(self):

        node_summary = self.config_data.get(
            "nodes",
            {}
        )

        nodes = node_summary.get(
            "nodes",
            []
        )

        backend_switches = node_summary.get(
            "backend_switches",
            []
        )

        print("\n🖥️ HCP NODE SUMMARY\n")

        if not nodes:

            print(
                "No node information found\n"
            )

        else:

            print(

                f"{'Node':<8}"
                f"{'Hardware':<15}"
                f"{'State':<15}"
                f"{'Removed':<10}"
                f"{'Private IP':<18}"
                f"{'System IP':<18}"

            )

            print("-" * 85)

            for node in nodes:

                removed = (
                    "Yes"
                    if str(
                        node.get(
                            "removed"
                        )
                    ).lower() == "true"
                    else "No"
                )

                print(

                    f"{node.get('node_number', '-'):<8}"
                    f"{node.get('hardware_type', '-'):<15}"
                    f"{node.get('state', '-'):<15}"
                    f"{removed:<10}"
                    f"{node.get('private_ip', '-'):<18}"
                    f"{node.get('system_ip', '-'):<18}"

                )

        # ---------------------------------
        # Backend Switch Summary
        # ---------------------------------
        print(
            "\n🔌 BACKEND SWITCH SUMMARY\n"
        )

        if not backend_switches:

            print(
                "No backend switch information found\n"
            )

        else:

            print(

                f"{'Index':<8}"
                f"{'Vendor':<12}"
                f"{'Model':<30}"
                f"{'State':<15}"
                f"{'IP Address':<18}"

            )

            print("-" * 85)

            for switch in backend_switches:

                print(

                    f"{switch.get('index', '-'):<8}"
                    f"{switch.get('vendor', '-'):<12}"
                    f"{switch.get('model', '-'):<30}"
                    f"{switch.get('state', '-'):<15}"
                    f"{switch.get('ip_address', '-'):<18}"

                )

        print("\n" + "=" * 70 + "\n")
    

    # ---------------------------------
    # Get node summary
    # ---------------------------------
    def get_node_summary(

        self
    ):

        node_summary = self.config_data.get(

            "nodes",

            {}
        )

        nodes = node_summary.get(

            "nodes",

            []
        )

        backend_switches = node_summary.get(

            "backend_switches",

            []
        )

        rows = []

        # ---------------------------------
        # Nodes
        # ---------------------------------
        for node in nodes:

            removed = (

                "Yes"

                if str(

                    node.get(
                        "removed"
                    )

                ).lower() == "true"

                else "No"
            )

            rows.append({

                "record_type":
                    "node",

                "node_number":
                    node.get(
                        "node_number"
                    ),

                "hardware_type":
                    node.get(
                        "hardware_type"
                    ),

                "state":
                    node.get(
                        "state"
                    ),

                "removed":
                    removed,

                "private_ip":
                    node.get(
                        "private_ip"
                    ),

                "system_ip":
                    node.get(
                        "system_ip"
                    ),

                "switch_index":
                    None,

                "vendor":
                    None,

                "model":
                    None,

                "switch_state":
                    None,

                "ip_address":
                    None
            })

        # ---------------------------------
        # Backend Switches
        # ---------------------------------
        for switch in backend_switches:

            rows.append({

                "record_type":
                    "backend_switch",

                "node_number":
                    None,

                "hardware_type":
                    None,

                "state":
                    None,

                "removed":
                    None,

                "private_ip":
                    None,

                "system_ip":
                    None,

                "switch_index":
                    switch.get(
                        "index"
                    ),

                "vendor":
                    switch.get(
                        "vendor"
                    ),

                "model":
                    switch.get(
                        "model"
                    ),

                "switch_state":
                    switch.get(
                        "state"
                    ),

                "ip_address":
                    switch.get(
                        "ip_address"
                    )
            })

        return pd.DataFrame(

            rows
        )


    

    # ---------------------------------
    # Print network interface summary
    # ---------------------------------
    def print_network_interface_summary(self):

        interfaces = self.config_data.get(
            "network_interfaces", []
        )

        print("\n🌐 HCP NETWORK INTERFACE SUMMARY\n")

        if not interfaces:

            print("No network interfaces found\n")
            return

        current_network = None

        for interface in interfaces:

            network_name = interface.get(
                "network_name"
            )

            # ---------------------------------
            # New Network Section
            # ---------------------------------
            if network_name != current_network:

                current_network = network_name

                print(
                    "\n"
                    + "=" * 70
                )

                print(
                    f"\nNetwork Name : "
                    f"{network_name}\n"
                )

            # ---------------------------------
            # Interface Details
            # ---------------------------------
            print(
                f"Node        : "
                f"{interface.get('node_number')}"
            )

            print(
                f"IP Address  : "
                f"{interface.get('ip_address')}"
            )

            print(
                f"Gateway     : "
                f"{interface.get('gateway')}"
            )

            print(
                f"MTU         : "
                f"{interface.get('mtu')}"
            )

            print(
                f"VLAN        : "
                f"{interface.get('vlan')}"
            )

            print()

        print("\n" + "=" * 70 + "\n")
    
    # ---------------------------------
    # Get network interface summary
    # ---------------------------------
    def get_network_interface_summary(

        self
    ):

        interfaces = self.config_data.get(

            "network_interfaces",

            []
        )

        rows = []

        for interface in interfaces:

            rows.append({

                "network_name":
                    interface.get(
                        "network_name"
                    ),

                "node_number":
                    interface.get(
                        "node_number"
                    ),

                "ip_address":
                    interface.get(
                        "ip_address"
                    ),

                "gateway":
                    interface.get(
                        "gateway"
                    ),

                "mtu":
                    interface.get(
                        "mtu"
                    ),

                "vlan":
                    interface.get(
                        "vlan"
                    )
            })

        return pd.DataFrame(

            rows
        )


    # ---------------------------------
    # Print physical interface summary
    # ---------------------------------
    def print_physical_interface_summary(self):

        interfaces = self.config_data.get(
            "physical_interfaces",
            []
        )

        print(
            "\n🖧 HCP PHYSICAL INTERFACE SUMMARY\n"
        )

        if not interfaces:

            print(
                "No physical interface data found\n"
            )

            return

        for interface in interfaces:

            print(
                f"{interface.get('interface')} "
                f"================================="
            )

            print(
                f"Supported Ports      : "
                f"{interface.get('supported_ports')}"
            )

            print(
                f"Supported Link Modes :"
            )

            for mode in interface.get(
                "supported_link_modes",
                []
            ):

                print(f"    {mode}")

            print(
                f"Speed                : "
                f"{interface.get('speed')}"
            )

            print(
                f"Port                 : "
                f"{interface.get('port')}"
            )

            print()

        print("\n" + "=" * 70 + "\n")
    
    # ---------------------------------
    # Get physical interface summary
    # ---------------------------------
    def get_physical_interface_summary(

        self
    ):

        interfaces = self.config_data.get(

            "physical_interfaces",

            []
        )

        rows = []

        for interface in interfaces:

            rows.append({

                "interface":
                    interface.get(
                        "interface"
                    ),

                "supported_ports":
                    interface.get(
                        "supported_ports"
                    ),

                "supported_link_modes":
                    ", ".join(

                        interface.get(

                            "supported_link_modes",

                            []
                        )
                    ),

                "speed":
                    interface.get(
                        "speed"
                    ),

                "port":
                    interface.get(
                        "port"
                    )
            })

        return pd.DataFrame(

            rows
        )
