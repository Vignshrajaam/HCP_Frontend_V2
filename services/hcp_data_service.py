# NOTE:
# SystemLogParser deprecated for
# tenant/namespace normalization.
# HCPConfigurationCollector is now
# the primary source of truth.

from collectors.logs.hcp_configuration_collector import HCPConfigurationCollector
from collectors.logs.access_log_collector import AccessLogCollector


class HCPDataService:

    def __init__(self, base_path):

        self.base_path = base_path

    # ---------------------------------
    # Main data collection
    # ---------------------------------
    def gather_all(

        self,

        include_access_logs=False
    ):

        # -----------------------------
        # Configuration collection
        # -----------------------------
        collector = (
            HCPConfigurationCollector(
                self.base_path
            )
        )

        config = collector.collect()

        # -----------------------------
        # Base result
        # -----------------------------
        result = {

            "config": config,

            "tenants":
            config.get(
                "tenants",
                []
            ),

            "namespaces":
            config.get(
                "namespaces",
                []
            )
        }

        # -----------------------------
        # Optional access logs
        # -----------------------------
        if include_access_logs:

            access_collector = (
                AccessLogCollector(
                    self.base_path
                )
            )

            access_logs = (
                access_collector.collect()
            )

            result[
                "access_logs"
            ] = access_logs

        return result

    # ---------------------------------
    # Convenience functions
    # ---------------------------------
    def get_tenants(self, data):

        return data.get("tenants", [])

    def get_namespaces(self, data):

        return data.get("namespaces", [])

    def get_config(self, data):

        return data.get("config", {})

