class HCPTechRefreshService:

    def __init__(self, config_data):

        self.config_data = config_data


    # ---------------------------------
    # Collect ATR / Node Addition Data
    # ---------------------------------
    def collect_cluster_profile(self):

        profile = {}

        # ---------------------------------
        # Nodes
        # ---------------------------------
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

        profile["node_models"] = sorted(

            list({

                n.get("hardware_type")

                for n in active_nodes
            })
        )

        profile["node_count"] = len(
            active_nodes
        )

        profile["backend_switches"] = (
            backend_switches
        )

        # ---------------------------------
        # Node Details
        # ---------------------------------
        node_details = []

        for node in active_nodes:

            node_details.append({

                "node_number": node.get(
                    "node_number"
                ),

                "hardware_type": node.get(
                    "hardware_type"
                ),

                "private_ip": node.get(
                    "private_ip"
                )

                #"system_ip": node.get(
                #    "system_ip"
                
            })

        profile["node_details"] = (
            node_details
        )

        # ---------------------------------
        # Cluster Type
        # ---------------------------------
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

            storage_type = settings.get(
                "storage_type"
            )

            profile["software_version"] = (
                settings.get(
                    "software_version"
                )
            )            

            profile["storage_type"] = storage_type

            if storage_type == "internal":

                profile["cluster_architecture"] = "RAIN"

            elif storage_type == "external":

                profile["cluster_architecture"] = "SAIN"

            else:

                profile["cluster_architecture"] = "UNKNOWN"



        # ---------------------------------
        # Map Information
        # ---------------------------------
        jvm = self.config_data.get(
            "jvm_status", {}
        )

        if jvm:

            profile["map_version"] = jvm.get(
                "map_version"
            )

            profile["map_size"] = jvm.get(
                "map_size"
            )

        # ---------------------------------
        # Bond Information
        # ---------------------------------
        bonds = self.config_data.get(
            "bond_configuration", []
        )

        for bond in bonds:

            bond_file = bond.get(
                "bond_file"
            )

            if bond_file == "bond0":

                profile["fe_bond_mode"] = bond.get(
                    "bonding_mode"
                )

            elif bond_file == "bond1":

                profile["be_bond_mode"] = bond.get(
                    "bonding_mode"
                )

        # ---------------------------------
        # Physical Interfaces
        # ---------------------------------
        physical_interfaces = self.config_data.get(
            "physical_interfaces", []
        )

        fe_ports = []

        be_ports = []

        for interface in physical_interfaces:

            interface_name = str(
                interface.get("interface", "")
            ).lower()

            port_data = {

                "interface": interface_name,

                "supported_ports": interface.get(
                    "supported_ports"
                ),

                "speed": interface.get(
                    "speed"
                ),

                "port": interface.get(
                    "port"
                )
            }

            # FE Interfaces
            if interface_name in [
                "eth0",
                "eth2"
            ]:

                fe_ports.append(
                    port_data
                )

            # BE Interfaces
            elif interface_name in [
                "eth1",
                "eth3"
            ]:

                be_ports.append(
                    port_data
                )

        profile["fe_ports"] = fe_ports

        profile["be_ports"] = be_ports


        # ---------------------------------
        # HCP Networks
        # ---------------------------------
        network_interfaces = self.config_data.get(
            "network_interfaces",
            []
        )

        networks = []

        for network in network_interfaces:

            networks.append({

                "node_number": network.get(
                    "node_number"
                ),

                "network_name": network.get(
                    "network_name"
                ),

                "ip_address": network.get(
                    "ip_address"
                ),

                "gateway": network.get(
                    "gateway"
                ),

                "mtu": network.get(
                    "mtu"
                ),

                "vlan": network.get(
                    "vlan"
                )
            })

        profile["networks"] = networks
        

        return profile


    # ---------------------------------
    # Print ATR Cluster Profile
    # ---------------------------------
    def print_cluster_profile(self):

        profile = self.collect_cluster_profile()

        print("\n🛠️ HCP TECH REFRESH PROFILE\n")

        print(
            f"Cluster Architecture   : "
            f"{profile.get('cluster_architecture')}"
        )

        print(
            f"Storage Type           : "
            f"{profile.get('storage_type')}"
        )

        print(
            f"Software Version       : "
            f"{profile.get('software_version')}"
        )

        print()

        print(
            f"Node Count             : "
            f"{profile.get('node_count')}"
        )

        print(
            f"Node Models            : "
            f"{', '.join(profile.get('node_models', []))}"
        )


        print("\n" + "=" * 70)

        # ---------------------------------
        # Node Details
        # ---------------------------------
        print("\n🖥️ NODE DETAILS\n")

        print(

            f"{'Node':<8}"
            f"{'Hardware':<18}"
            f"{'Private IP':<18}"
            #f"{'System IP':<18}"
        )

        print("-" * 70)

        for node in profile.get(
            "node_details", []
        ):

            print(

                f"{str(node.get('node_number')):<8}"
                f"{str(node.get('hardware_type')):<18}"
                f"{str(node.get('private_ip')):<18}"
                #f"{str(node.get('system_ip')):<18}"
            )

        print()

                
        print(
            f"Map Version            : "
            f"{profile.get('map_version')}" 
        )

        print(
            f"Region Count           : "
            f"{profile.get('map_size')}"
        )

        print("\n" + "=" * 70 + "\n")

        
        
        print(
            f"Front-End Bond Mode    : "
            f"{profile.get('fe_bond_mode')}"
        )

        print(
            f"Back-End Bond Mode     : "
            f"{profile.get('be_bond_mode')}"
        )

        print("\n" + "=" * 70 + "\n")

        
        # ---------------------------------
        # FE Ports
        # ---------------------------------
        print("\nFront-End Port Details:\n")

        for port in profile.get(
            "fe_ports", []
        ):

            print(
                f"{port.get('interface')}"
            )

            print(
                f"  Supported Ports      : "
                f"{port.get('supported_ports')}"
            )

            print(
                f"  Speed                : "
                f"{port.get('speed')}"
            )

            print(
                f"  Port                 : "
                f"{port.get('port')}"
            )

            print()

        # ---------------------------------
        # BE Ports
        # ---------------------------------
        print("\nBack-End Port Details:\n")

        for port in profile.get(
            "be_ports", []
        ):

            print(
                f"{port.get('interface')}"
            )

            print(
                f"  Supported Ports      : "
                f"{port.get('supported_ports')}"
            )

            print(
                f"  Speed                : "
                f"{port.get('speed')}"
            )

            print(
                f"  Port                 : "
                f"{port.get('port')}"
            )

            print()

        # ---------------------------------
        # HCP Networks
        # ---------------------------------

        print("\n" + "=" * 70 + "\n")

        print(
            "\n🌐 HCP NETWORK INTERFACE SUMMARY\n"
        )

        networks = profile.get(
            "networks",
            []
        )

        if not networks:

            print(
                "No network information found"
            )

        else:

            grouped_networks = {}

            # ---------------------------------
            # Group by network name
            # ---------------------------------
            for network in networks:

                network_name = network.get(
                    "network_name"
                )

                if (
                    network_name
                    not in grouped_networks
                ):

                    grouped_networks[
                        network_name
                    ] = []

                grouped_networks[
                    network_name
                ].append(network)

            # ---------------------------------
            # Print grouped networks
            # ---------------------------------
            for network_name, entries in (
                grouped_networks.items()
            ):

                print(
                    f"\nNetwork Name : "
                    f"{network_name}\n"
                )

                for network in entries:

                    print(
                        f"Node        : "
                        f"{network.get('node_number')}"
                    )

                    print(
                        f"IP Address  : "
                        f"{network.get('ip_address')}"
                    )

                    print(
                        f"Gateway     : "
                        f"{network.get('gateway')}"
                    )

                    print(
                        f"MTU         : "
                        f"{network.get('mtu')}"
                    )

                    print(
                        f"VLAN        : "
                        f"{network.get('vlan')}"
                    )

                    print()

        
        

        print("\n" + "=" * 70 + "\n")
