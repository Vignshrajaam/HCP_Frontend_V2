import pandas as pd
from utils.export import ExportManager


class NamespaceInsightsService:

    def __init__(self, config_data):

        self.config_data = config_data
        self.exporter = ExportManager()
    

    # ---------------------------------
    # Export Tenant Summary ( dict format  to DataFrame and export )
    # ---------------------------------
    def export_tenant_summary(

        self
    ):

        tenant_data = (
            self.collector.collect_tenants()
        )

        if not tenant_data:

            print(
                "\nNo tenant data found\n"
            )

            return

        df = pd.DataFrame(
            tenant_data
        )

        self.exporter.prompt_single_export(

            df,

            "tenants"
        )
    
    # ---------------------------------
    # Export Namespace Summary ( dict format  to DataFrame and export )
    # ---------------------------------
    def export_namespace_summary(

        self
    ):

        namespace_data = (
            self.collector.collect_namespaces()
        )

        if not namespace_data:

            print(
                "\nNo namespace data found\n"
            )

            return

        df = pd.DataFrame(
            namespace_data
        )

        self.exporter.prompt_single_export(

            df,

            "namespaces"
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

        # ---------------------------------
        # Convert to DataFrame
        # ---------------------------------
        df = pd.DataFrame(
            tenants
        )

        for tenant in tenants:

            print(
                f"Tenant Name           : "
                f"{tenant.get('name')}"
            )

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

            print(
                "\n" + "=" * 70 + "\n"
            )

        # ---------------------------------
        # Export
        # ---------------------------------
        self.exporter.prompt_single_export(

            df,

            "tenants"
        )


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

        # ---------------------------------
        # Convert to DataFrame
        # ---------------------------------
        df = pd.DataFrame(
            namespaces
        )

        for ns in namespaces:

            print(
                f"Namespace Name        : "
                f"{ns.get('name')}"
            )

            print(
                f"Tenant                : "
                f"{ns.get('tenant')}"
            )

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

            print(
                "\n" + "=" * 70 + "\n"
            )

        # ---------------------------------
        # Export
        # ---------------------------------
        self.exporter.prompt_single_export(

            df,

            "namespaces"
        ) 
    




    # ---------------------------------
    # Namespace Risk Assessment
    # ---------------------------------
    def namespace_risk_assessment(self):

        namespaces = self.config_data.get(
            "namespaces",
            []
        )

        report = []

        for ns in namespaces:

            score = 0

            reasons = []

            # ---------------------------------
            # DPL=1 without replication
            # ---------------------------------
            if (

                str(
                    ns.get("dpl")
                ) == "1"

                and

                ns.get(
                    "replication_enabled"
                ) is False
            ):

                score += 50

                reasons.append(
                    "DPL=1 without replication"
                )

            # ---------------------------------
            # Replication disabled
            # ---------------------------------
            if ns.get(
                "replication_enabled"
            ) is False:

                score += 25

                reasons.append(
                    "Replication disabled"
                )

            # ---------------------------------
            # HTTP enabled
            # ---------------------------------
            if ns.get(
                "http_enabled"
            ) is True:

                score += 20

                reasons.append(
                    "HTTP enabled"
                )

            # ---------------------------------
            # No retention default
            # ---------------------------------
            if str(

                ns.get(
                    "retention_default",
                    "0"
                )

            ) == "0":

                score += 25

                reasons.append(
                    "No default retention"
                )

            # ---------------------------------
            # S3 Object Lock disabled
            # ---------------------------------
            if (

                ns.get(
                    "s3_enabled"
                ) is True

                and

                ns.get(
                    "s3_objectlock"
                ) == "NONE"
            ):

                score += 10

                reasons.append(
                    "S3 Object Lock disabled"
                )

            # ---------------------------------
            # Cloud optimized disabled
            # ---------------------------------
            if ns.get(
                "cloud_optimized"
            ) is False:

                score += 20

                reasons.append(
                    "Cloud optimized disabled"
                )

            # ---------------------------------
            # Version pruning disabled
            # ---------------------------------
            if (

                ns.get(
                    "versioning_enabled"
                ) is True

                and

                ns.get(
                    "versioning_pruning_enabled"
                ) is False
            ):

                score += 15

                reasons.append(
                    "Version pruning disabled"
                )

            # ---------------------------------
            # ACL mismatch
            # ---------------------------------
            if (

                ns.get(
                    "acls_enabled"
                ) is True

                and

                ns.get(
                    "acls_honored"
                ) is False
            ):

                score += 5

                reasons.append(
                    "ACLs enabled but not honored"
                )

            # ---------------------------------
            # Search misconfiguration
            # ---------------------------------
            if (

                ns.get(
                    "search_enabled"
                ) is True

                and

                ns.get(
                    "indexing_enabled"
                ) is False
            ):

                score += 10

                reasons.append(
                    "Search enabled but indexing disabled"
                )

            # ---------------------------------
            # Severity
            # ---------------------------------
            if score >= 70:

                severity = "CRITICAL"

            elif score >= 40:

                severity = "HIGH"

            elif score >= 20:

                severity = "MEDIUM"

            else:

                severity = "LOW"

            report.append({

                "tenant":
                ns.get("tenant"),

                "name":
                ns.get("name"),

                "score":
                score,

                "severity":
                severity,

                "reasons":
                reasons
            })

        return report


    # ---------------------------------
    # Print Namespace Risk Assessment
    # ---------------------------------
    def print_namespace_risk_assessment(
        self,
        report
    ):

        print(
            "\n📊 NAMESPACE RISK "
            "ASSESSMENT REPORT\n"
        )

        if not report:

            print(
                "No namespaces found\n"
            )

            return

        sorted_report = sorted(

            report,

            key=lambda x:
            x["score"],

            reverse=True
        )

        findings = False

        for ns in sorted_report:

            if ns["score"] == 0:

                continue

            findings = True

            print(

                f"{ns['severity']} | "
                f"Score={ns['score']} | "
                f"{ns['tenant']} / "
                f"{ns['name']}"
            )

            for reason in ns["reasons"]:

                print(
                    f"   - {reason}"
                )

            print()

        if not findings:

            print(
                "✅ No namespace "
                "risk findings detected"
            )

        print(
            "\n" + "=" * 70 + "\n"
        )


    # ---------------------------------
    # Namespace Classification
    # ---------------------------------
    def namespace_classification(self):

        namespaces = self.config_data.get(
            "namespaces",
            []
        )

        report = []

        for ns in namespaces:

            # ---------------------------------
            # Compliance / Governance
            # ---------------------------------
            if (

                str(
                    ns.get(
                        "retention_default",
                        "0"
                    )
                ) != "0"

                or

                ns.get(
                    "s3_objectlock"
                ) != "NONE"
            ):

                classification = "COMPLIANCE"

            # ---------------------------------
            # Search / Discovery
            # ---------------------------------
            elif (

                ns.get(
                    "search_enabled"
                ) is True

                or

                ns.get(
                    "indexing_enabled"
                ) is True
            ):

                classification = "SEARCH"

            # ---------------------------------
            # Logging / Observability
            # ---------------------------------
            elif (

                ns.get(
                    "s3_enabled"
                ) is True

                and

                ns.get(
                    "cloud_optimized"
                ) is True

                and

                str(
                    ns.get("dpl")
                ) == "1"

                and

                ns.get(
                    "replication_enabled"
                ) is False

                and

                ns.get(
                    "versioning_enabled"
                ) is True
            ):

                classification = "LOGGING"

            # ---------------------------------
            # Cloud Native / Modern App
            # ---------------------------------
            elif (

                ns.get(
                    "s3_enabled"
                ) is True

                and

                ns.get(
                    "cloud_optimized"
                ) is True
            ):

                classification = "CLOUD_NATIVE"

            # ---------------------------------
            # Backup Repository
            # ---------------------------------
            elif (

                ns.get(
                    "versioning_enabled"
                ) is True

                and

                ns.get(
                    "s3_enabled"
                ) is True
            ):

                classification = "BACKUP"

            # ---------------------------------
            # Standard S3
            # ---------------------------------
            elif ns.get(
                "s3_enabled"
            ) is True:

                classification = "S3_STANDARD"

            # ---------------------------------
            # General Purpose
            # ---------------------------------
            else:

                classification = "GENERAL"

            report.append({

                "tenant":
                ns.get("tenant"),

                "name":
                ns.get("name"),

                "classification":
                classification
            })

        return report


    # ---------------------------------
    # Print Namespace Classification
    # ---------------------------------
    def print_namespace_classification(
        self,
        report
    ):

        print(
            "\n📂 NAMESPACE "
            "CLASSIFICATION\n"
        )

        if not report:

            print(
                "No namespaces found\n"
            )

            return

        print(

            f"{'Classification':<20}"
            f"{'Tenant / Namespace'}"

        )

        print("-" * 70)

        for ns in report:

            print(

                f"{ns['classification']:<20}"
                f"{ns['tenant']} / "
                f"{ns['name']}"
            )

        print(
            "\n" + "=" * 70 + "\n"
        )
    
