class HCPNodeAdditionService:

    def __init__(
        self,
        cluster_profile
        ):
        self.cluster_profile = (
            cluster_profile
            )
        self.node_addition_input = {}


    # ---------------------------------
    # Take Node Addition Input
    # ---------------------------------
    def collect_node_addition_input(self):

        print("\n🖥️ NODE ADDITION INPUT\n")

        # ---------------------------------
        # Number of Nodes
        # ---------------------------------
        while True:

            try:

                node_count = int(

                    input(
                        "Enter number of nodes "
                        "to add: "
                    )
                )

                # Must be greater than 0
                if node_count <= 0:

                    print(
                        "Node count must be "
                        "greater than 0"
                    )

                    continue

                # Must be even number
                if node_count % 2 != 0:

                    print(
                        "HCP node addition "
                        "requires even number "
                        "of nodes"
                    )

                    continue

                break

            except ValueError:

                print(
                    "Please enter a valid number"
                )

        # ---------------------------------
        # Node Model
        # ---------------------------------
        print("\nSupported Node Models:")

        
        print("1. HCP G11")
        print("2. HCP O12")

        model_choice = input(
            "\nSelect node model: "
        ).strip()

        model_map = {


            "1": "HCP G11",

            "2": "HCP O12"
        }

        node_model = model_map.get(
            model_choice,
            "UNKNOWN"
        )

        # ---------------------------------
        # NIC Card / Port Speed
        # ---------------------------------
        print("\nNIC Card :")

        # ---------------------------------
        # O12 supports only 10G
        # ---------------------------------
        if node_model == "HCP G11":

            print(
                "HCP G11 supports "
                "only 10G SFP+"
            )

            switch_port_speed = "10G"

        else:

            print("1. 10G SFP+")
            print("2. 25G SFP+")

            speed_choice = input(
                "\nSelect NIC Card "
                "port speed: "
            ).strip()

            speed_map = {

                "1": "10G",

                "2": "25G"
            }

            switch_port_speed = speed_map.get(
                speed_choice,
                "UNKNOWN"
            )


        # ---------------------------------
        # Expected Backend NIC Details
        # ---------------------------------
        if switch_port_speed == "10G":

            expected_backend_port = {

                "supported_ports":
                "[ FIBRE ]",

                "speed":
                "10000Mb/s",

                "port":
                "Direct Attach Copper"
            }

        elif switch_port_speed == "25G":

            expected_backend_port = {

                "supported_ports":
                "[ FIBRE ]",

                "speed":
                "25000Mb/s",

                "port":
                "Direct Attach Copper"
            }

        else:

            expected_backend_port = {}

        # ---------------------------------
        # Save Input
        # ---------------------------------
        self.node_addition_input = {

            "node_count": node_count,

            "node_model": node_model,

            "switch_port_speed": switch_port_speed,

            "expected_backend_port": expected_backend_port
        }

        return self.node_addition_input


    # ---------------------------------
    # Print Input Summary
    # ---------------------------------
    def print_node_addition_input(self):

        data = self.node_addition_input

        if not data:

            print(
                "\nNo node addition input found\n"
            )

            return

        print("\n🛠️ NODE ADDITION REQUEST\n")

        print(
            f"Number of Nodes     : "
            f"{data.get('node_count')}"
        )

        print(
            f"Node Model          : "
            f"{data.get('node_model')}"
        )

        print(
            f"Switch Port Speed   : "
            f"{data.get('switch_port_speed')}"
        )

        print("\n" + "=" * 70 + "\n")


    # ---------------------------------
    # Validate Node Addition
    # ---------------------------------
    def validate_node_addition(self):

        validations = []

        existing_models = (
            self.cluster_profile.get(
                "node_models",
                []
            )
        )

        existing_version = str(

            self.cluster_profile.get(
                "software_version",
                ""
            )
        )

        new_model = (
            self.node_addition_input.get(
                "node_model"
            )
        )

        # ---------------------------------
        # Validation 1
        # Cannot mix G10 and O12
        # ---------------------------------
        if (

            "HCP G10" in existing_models
            and new_model == "HCP O12"

        ):

            validations.append({

                "status": "FAILED",

                "message":
                (
                    "Cannot mix "
                    "HCP G10 and "
                    "HCP O12 nodes"
                )
            })

        else:

            validations.append({

                "status": "PASSED",

                "message":
                (
                    "Node model mix "
                    "validation passed"
                )
            })

        # ---------------------------------
        # Validation 2
        # Recommended Version
        # ---------------------------------
        if existing_version != "10.0.1.4":

            validations.append({

                "status": "WARNING",

                "message":
                (
                    "Recommended HCP "
                    "version for node "
                    "addition is 10.0.1.4"
                )
            })

        else:

            validations.append({

                "status": "PASSED",

                "message":
                (
                    "Recommended HCP "
                    "version validation passed"
                )
            })

        # ---------------------------------
        # Validation 3
        # O12 requires HCP 10.x
        # ---------------------------------
        if new_model == "HCP O12":

            if not existing_version.startswith(
                "10."
            ):

                validations.append({

                    "status": "WARNING",

                    "message":
                    (
                        "Existing HCP "
                        "cluster must be "
                        "10.x for adding "
                        "HCP O12 nodes"
                    )
                })

            else:

                validations.append({

                    "status": "PASSED",

                    "message":
                    (
                        "HCP version "
                        "supports O12 nodes"
                    )
                })

        # ---------------------------------
        # Validation 4
        # Backend Port Validation
        # ---------------------------------
        expected_port = (

            self.node_addition_input.get(
                "expected_backend_port",
                {}
            )
        )

        be_ports = (
            self.cluster_profile.get(
                "be_ports",
                []
            )
        )

        for port in be_ports:

            existing_supported_ports = str(

                port.get(
                    "supported_ports",
                    ""
                )
            ).strip()

            existing_speed = str(

                port.get(
                    "speed",
                    ""
                )
            ).strip()

            existing_port = str(

                port.get(
                    "port",
                    ""
                )
            ).strip()

            expected_supported_ports = str(

                expected_port.get(
                    "supported_ports",
                    ""
                )
            ).strip()

            expected_speed = str(

                expected_port.get(
                    "speed",
                    ""
                )
            ).strip()

            expected_port_type = str(

                expected_port.get(
                    "port",
                    ""
                )
            ).strip()

            # ---------------------------------
            # Supported Ports Mismatch
            # ---------------------------------
            if (
                existing_supported_ports
                != expected_supported_ports
            ):

                validations.append({

                    "status": "FAILED",

                    "message":
                    (
                        f"{port.get('interface')} "
                        f"supported ports "
                        f"do not match "
                        f"required NIC"
                    )
                })

                continue

            # ---------------------------------
            # Speed Mismatch
            # ---------------------------------
            if existing_speed != expected_speed:

                validations.append({

                    "status": "WARNING",

                    "message":
                    (
                        f"{port.get('interface')} "
                        f"speed mismatch. "
                        f"Existing="
                        f"{existing_speed}, "
                        f"Required="
                        f"{expected_speed}"
                    )
                })

                continue

            # ---------------------------------
            # Port Type Mismatch
            # ---------------------------------
            if existing_port != expected_port_type:

                validations.append({

                    "status": "WARNING",

                    "message":
                    (
                        f"{port.get('interface')} "
                        f"port type mismatch. "
                        f"Existing="
                        f"{existing_port}, "
                        f"Required="
                        f"{expected_port_type}"
                    )
                })

                continue

            # ---------------------------------
            # Full Match
            # ---------------------------------
            validations.append({

                "status": "PASSED",

                "message":
                (
                    f"{port.get('interface')} "
                    f"backend NIC matches "
                    f"expected configuration. "
                    f"Double-check BOM and "
                    f"field implementation."
                )
            })
        

        # ---------------------------------
        # Save validations
        # ---------------------------------
        self.validations = validations

        # ---------------------------------
        # Print validations
        # ---------------------------------
        self.print_validation_results()

        # ---------------------------------
        # Check for failed validations
        # ---------------------------------
        failed_validations = [

            v for v in self.validations

            if v["status"] == "FAILED"
        ]

        # ---------------------------------
        # Build projected cluster profile
        # ---------------------------------
        if not failed_validations:

            self.build_projected_cluster_profile()

            


    # ---------------------------------
    # Print Validation Results
    # ---------------------------------
    def print_validation_results(self):

        print(
            "\n🔎 NODE ADDITION VALIDATION\n"
        )

        if not hasattr(
            self,
            "validations"
        ):

            print(
                "No validation results found"
            )

            return

        for validation in self.validations:

            print(

                f"[{validation['status']}] "
                f"{validation['message']}"
            )

        print("\n" + "=" * 70 + "\n")


    # ---------------------------------
    # Build Projected Cluster Profile
    # ---------------------------------
    def build_projected_cluster_profile(self):

        print(
            "\n✅ Validation passed. "
            "Building projected cluster profile...\n"
        )

        projected_profile = dict(
            self.cluster_profile
        )

        existing_nodes = list(

            projected_profile.get(
                "node_details",
                []
            )
        )

        existing_count = int(

            projected_profile.get(
                "node_count",
                0
            )
        )

        nodes_to_add = int(

            self.node_addition_input.get(
                "node_count",
                0
            )
        )

        new_model = (
            self.node_addition_input.get(
                "node_model"
            )
        )

        # ---------------------------------
        # Last Node Number
        # ---------------------------------
        existing_node_numbers = []

        for node in existing_nodes:

            try:

                existing_node_numbers.append(

                    int(node.get(
                        "node_number"
                    ))
                )

            except:

                pass

        if existing_node_numbers:

            last_node = max(
                existing_node_numbers
            )

        else:

            last_node = 100

        # ---------------------------------
        # Add New Nodes
        # ---------------------------------
        for i in range(nodes_to_add):

            new_node_number = (
                last_node + i + 1
            )

            existing_nodes.append({

                "node_number":
                str(new_node_number),

                "hardware_type":
                new_model,

                "private_ip":
                "TO_BE_ASSIGNED",

                "system_ip":
                "TO_BE_ASSIGNED"
            })

        # ---------------------------------
        # Update Counts
        # ---------------------------------

        # ---------------------------------
        # Add Networks For New Nodes
        # ---------------------------------
        projected_networks = list(

            projected_profile.get(
                "networks",
                []
            )
        )

        # Existing networks from first node
        template_networks = []

        if projected_networks:

            first_node_number = str(

                projected_networks[0].get(
                    "node_number"
                )
            )

            template_networks = [

                n for n in projected_networks

                if str(
                    n.get("node_number")
                ) == first_node_number
            ]

        # ---------------------------------
        # Create networks for new nodes
        # ---------------------------------
        for i in range(nodes_to_add):

            new_node_number = str(
                last_node + i + 1
            )

            for network in template_networks:

                projected_networks.append({

                    "node_number":
                    new_node_number,

                    "network_name":
                    network.get(
                        "network_name"
                    ),

                    "ip_address":
                    "TO_BE_ASSIGNED",

                    "gateway":
                    network.get(
                        "gateway"
                    ),

                    "mtu":
                    network.get(
                        "mtu"
                    ),

                    "vlan":
                    network.get(
                        "vlan"
                    )
                })

        # ---------------------------------
        # Save projected networks
        # ---------------------------------
        projected_profile[
            "networks"
        ] = projected_networks      

        
        projected_profile[
            "node_details"
        ] = existing_nodes

        projected_profile[
            "node_count"
        ] = (
            existing_count
            + nodes_to_add
        )


        # ---------------------------------
        # Recalculate Region Count
        # ---------------------------------
        new_node_count = projected_profile.get(
            "node_count",
            0
        )

        if new_node_count == 1:

            expected_map_size = 32

        elif 2 <= new_node_count <= 4:

            expected_map_size = 64

        elif 5 <= new_node_count <= 8:

            expected_map_size = 128

        elif 9 <= new_node_count <= 16:

            expected_map_size = 256
            
        elif node_count >= 17:

            expected_map_size = 256

        else:

            expected_map_size = "UNKNOWN"

        projected_profile[
            "recommended_map_size"
        ] = expected_map_size
        

        # ---------------------------------
        # Update Node Models
        # ---------------------------------
        models = set(

            projected_profile.get(
                "node_models",
                []
            )
        )

        models.add(new_model)

        projected_profile[
            "node_models"
        ] = sorted(list(models))

        # ---------------------------------
        # Print Projected Profile
        # ---------------------------------
        self.print_full_projected_cluster_profile(
            projected_profile
        )


    # ---------------------------------
    # Print Projected Cluster Profile
    # ---------------------------------
    def print_projected_cluster_profile(

        self,
        profile
    ):

        print(
            "\n🛠️ PROJECTED HCP TECH REFRESH PROFILE\n"
        )

        print(
            f"Node Count             : "
            f"{profile.get('node_count')}"
        )

        print(
            f"Node Models            : "
            f"{', '.join(profile.get('node_models', []))}"
        )

        print("\n" + "=" * 70)

        print("\n🖥️ NODE DETAILS\n")

        print(

            f"{'Node':<8}"
            f"{'Hardware':<18}"
            f"{'Private IP':<20}"
        )

        print("-" * 70)

        for node in profile.get(
            "node_details",
            []
        ):

            print(

                f"{str(node.get('node_number')):<8}"
                f"{str(node.get('hardware_type')):<18}"
                f"{str(node.get('private_ip')):<20}"
            )

        print("\n" + "=" * 70 + "\n")

    # ---------------------------------
    # Print Full Projected Cluster Profile
    # ---------------------------------
    def print_full_projected_cluster_profile(

        self,
        profile
    ):

        print(
            "\n🛠️ PROJECTED HCP TECH REFRESH PROFILE\n"
        )

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

        print()

        print(
            f"Map Version            : "
            f"{profile.get('map_version')}"
        )

        print(
            f"Region Count           : "
            f"{profile.get('map_size')}"
        )

        print(
            f"Recommended Regions    : "
            f"{profile.get('recommended_map_size')}"
        )



        print("\n" + "=" * 70)

        # ---------------------------------
        # Node Details
        # ---------------------------------
        print("\n🖥️ NODE DETAILS\n")

        print(

            f"{'Node':<8}"
            f"{'Hardware':<18}"
            f"{'Private IP':<20}"
            f"{'System IP':<20}"
        )

        print("-" * 80)

        for node in profile.get(
            "node_details",
            []
        ):

            print(

                f"{str(node.get('node_number')):<8}"
                f"{str(node.get('hardware_type')):<18}"
                f"{str(node.get('private_ip')):<20}"
                f"{str(node.get('system_ip')):<20}"
            )

        print("\n" + "=" * 70)

        # ---------------------------------
        # FE Bond
        # ---------------------------------
        print("\nFront-End Bond Mode:\n")

        print(
            profile.get(
                "fe_bond_mode"
            )
        )

        # ---------------------------------
        # BE Bond
        # ---------------------------------
        print("\nBack-End Bond Mode:\n")

        print(
            profile.get(
                "be_bond_mode"
            )
        )

        print("\n" + "=" * 70)

        # ---------------------------------
        # FE Ports
        # ---------------------------------
        print("\nFront-End Port Details:\n")

        for port in profile.get(
            "fe_ports",
            []
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
            "be_ports",
            []
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

        print("\n" + "=" * 70)


        # ---------------------------------
        # Networks
        # ---------------------------------
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
