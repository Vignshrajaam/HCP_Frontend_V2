import pandas as pd


class HCPAccessLogInsightsService:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(

        self,

        dataframe
    ):

        self.df = dataframe

    # ---------------------------------
    # Top Client IPs
    # ---------------------------------
    def top_ips(

        self,

        limit=10
    ):

        return (

            self.df["ip"]

            .value_counts()

            .head(limit)

            .rename_axis("ip")

            .reset_index(

                name="requests"
            )
        )

    # ---------------------------------
    # Top Users
    # ---------------------------------
    def top_users(

        self,

        limit=10
    ):

        return (

            self.df["user"]

            .value_counts()

            .head(limit)

            .rename_axis("user")

            .reset_index(

                name="requests"
            )
        )

    # ---------------------------------
    # Top Tenants
    # ---------------------------------
    def top_tenants(

        self,

        limit=10
    ):

        return (

            self.df["tenant"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis("tenant")

            .reset_index(

                name="requests"
            )
        )

    # ---------------------------------
    # Top Namespaces
    # ---------------------------------
    def top_namespaces(

        self,

        limit=10
    ):

        return (

            self.df["namespace"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis("namespace")

            .reset_index(

                name="requests"
            )
        )

    # ---------------------------------
    # HTTP Methods
    # ---------------------------------
    def top_methods(self):

        return (

            self.df["method"]

            .value_counts()

            .rename_axis("method")

            .reset_index(

                name="requests"
            )
        )

    # ---------------------------------
    # Status Codes
    # ---------------------------------
    def top_status_codes(self):

        return (

            self.df["status"]

            .value_counts()

            .rename_axis("status")

            .reset_index(

                name="requests"
            )
        )

    # ---------------------------------
    # Top Response Times
    # ---------------------------------
    def get_top_responsetime(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Response Time
        # ---------------------------------
        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        # ---------------------------------
        # Remove invalid values
        # ---------------------------------
        temp = temp.dropna(
            subset=["resptime"]
        )

        # ---------------------------------
        # Sort Descending
        # ---------------------------------
        temp = temp.sort_values(

            by="resptime",

            ascending=False
        )

        # ---------------------------------
        # Select Important Columns
        # ---------------------------------
        columns = [

            "datetime",

            "ip",

            "user",

            "method",

            "path",

            "status",

            "namespace",

            "tenant",

            "protocol_type",

            "resptime",

            "node"
        ]

        return temp.reindex(
            columns=columns
        ).head(limit)



    # ---------------------------------
    # 4xx Errors
    # ---------------------------------
    def get_4xx_errors(

        self,

        limit=100
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[

            (temp["status"] >= 400)

            &

            (temp["status"] < 500)
        ]

        return temp.sort_values(

            by="datetime",

            ascending=False
        ).head(limit)


    # ---------------------------------
    # 5xx Errors
    # ---------------------------------
    def get_5xx_errors(

        self,

        limit=100
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[

            (temp["status"] >= 500)

            &

            (temp["status"] < 600)
        ]

        return temp.sort_values(

            by="datetime",

            ascending=False
        ).head(limit)

    # ---------------------------------
    # Top Failed Paths
    # ---------------------------------
    def get_top_failed_paths(

        self,

        limit=20
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[
            temp["status"] >= 400
        ]

        return (

            temp["path"]

            .value_counts()

            .head(limit)

            .rename_axis("path")

            .reset_index(

                name="failures"
            )
        )


    # ---------------------------------
    # Top Failed Tenants
    # ---------------------------------
    def get_top_failed_tenants(

        self,

        limit=20
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[
            temp["status"] >= 400
        ]

        return (

            temp["tenant"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis("tenant")

            .reset_index(

                name="failures"
            )
        )


    # ---------------------------------
    # Top Failed IPs
    # ---------------------------------
    def get_top_failed_ips(

        self,

        limit=20
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[
            temp["status"] >= 400
        ]

        return (

            temp["ip"]

            .value_counts()

            .head(limit)

            .rename_axis("ip")

            .reset_index(

                name="failures"
            )
        )
    # ---------------------------------
    # Delete Operations
    # ---------------------------------
    def get_delete_operations(

        self,

        limit=100
    ):

        temp = self.df.copy()

        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "DELETE"
        ]

        return temp.sort_values(

            by="datetime",

            ascending=False
        ).head(limit)
    
    # ---------------------------------
    # High 403 Activity
    # ---------------------------------
    def get_high_403_activity(

        self,

        limit=20
    ):

        temp = self.df.copy()

        temp = temp[
            temp["status"].astype(str) == "403"
        ]

        return (

            temp["ip"]

            .value_counts()

            .head(limit)

            .rename_axis("ip")

            .reset_index(

                name="403_count"
            )
        )
    # ---------------------------------
    # Anonymous Access
    # ---------------------------------
    def get_anonymous_access(

        self,

        limit=100
    ):

        temp = self.df.copy()

        temp = temp[

            temp["user"]

            .astype(str)

            == "-"
        ]

        return temp.sort_values(

            by="datetime",

            ascending=False
        ).head(limit)
    
    # ---------------------------------
    # Large Uploads
    # ---------------------------------
    def get_large_uploads(

        self,

        min_size=100000000,

        limit=100
    ):
        """
        Default:
        100 MB+
        """

        temp = self.df.copy()

        temp["get_size"] = pd.to_numeric(

            temp["get_size"],

            errors="coerce"
        )

        temp = temp[

            temp["get_size"] >= min_size
        ]

        return temp.sort_values(

            by="get_size",

            ascending=False
        ).head(limit)
    
    # ---------------------------------
    # Suspicious IPs
    # ---------------------------------
    def get_suspicious_ips(

        self,

        threshold=100
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[
            temp["status"] >= 400
        ]

        failed = (

            temp["ip"]

            .value_counts()

            .reset_index()
        )

        failed.columns = [

            "ip",

            "failures"
        ]

        return failed[
            failed["failures"] >= threshold
        ]
    
    # ---------------------------------
    # Slowest Requests
    # ---------------------------------
    def get_slowest_requests(

        self,

        limit=100
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["resptime"]
        )

        return temp.sort_values(

            by="resptime",

            ascending=False
        ).head(limit)
    
    # ---------------------------------
    # High Latency Paths
    # ---------------------------------
    def get_high_latency_paths(

        self,

        limit=20
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["resptime"]
        )

        result = (

            temp.groupby("path")["resptime"]

            .mean()

            .sort_values(

                ascending=False
            )

            .head(limit)

            .reset_index()
        )

        result.columns = [

            "path",

            "avg_resptime"
        ]

        return result
    
    # ---------------------------------
    # High Latency Tenants
    # ---------------------------------
    def get_high_latency_tenants(

        self,

        limit=20
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["resptime"]
        )

        result = (

            temp.groupby("tenant")["resptime"]

            .mean()

            .sort_values(

                ascending=False
            )

            .head(limit)

            .reset_index()
        )

        result.columns = [

            "tenant",

            "avg_resptime"
        ]

        return result
    
    # ---------------------------------
    # Average Response Time
    # ---------------------------------
    def get_average_response_time(

        self
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        avg_rt = temp["resptime"].mean()

        return pd.DataFrame({

            "metric": [
                "average_response_time"
            ],

            "value": [
                round(avg_rt, 2)
            ]
        })
    
    # ---------------------------------
    # Requests Per Hour
    # ---------------------------------
    def requests_per_hour(

        self
    ):

        temp = self.df.copy()

        temp["datetime"] = pd.to_datetime(

            temp["datetime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["datetime"]
        )

        temp["hour"] = temp["datetime"].dt.floor("h")

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="requests"
            )
        )

        return result.sort_values(
            by="hour"
        )
    
    # ---------------------------------
    # Requests Per Day
    # ---------------------------------
    def requests_per_day(

        self
    ):

        temp = self.df.copy()

        temp["datetime"] = pd.to_datetime(

            temp["datetime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["datetime"]
        )

        temp["day"] = temp["datetime"].dt.date

        result = (

            temp.groupby("day")

            .size()

            .reset_index(
                name="requests"
            )
        )

        return result.sort_values(
            by="day"
        )
    
    # ---------------------------------
    # Errors Over Time
    # ---------------------------------
    def errors_over_time(

        self
    ):

        temp = self.df.copy()

        temp["datetime"] = pd.to_datetime(

            temp["datetime"],

            errors="coerce"
        )

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp.dropna(

            subset=[

                "datetime",

                "status"
            ]
        )

        temp = temp[
            temp["status"] >= 400
        ]

        temp["hour"] = temp["datetime"].dt.floor("h")

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="errors"
            )
        )

        return result.sort_values(
            by="hour"
        )
    
    # ---------------------------------
    # S3 Activity Over Time
    # ---------------------------------
    def s3_activity_over_time(

        self
    ):

        temp = self.df.copy()

        temp["datetime"] = pd.to_datetime(

            temp["datetime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["datetime"]
        )

        temp = temp[
            temp["protocol_type"] == "S3"
        ]

        temp["hour"] = temp["datetime"].dt.floor("h")

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="s3_requests"
            )
        )

        return result.sort_values(
            by="hour"
        )
    
    # ---------------------------------
    # REST Activity Over Time
    # ---------------------------------
    def rest_activity_over_time(

        self
    ):

        temp = self.df.copy()

        temp["datetime"] = pd.to_datetime(

            temp["datetime"],

            errors="coerce"
        )

        temp = temp.dropna(
            subset=["datetime"]
        )

        temp = temp[
            temp["protocol_type"] == "REST"
        ]

        temp["hour"] = temp["datetime"].dt.floor("h")

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="rest_requests"
            )
        )

        return result.sort_values(
            by="hour"
        )
    
    # ---------------------------------
    # Trace IP Activity
    # ---------------------------------
    def trace_ip_activity(

        self,

        ip,

        limit=500
    ):

        temp = self.df.copy()

        temp = temp[

            temp["ip"]

            .astype(str)

            == str(ip)
        ]

        return temp.sort_values(

            by="datetime"
        ).head(limit)
    
        # ---------------------------------
    # Trace User Activity
    # ---------------------------------
    def trace_user_activity(

        self,

        user,

        limit=500
    ):

        temp = self.df.copy()

        temp = temp[

            temp["user"]

            .astype(str)

            == str(user)
        ]

        return temp.sort_values(

            by="datetime"
        ).head(limit)
    
    # ---------------------------------
    # Trace Namespace Activity
    # ---------------------------------
    def trace_namespace_activity(

        self,

        namespace,

        limit=500
    ):

        temp = self.df.copy()

        temp = temp[

            temp["namespace"]

            .astype(str)

            .str.contains(

                namespace,

                case=False,

                na=False
            )
        ]

        return temp.sort_values(

            by="datetime"
        ).head(limit)
    
    # ---------------------------------
    # Trace Object Activity
    # ---------------------------------
    def trace_object_activity(

        self,

        keyword,

        limit=500
    ):

        temp = self.df.copy()

        temp = temp[

            temp["path"]

            .astype(str)

            .str.contains(

                keyword,

                case=False,

                na=False
            )
        ]

        return temp.sort_values(

            by="datetime"
        ).head(limit)
    
    # ---------------------------------
    # 4XX Errors Over Time
    # ---------------------------------
    def errors_4xx_over_time(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Status
        # ---------------------------------
        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Filter 4XX
        # ---------------------------------
        temp = temp[

            (temp["status"] >= 400)

            &

            (temp["status"] < 500)
        ]

        # ---------------------------------
        # Group By Hour
        # ---------------------------------
        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(name="errors")
        )

        return result
    
    # ---------------------------------
    # 5XX Errors Over Time
    # ---------------------------------
    def errors_5xx_over_time(

        self
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Filter 5XX
        # ---------------------------------
        temp = temp[

            (temp["status"] >= 500)

            &

            (temp["status"] < 600)
        ]

        # ---------------------------------
        # Group By Hour
        # ---------------------------------
        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(name="errors")
        )

        return result
    
    # ---------------------------------
    # DELETE Activity Over Time
    # ---------------------------------
    def delete_activity_over_time(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Filter DELETE
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "DELETE"
        ]

        # ---------------------------------
        # Group By Hour
        # ---------------------------------
        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(name="requests")
        )

        return result
    
    # ---------------------------------
    # PUT Activity Over Time
    # ---------------------------------
    def put_activity_over_time(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Filter PUT
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "PUT"
        ]

        # ---------------------------------
        # Group By Hour
        # ---------------------------------
        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby("hour")

            .size()

            .reset_index(name="requests")
        )

        return result
    
    # ---------------------------------
    # Requests Per Node Over Time
    # ---------------------------------
    def requests_per_node_over_time(

        self
    ):

        temp = self.df.copy()

        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby([

                "hour",
                "node"

            ])

            .size()

            .reset_index(name="requests")
        )

        return result
    
    # ---------------------------------
    # Tenant Activity Over Time
    # ---------------------------------
    def tenant_activity_over_time(

        self
    ):

        temp = self.df.copy()

        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby([

                "hour",
                "tenant"

            ])

            .size()

            .reset_index(name="requests")
        )

        return result
    # ---------------------------------
    # Namespace Activity Over Time
    # ---------------------------------
    def namespace_activity_over_time(

        self
    ):

        temp = self.df.copy()

        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby([

                "hour",
                "namespace"

            ])

            .size()

            .reset_index(name="requests")
        )

        return result
    
    # ---------------------------------
    # Average Response Time Over Time
    # ---------------------------------
    def average_resptime_over_time(

        self
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        temp["hour"] = (
            temp["datetime"]
            .dt.floor("h")
        )

        result = (

            temp.groupby("hour")[

                "resptime"

            ]

            .mean()

            .reset_index()
        )

        result.rename(

            columns={

                "resptime":
                "avg_resptime"

            },

            inplace=True
        )

        return result
    
    # ---------------------------------
    # After Hours Activity
    # ---------------------------------
    def after_hours_activity(

        self
    ):

        temp = self.df.copy()

        temp["hour_of_day"] = (
            temp["datetime"]
            .dt.hour
        )

        # ---------------------------------
        # After Hours Filter
        # ---------------------------------
        temp = temp[

            (temp["hour_of_day"] < 8)

            |

            (temp["hour_of_day"] > 18)
        ]

        result = (

            temp.groupby(

                "hour_of_day"

            )

            .size()

            .reset_index(name="requests")
        )

        return result
    # ---------------------------------
    # Top Tenant Reads
    # ---------------------------------
    def top_tenants_reads(

        self,

        limit=10
    ):

        temp = self.df.copy()

        # ---------------------------------
        # GET + HEAD = Reads
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            .isin([

                "GET",

                "HEAD"
            ])
        ]

        return (

            temp["tenant"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "tenant"
            )

            .reset_index(

                name="requests"
            )
        )
    
    # ---------------------------------
    # Top Tenant Writes
    # ---------------------------------
    def top_tenants_writes(

        self,

        limit=10
    ):

        temp = self.df.copy()

        # ---------------------------------
        # PUT = Write Activity
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "PUT"
        ]

        return (

            temp["tenant"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "tenant"
            )

            .reset_index(

                name="requests"
            )
        )
    
    # ---------------------------------
    # Top IP Reads
    # ---------------------------------
    def top_ips_reads(

        self,

        limit=10
    ):

        temp = self.df.copy()

        # ---------------------------------
        # GET + HEAD = Read Activity
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            .isin([

                "GET",

                "HEAD"
            ])
        ]

        return (

            temp["ip"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "ip"
            )

            .reset_index(

                name="requests"
            )
        )
    
    # ---------------------------------
    # Top IPS Writes
    # ---------------------------------
    def top_ips_writes(

        self,

        limit=10
    ):

        temp = self.df.copy()

        # ---------------------------------
        # PUT = Write Activity
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "PUT"
        ]

        return (

            temp["ip"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "ip"
            )

            .reset_index(

                name="requests"
            )
        )
    # ---------------------------------
    # Top Extensions
    # ---------------------------------
    def top_extensions(

        self,

        limit=10
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Normalize Path
        # ---------------------------------
        temp["clean_path"] = (

            temp["path"]

            .astype(str)

            .str.split("?")

            .str[0]

            .str.lower()
        )

        # ---------------------------------
        # Known Compound Extensions
        # ---------------------------------
        compound_ext = [

            "tar.gz",

            "tar.xz",

            "tar.bz2"
        ]

        def extract_extension(path):

            for ext in compound_ext:

                if path.endswith(

                    "." + ext
                ):

                    return ext

            # ---------------------------------
            # Standard Extension
            # ---------------------------------
            if "." in path:

                return (

                    path.split(".")[-1]
                )

            return "unknown"

        temp["extension"] = (

            temp["clean_path"]

            .apply(

                extract_extension
            )
        )

        return (

            temp["extension"]

            .value_counts()

            .head(limit)

            .rename_axis(

                "extension"
            )

            .reset_index(

                name="requests"
            )
        )
    
    # ---------------------------------
    # Top Users with 403 Errors
    # ---------------------------------
    def top_403_users(
        self,
        limit=10
    ):
        temp = self.df.copy()

        # ---------------------------------
        # Filter only 403 status
        # ---------------------------------
        temp = temp[
            temp["status"] == 403
        ]

        # ---------------------------------
        # Count by user
        # ---------------------------------
        result = (
            temp["user"]
            .value_counts()
            .head(limit)
            .reset_index()
        )

        # ---------------------------------
        # Rename columns
        # ---------------------------------
        result.columns = [
            "user",
            "403_count"
        ]

        return result
    # ---------------------------------
    # Top 404 Objects
    # ---------------------------------
    def top_404_objects(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Status
        # ---------------------------------
        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Filter 404
        # ---------------------------------
        temp = temp[

            temp["status"]

            == 404
        ]

        return (

            temp["path"]

            .value_counts()

            .head(limit)

            .rename_axis(

                "path"
            )

            .reset_index(

                name="failures"
            )
        )
    
    # ---------------------------------
    # Error Rate By Tenant
    # ---------------------------------
    def error_rate_by_tenant(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Status
        # ---------------------------------
        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Total Requests Per Tenant
        # ---------------------------------
        total_requests = (

            temp.groupby(

                "tenant"
            )

            .size()

            .reset_index(

                name="total_requests"
            )
        )

        # ---------------------------------
        # Failed Requests (4XX + 5XX)
        # ---------------------------------
        failed_requests = (

            temp[

                temp["status"]

                >= 400
            ]

            .groupby(

                "tenant"
            )

            .size()

            .reset_index(

                name="failed_requests"
            )
        )

        # ---------------------------------
        # Merge
        # ---------------------------------
        result = total_requests.merge(

            failed_requests,

            on="tenant",

            how="left"
        )

        result["failed_requests"] = (

            result["failed_requests"]

            .fillna(0)
        )

        # ---------------------------------
        # Error Rate %
        # ---------------------------------
        result["error_rate_pct"] = (

            result["failed_requests"]

            /

            result["total_requests"]

            * 100
        ).round(2)

        # ---------------------------------
        # Sort By Error Rate
        # ---------------------------------
        result = result.sort_values(

            by="error_rate_pct",

            ascending=False
        )

        return result.head(limit)
    

    # ---------------------------------
    # Failure Percentage
    # ---------------------------------
    def failure_percentage(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Status
        # ---------------------------------
        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Total Requests
        # ---------------------------------
        total_requests = len(

            temp
        )

        # ---------------------------------
        # Failed Requests
        # ---------------------------------
        failed_requests = len(

            temp[

                temp["status"]

                >= 400
            ]
        )

        # ---------------------------------
        # Failure %
        # ---------------------------------
        failure_pct = round(

            (

                failed_requests

                /

                total_requests

            )

            * 100,

            2
        )

        return pd.DataFrame([

            {

                "total_requests":
                    total_requests,

                "failed_requests":
                    failed_requests,

                "failure_percentage":
                    failure_pct
            }
        ])
    
    # ---------------------------------
    # High 403 Activity
    # ---------------------------------
    def get_high_403_activity(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Status
        # ---------------------------------
        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Filter 403
        # ---------------------------------
        temp = temp[

            temp["status"]

            == 403
        ]

        return (

            temp["user"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "user"
            )

            .reset_index(

                name="failures"
            )
        )
    
    # ---------------------------------
    # Large Uploads
    # ---------------------------------
    def get_large_uploads(

        self,

        min_size_mb=100,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # PUT Only
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "PUT"
        ]

        # ---------------------------------
        # Convert PUT Size
        # ---------------------------------
        temp["put_size"] = pd.to_numeric(

            temp["put_size"],

            errors="coerce"
        ).fillna(0)

        # ---------------------------------
        # Threshold
        # ---------------------------------
        min_size_bytes = (

            min_size_mb

            * 1024

            * 1024
        )

        temp = temp[

            temp["put_size"]

            >= min_size_bytes
        ]

        # ---------------------------------
        # Human Readable Size
        # ---------------------------------
        temp["size_mb"] = (

            temp["put_size"]

            /

            (1024 ** 2)

        ).round(2)

        return (

            temp[

                [

                    "datetime",

                    "tenant",

                    "namespace",

                    "user",

                    "ip",

                    "path",

                    "size_mb"
                ]
            ]

            .sort_values(

                by="size_mb",

                ascending=False
            )

            .head(limit)

            .reset_index(

                drop=True
            )
        )
    
    # ---------------------------------
    # Failed Login Patterns
    # ---------------------------------
    def get_failed_login_patterns(

        self,

        threshold=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Status
        # ---------------------------------
        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        # ---------------------------------
        # Authentication Failures
        # ---------------------------------
        temp = temp[

            temp["status"]

            .isin([

                401,

                403
            ])
        ]

        if temp.empty:

            return pd.DataFrame()

        # ---------------------------------
        # Group Per Hour
        # ---------------------------------
        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        result = (

            temp.groupby(

                [

                    "hour",

                    "user",

                    "ip",

                    "tenant"
                ]
            )

            .size()

            .reset_index(

                name="failures"
            )
        )

        # ---------------------------------
        # Threshold Filter
        # ---------------------------------
        result = result[

            result["failures"]

            >= threshold
        ]

        return (

            result

            .sort_values(

                by="failures",

                ascending=False
            )

            .reset_index(

                drop=True
            )
        )
    
    # ---------------------------------
    # Delete Activity By Tenant
    # ---------------------------------
    def get_delete_by_tenant(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # DELETE Only
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "DELETE"
        ]

        return (

            temp["tenant"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "tenant"
            )

            .reset_index(

                name="deletes"
            )
        )
    
    # ---------------------------------
    # Delete Activity By User
    # ---------------------------------
    def get_delete_by_user(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # DELETE Only
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "DELETE"
        ]

        return (

            temp["user"]

            .dropna()

            .value_counts()

            .head(limit)

            .rename_axis(

                "user"
            )

            .reset_index(

                name="deletes"
            )
        )
    
    # ---------------------------------
    # High Latency Nodes
    # ---------------------------------
    def get_high_latency_nodes(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Convert Response Time
        # ---------------------------------
        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        # ---------------------------------
        # Remove Nulls
        # ---------------------------------
        temp = temp.dropna(

            subset=[

                "resptime",

                "node"
            ]
        )

        result = (

            temp.groupby(

                "node"
            )["resptime"]

            .mean()

            .reset_index()
        )

        result["avg_resptime_ms"] = (

            result["resptime"]

            .round(2)
        )

        return (

            result[

                [

                    "node",

                    "avg_resptime_ms"
                ]
            ]

            .sort_values(

                by="avg_resptime_ms",

                ascending=False
            )

            .head(limit)

            .reset_index(

                drop=True
            )
        )
    
    # ---------------------------------
    # High Request Nodes
    # ---------------------------------
    def get_high_requests_nodes(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Remove Missing Nodes
        # ---------------------------------
        temp = temp.dropna(

            subset=[

                "node"
            ]
        )

        return (

            temp["node"]

            .value_counts()

            .head(limit)

            .rename_axis(

                "node"
            )

            .reset_index(

                name="requests"
            )
        )
    
    # ---------------------------------
    # Slow PUT Requests
    # ---------------------------------
    def slow_puts(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # PUT Only
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            == "PUT"
        ]

        # ---------------------------------
        # Convert Response Time
        # ---------------------------------
        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        temp = temp.dropna(

            subset=[

                "resptime"
            ]
        )

        return (

            temp[

                [

                    "datetime",

                    "tenant",

                    "namespace",

                    "user",

                    "ip",

                    "node",

                    "path",

                    "put_size",

                    "resptime"
                ]
            ]

            .sort_values(

                by="resptime",

                ascending=False
            )

            .head(limit)

            .reset_index(

                drop=True
            )
        )
    
    # ---------------------------------
    # Slow GET Requests
    # ---------------------------------
    def slow_gets(

        self,

        limit=20
    ):

        temp = self.df.copy()

        # ---------------------------------
        # GET + HEAD
        # ---------------------------------
        temp = temp[

            temp["method"]

            .astype(str)

            .str.upper()

            .isin([

                "GET",

                "HEAD"
            ])
        ]

        # ---------------------------------
        # Convert Response Time
        # ---------------------------------
        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        temp = temp.dropna(

            subset=[

                "resptime"
            ]
        )

        return (

            temp[

                [

                    "datetime",

                    "tenant",

                    "namespace",

                    "user",

                    "ip",

                    "node",

                    "path",

                    "get_size",

                    "resptime"
                ]
            ]

            .sort_values(

                by="resptime",

                ascending=False
            )

            .head(limit)

            .reset_index(

                drop=True
            )
        )