import pandas as pd
class HCPConfigurationAnalysisService:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(self, config_data):

        self.config_data = config_data

    # ---------------------------------
    # Analyze cluster health
    # ---------------------------------
    def analyze_cluster_health(self):

        findings = []

        # =================================
        # Cluster CFG Checks
        # =================================
        cluster_cfg = self.config_data.get(
            "cluster_cfg", []
        )

        if cluster_cfg:

            parsed = cluster_cfg[0].get(
                "parsed", {}
            )

            settings = parsed.get(
                "settings", {}
            )

            # -----------------------------
            # DNS Check
            # -----------------------------
            dns_servers = str(
                settings.get(
                    "dns_servers", ""
                )
            )

            dns_count = len([

                x.strip()

                for x in dns_servers.split(",")

                if x.strip()

            ])

            if dns_count <= 1:

                findings.append({

                    "severity": "WARNING",

                    "category": "CLUSTER",

                    "message":
                        "Only one DNS server configured",

                    "details":
                        dns_servers
                })

            # -----------------------------
            # NTP Check
            # -----------------------------
            ntp = str(
                settings.get(
                    "timeserver", ""
                )
            )

            ntp_count = len([

                x.strip()

                for x in ntp.split(",")

                if x.strip()

            ])

            if ntp_count <= 1:

                findings.append({

                    "severity": "WARNING",

                    "category": "CLUSTER",

                    "message":
                        "Only one NTP server configured",

                    "details":
                        ntp
                })

            # -----------------------------
            # TLS Check
            # -----------------------------
            tls = str(
                settings.get(
                    "minimum_ssl_protocol",
                    ""
                )
            )

            if tls != "TLSv1.3":

                findings.append({

                    "severity": "WARNING",

                    "category": "SECURITY",

                    "message":
                        "TLSv1.3 not enforced",

                    "details":
                        f"Configured={tls}"
                })
            # -----------------------------
            # Encryption Checks
            # -----------------------------
            encryption = str(
                settings.get(
                    "encryption", ""
                )
            ).lower()

            encryption_flight = str(
                settings.get(
                    "encryption_flight", ""
                )
            ).lower()

            # DARE
            if encryption == "true":

                findings.append({

                    "severity": "INFO",

                    "category": "SECURITY",

                    "message":
                        "DARE encryption enabled",

                    "details":
                        (
                            "Encryption enabled "
                            "on Primary Running Pool"
                        )
                })

            else:

                findings.append({

                    "severity": "WARNING",

                    "category": "SECURITY",

                    "message":
                        "DARE encryption disabled"
                })

            # DIFE
            if encryption_flight == "true":

                findings.append({

                    "severity": "INFO",

                    "category": "SECURITY",

                    "message":
                        "DIFE encryption enabled"
                })

            else:

                findings.append({

                    "severity": "WARNING",

                    "category": "SECURITY",

                    "message":
                        "DIFE encryption disabled"
                })

        # =================================
        # JVM STATUS CHECKS
        # =================================
        jvm = self.config_data.get(
            "jvm_status", {}
        )

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

        active_nodes = [

            n for n in nodes

            if str(
                n.get("removed")
            ).lower() != "true"
        ]

        node_count = len(active_nodes)

        actual_map_size = int(
            jvm.get(
                "map_size", 0
            )
        )

        expected_map_size = None

        if node_count == 1:

            expected_map_size = 32

        elif 2 <= node_count <= 4:

            expected_map_size = 64

        elif 5 <= node_count <= 8:

            expected_map_size = 128

        elif 9 <= node_count <= 16:

            expected_map_size = 256

        elif node_count >= 17:

            expected_map_size = 256

        if (
            expected_map_size
            and
            actual_map_size != expected_map_size
        ):

            findings.append({

                "severity": "WARNING",

                "category": "JVM",

                "message":
                    "Unexpected map size configured",

                "details":
                    f"Nodes={node_count}, "
                    f"Expected={expected_map_size}, "
                    f"Configured={actual_map_size}"
            })

        # =================================
        # CERTIFICATE CHECKS
        # =================================
        certificates = self.config_data.get(
            "certificates", []
        )

        default_cert_keywords = [

            "OU=HCP",

            "O=Hitachi",

            "L=Waltham",

            "ST=Massachusetts",

            "C=US"
        ]

        for cert in certificates:

            subject = str(
                cert.get("subject_dn", "")
            )

            if all(

                keyword in subject

                for keyword in default_cert_keywords
            ):

                findings.append({

                    "severity": "WARNING",

                    "category": "SECURITY",

                    "message":
                        "Default HCP certificate detected",

                    "details":
                        cert.get("subject_dn")
                })

        # =================================
        # NODE HEALTH CHECKS
        # =================================
        unavailable_nodes = []

        hardware_types = set()

        for node in nodes:

            removed = str(
                node.get("removed")
            ).lower()

            state = str(
                node.get("state")
            ).upper()

            hardware = str(
                node.get("hardware_type")
            )

            if removed != "true":

                hardware_types.add(hardware)

                if state != "AVAILABLE":

                    unavailable_nodes.append(
                        node.get("node_number")
                    )

        # Node availability
        if unavailable_nodes:

            findings.append({

                "severity": "CRITICAL",

                "category": "NODES",

                "message":
                    "Unavailable nodes detected",

                "details":
                    ",".join(unavailable_nodes)
            })

        # Mixed hardware
        if len(hardware_types) > 1:

            findings.append({

                "severity": "INFO",

                "category": "NODES",

                "message":
                    "Mixed node hardware detected",

                "details":
                    ", ".join(hardware_types)
            })

        return findings

    # ---------------------------------
    # Analyze networking
    # ---------------------------------
    def analyze_networking(self):

        findings = []

        # =================================
        # Network Checks
        # =================================
        networks = self.config_data.get(
            "networks", []
        )

        replication_network_found = False

        for network in networks:

            network_name = str(
                network.get(
                    "name", ""
                )
            )

            # Ignore backend network
            if network_name == "[hcp_backend]":

                continue

            # -----------------------------
            # Replication Network
            # -----------------------------
            if network.get(
                "is_replication_network"
            ):

                replication_network_found = True

            # -----------------------------
            # Downstream DNS
            # -----------------------------
            dns_servers = str(
                network.get(
                    "dns_servers"
                )
            )

            if (
                dns_servers in [
                    "None",
                    "",
                    "null"
                ]
            ):

                findings.append({

                    "severity": "WARNING",

                    "category": "NETWORK",

                    "message":
                        "Downstream DNS server "
                        "not specified",

                    "details":
                    (f"Network={network_name} | "f"Domain={network.get('domain')}")
                })

            # -----------------------------
            # DNS Notify
            # -----------------------------
            dns_notify = str(
                network.get(
                    "dns_notify"
                )
            ).lower()

            if dns_notify == "false":

                findings.append({

                    "severity": "INFO",

                    "category": "NETWORK",

                    "message":
                        "DNS notify disabled",

                    "details":
                        (
                            f"Network={network_name} | "
                            f"Domain={network.get('domain')} | "
                            f"DNS failover updates "
                            f"may be slower"
                        )
                })

            # -----------------------------
            # DNS Refresh Rate
            # -----------------------------
            dns_refresh = str(
                network.get(
                    "dns_refresh_rate"
                )
            )

            if dns_refresh.endswith("H"):

                findings.append({

                    "severity": "INFO",

                    "category": "NETWORK",

                    "message":
                        "High DNS refresh interval",

                    "details":
                        (
                            f"Network={network_name} | "
                            f"Domain={network.get('domain')} | "
                            f"Refresh={dns_refresh}"
                        )
                })

        # Replication network missing
        if not replication_network_found:

            findings.append({

                "severity": "INFO",

                "category": "NETWORK",

                "message":
                    "No dedicated replication "
                    "network configured"
            })

        # =================================
        # Bond Checks
        # =================================
        bonds = self.config_data.get(
            "bond_configuration", []
        )

        for bond in bonds:

            bond_file = str(
                bond.get("bond_file")
            )

            bonding_mode = str(
                bond.get(
                    "bonding_mode", ""
                )
            )

            # -----------------------------
            # Front-End Bonding Mode
            # -----------------------------
            if bond_file == "bond0":

                if (
                    "802.3ad"
                    not in bonding_mode
                ):

                    findings.append({

                        "severity": "INFO",

                        "category": "NETWORK",

                        "message":
                            "Front-end bond not "
                            "using LACP",

                        "details":
                            (
                                "IEEE 802.3ad "
                                "can improve "
                                "performance"
                            )
                    })

            # -----------------------------
            # Interface Speed Checks
            # -----------------------------
            for interface in bond.get(
                "interfaces", []
            ):

                speed = str(
                    interface.get(
                        "speed", ""
                    )
                )

                interface_name = interface.get(
                    "interface"
                )

                if (
                    "25000"
                    not in speed
                ):

                    findings.append({

                        "severity": "INFO",

                        "category": "NETWORK",

                        "message":
                            "Interface not running "
                            "at 25Gbps",

                        "details":
                            (
                                f"{bond_file} | "
                                f"{interface_name} | "
                                f"{speed}"
                            )
                    })

        return findings

    # ---------------------------------
    # Analyze replication
    # ---------------------------------
    def analyze_replication(self):

        findings = []

        replications = self.config_data.get(
            "replications", []
        )

        for repl in replications:

            suspend = str(
                repl.get("suspend_state")
            ).upper()

            if suspend != "NOT_SUSPENDED":

                findings.append({

                    "severity": "WARNING",

                    "category": "REPLICATION",

                    "message":
                        "Replication link suspended",

                    "details":
                        repl.get("link_name")
                })

            else:

                findings.append({

                    "severity": "HEALTHY",

                    "category": "REPLICATION",

                    "message":
                        f"{repl.get('link_name')} "
                        f"replicating normally"
                })

        return findings


    # ---------------------------------
    # Analyze storage
    # ---------------------------------
    def analyze_storage(self):

        findings = []

        # =================================
        # Service Plan Checks
        # =================================
        service_plans = self.config_data.get(
            "service_plans", []
        )

        for plan in service_plans:

            plan_name = str(
                plan.get("name")
            )

            encryption = str(
                plan.get("encryption")
            ).upper()

            # -----------------------------
            # Encryption Check
            # -----------------------------
            if encryption == "NONE":

                findings.append({

                    "severity": "WARNING",

                    "category": "SERVICE_PLAN",

                    "message":
                        "Service plan not encrypting",

                    "details":
                        f"Plan={plan_name}"
                })

        # =================================
        # Storage Component Checks
        # =================================
        storage_components = self.config_data.get(
            "storage_components", []
        )

        for component in storage_components:

            name = str(
                component.get("name")
            )

            in_use = str(
                component.get("in_use")
            ).lower()

            # -----------------------------
            # In Use Check
            # -----------------------------
            if in_use == "false":

                findings.append({

                    "severity": "INFO",

                    "category": "STORAGE_COMPONENT",

                    "message":
                        "Storage component not in use",

                    "details":
                        f"Name={name}"
                })

        # =================================
        # Storage Pool Checks
        # =================================
        pools = self.config_data.get(
            "storage_pools", []
        )

        for pool in pools:

            pool_name = str(
                pool.get("name")
            )

            balancing_enabled = str(
                pool.get(
                    "balancing_enabled"
                )
            )

            balancing_status = str(
                pool.get(
                    "balancing_status"
                )
            )

            compressed = str(
                pool.get(
                    "compressed"
                )
            )

            in_use = str(
                pool.get(
                    "in_use"
                )
            ).lower()

            status = str(
                pool.get(
                    "status"
                )
            ).upper()

            # -----------------------------
            # Balancing Enabled
            # -----------------------------
            findings.append({

                "severity": "INFO",

                "category": "STORAGE_POOL",

                "message":
                    "Pool balancing configuration",

                "details":
                    (
                        f"Pool={pool_name} | "
                        f"Enabled={balancing_enabled}"
                    )
            })

            # -----------------------------
            # Balancing Status
            # -----------------------------
            findings.append({

                "severity": "INFO",

                "category": "STORAGE_POOL",

                "message":
                    "Pool balancing status",

                "details":
                    (
                        f"Pool={pool_name} | "
                        f"Status={balancing_status}"
                    )
            })

            # -----------------------------
            # Compression Status
            # -----------------------------
            findings.append({

                "severity": "INFO",

                "category": "STORAGE_POOL",

                "message":
                    "Pool compression status",

                "details":
                    (
                        f"Pool={pool_name} | "
                        f"Compressed={compressed}"
                    )
            })

            # -----------------------------
            # Pool Not In Use
            # -----------------------------
            if in_use == "false":

                findings.append({

                    "severity": "WARNING",

                    "category": "STORAGE_POOL",

                    "message":
                        "Storage pool not in use",

                    "details":
                        f"Pool={pool_name}"
                })

            # -----------------------------
            # Pool Not Active
            # -----------------------------
            if status != "ACTIVE":

                findings.append({

                    "severity": "WARNING",

                    "category": "STORAGE_POOL",

                    "message":
                        "Storage pool not active",

                    "details":
                        (
                            f"Pool={pool_name} | "
                            f"Status={status}"
                        )
                })

        return findings

    # ---------------------------------
    # Main analyze
    # ---------------------------------
    def analyze(self):

        report = []

        report.extend(
            self.analyze_cluster_health()
        )

        report.extend(
            self.analyze_networking()
        )

        report.extend(
            self.analyze_replication()
        )

        report.extend(
            self.analyze_storage()
        )

        return report

    # ---------------------------------
    # Print report
    # ---------------------------------
    def print_report(self, report):

        print("\n🧠 HCP CONFIGURATION INSIGHTS\n")

        hcp_score = self.calculate_hcp_score(report)

        print(
            f"HCP SCORE : "
            f"{hcp_score['score']}/100"
        )

        print(
            f"RATING    : "
            f"{hcp_score['rating']}"
        )

        print()

        if not report:

            print("No findings\n")
            return

        for finding in report:

            severity = finding.get(
                "severity"
            )

            category = finding.get(
                "category"
            )

            message = finding.get(
                "message"
            )

            details = finding.get(
                "details"
            )

            line = (
                f"{severity:<10}"
                f"| "
                f"{category:<12}"
                f"| "
                f"{message}"
            )

            if details:

                line += f" -> {details}"

            print(line)
            print("-" * 92 + "\n")
            

        print("\n" + "=" * 70 + "\n")
        
        


    # ---------------------------------
    # Calculate HCP Score
    # ---------------------------------
    def calculate_hcp_score(
        self,
        report
    ):

        score = 100

        # ---------------------------------
        # Parameter Weight Mapping
        # ---------------------------------
        parameter_weights = {

            # HIGH
            "Only one DNS server configured":
            -12,

            "Only one NTP server configured":
            -12,

            "DIFE encryption disabled":
            -12,

            "Unavailable nodes detected":
            -12,

            # MEDIUM
            "Unexpected map size configured":
            -7,

            # LOW
            "TLSv1.3 not enforced":
            -3,

            "Default HCP certificate detected":
            -3,

            "Downstream DNS server not specified":
            -3,

            "DNS notify disabled":
            -3,

            "High DNS refresh interval":
            -3
        }

        # ---------------------------------
        # Apply Weights
        # ---------------------------------
        for finding in report:

            message = str(
                finding.get(
                    "message",
                    ""
                )
            )

            weight = parameter_weights.get(
                message,
                0
            )

            score += weight

        # ---------------------------------
        # Score Floor
        # ---------------------------------
        if score < 0:

            score = 0

        # ---------------------------------
        # Rating
        # ---------------------------------
        if score >= 90:

            rating = "EXCELLENT"

        elif score >= 75:

            rating = "GOOD"

        elif score >= 50:

            rating = "FAIR"

        elif score >= 25:

            rating = "POOR"

        else:

            rating = "CRITICAL"

        return {

            "score": score,

            "rating": rating
        }
    
    # ---------------------------------
    # Get report dataframe
    # ---------------------------------
    def get_report_df(

        self,

        report
    ):

        return pd.DataFrame(

            report
        )

