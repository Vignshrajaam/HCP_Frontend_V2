import pandas as pd
from analytics.filters import AccessLogFilters



class HCPAccessLogAnalysisService:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(self, dataframe):

        self.df = dataframe

        self.filters = (
            AccessLogFilters(
                dataframe
            )
        )

    # ---------------------------------
    # Validate DataFrame
    # ---------------------------------
    def has_data(self):

        return (

            self.df is not None

            and not self.df.empty
        )

    # ---------------------------------
    # Access Log Summary
    # ---------------------------------
    def get_summary(self):

        if not self.has_data():

            return {}

        return {

            "total_requests":
            len(self.df),

            "unique_client_ips":
            self.df["ip"].nunique(),

            "unique_users":
            self.df["user"].nunique(),

            "unique_hosts":
            self.df["host"].nunique(),

            "http_methods":
            self.df["method"]
            .value_counts()
            .to_dict(),

            "status_codes":
            self.df["status"]
            .value_counts()
            .to_dict()
        }

    # ---------------------------------
    # Top Client IPs
    # ---------------------------------
    def get_top_client_ips(

        self,

        limit=10
    ):

        if not self.has_data():

            return pd.DataFrame()

        return (

            self.df["ip"]

            .value_counts()

            .head(limit)

            .reset_index(
                name="requests"
            )

            .rename(

                columns={

                    "index":
                    "ip"
                }
            )
        )

    # ---------------------------------
    # Failed Requests
    # ---------------------------------
    def get_failed_requests(self):

        if not self.has_data():

            return pd.DataFrame()

        return self.df[

            self.df["status"]

            .astype(str)

            .str.startswith(

                ("4", "5")
            )
        ]

    # ---------------------------------
    # S3 Operations
    # ---------------------------------
    def get_s3_operations(self):

        if not self.has_data():

            return pd.DataFrame()

        s3_methods = [

            "PUT",
            "GET",
            "DELETE",
            "HEAD"
        ]

        return self.df[

            self.df["method"]

            .isin(s3_methods)
        ]

    # ---------------------------------
    # REST API Operations
    # ---------------------------------
    def get_rest_operations(self):

        if not self.has_data():

            return pd.DataFrame()

        return self.df[

            self.df["path"]

            .astype(str)

            .str.contains(

                "/rest",

                case=False,

                na=False
            )
        ]

    # ---------------------------------
    # Filter by IP
    # ---------------------------------
    def filter_by_ip(

        self,

        ip
    ):

        return self.filters.by_ip(ip)

    # ---------------------------------
    # Filter by User
    # ---------------------------------
    def filter_by_user(

        self,

        user
    ):

        return self.filters.by_user(user)

    # ---------------------------------
    # Filter by Method
    # ---------------------------------
    def filter_by_method(

        self,

        method
    ):

        return self.filters.by_method(method)

    # ---------------------------------
    # Filter by Status
    # ---------------------------------
    def filter_by_status(

        self,

        status
    ):

        return self.filters.by_status(status)

    # ---------------------------------
    # Filter by Path
    # ---------------------------------
    def filter_by_path(

        self,

        path
    ):

        return self.filters.by_path(path)

    # ---------------------------------
    # Filter by Host
    # ---------------------------------
    def filter_by_host(

        self,

        host
    ):

        return self.filters.by_host(host)

    # ---------------------------------
    # Filter by Node
    # ---------------------------------
    def filter_by_node(

        self,

        node
    ):

        return self.filters.by_node(node)

    # ---------------------------------
    # Slow Requests
    # ---------------------------------
    def get_slow_requests(

        self,

        threshold_ms=1000
    ):

        return self.filters.by_resptime(

            min_resptime=threshold_ms
        )

    # ---------------------------------
    # Top Requested Paths
    # ---------------------------------
    def get_top_paths(

        self,

        limit=10
    ):

        if not self.has_data():

            return pd.DataFrame()

        return (

            self.df["path"]

            .value_counts()

            .head(limit)

            .reset_index(
                name="requests"
            )

            .rename(

                columns={

                    "index":
                    "path"
                }
            )
        )
