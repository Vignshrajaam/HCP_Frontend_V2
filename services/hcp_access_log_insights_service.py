# import pandas as pd


# class HCPAccessLogInsightsService:

#     # ---------------------------------
#     # Init
#     # ---------------------------------
#     def __init__(

#         self,

#         dataframe
#     ):

#         self.df = dataframe

#     # ---------------------------------
#     # Top Client IPs
#     # ---------------------------------
#     def top_ips(

#         self,

#         limit=10
#     ):

#         return (

#             self.df["ip"]

#             .value_counts()

#             .head(limit)

#             .rename_axis("ip")

#             .reset_index(

#                 name="requests"
#             )
#         )

#     # ---------------------------------
#     # Top Users
#     # ---------------------------------
#     def top_users(

#         self,

#         limit=10
#     ):

#         return (

#             self.df["user"]

#             .value_counts()

#             .head(limit)

#             .rename_axis("user")

#             .reset_index(

#                 name="requests"
#             )
#         )

#     # ---------------------------------
#     # Top Tenants
#     # ---------------------------------
#     def top_tenants(

#         self,

#         limit=10
#     ):

#         return (

#             self.df["tenant"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis("tenant")

#             .reset_index(

#                 name="requests"
#             )
#         )

#     # ---------------------------------
#     # Top Namespaces
#     # ---------------------------------
#     def top_namespaces(

#         self,

#         limit=10
#     ):

#         return (

#             self.df["namespace"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis("namespace")

#             .reset_index(

#                 name="requests"
#             )
#         )

#     # ---------------------------------
#     # HTTP Methods
#     # ---------------------------------
#     def top_methods(self):

#         return (

#             self.df["method"]

#             .value_counts()

#             .rename_axis("method")

#             .reset_index(

#                 name="requests"
#             )
#         )

#     # ---------------------------------
#     # Status Codes
#     # ---------------------------------
#     def top_status_codes(self):

#         return (

#             self.df["status"]

#             .value_counts()

#             .rename_axis("status")

#             .reset_index(

#                 name="requests"
#             )
#         )

#     # ---------------------------------
#     # Top Response Times
#     # ---------------------------------
#     def get_top_responsetime(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Response Time
#         # ---------------------------------
#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Remove invalid values
#         # ---------------------------------
#         temp = temp.dropna(
#             subset=["resptime"]
#         )

#         # ---------------------------------
#         # Sort Descending
#         # ---------------------------------
#         temp = temp.sort_values(

#             by="resptime",

#             ascending=False
#         )

#         # ---------------------------------
#         # Select Important Columns
#         # ---------------------------------
#         columns = [

#             "datetime",

#             "ip",

#             "user",

#             "method",

#             "path",

#             "status",

#             "namespace",

#             "tenant",

#             "protocol_type",

#             "resptime",

#             "node"
#         ]

#         return temp.reindex(
#             columns=columns
#         ).head(limit)



#     # ---------------------------------
#     # 4xx Errors
#     # ---------------------------------
#     def get_4xx_errors(

#         self,

#         limit=100
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp[

#             (temp["status"] >= 400)

#             &

#             (temp["status"] < 500)
#         ]

#         return temp.sort_values(

#             by="datetime",

#             ascending=False
#         ).head(limit)


#     # ---------------------------------
#     # 5xx Errors
#     # ---------------------------------
#     def get_5xx_errors(

#         self,

#         limit=100
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp[

#             (temp["status"] >= 500)

#             &

#             (temp["status"] < 600)
#         ]

#         return temp.sort_values(

#             by="datetime",

#             ascending=False
#         ).head(limit)

#     # ---------------------------------
#     # Top Failed Paths
#     # ---------------------------------
#     def get_top_failed_paths(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp[
#             temp["status"] >= 400
#         ]

#         return (

#             temp["path"]

#             .value_counts()

#             .head(limit)

#             .rename_axis("path")

#             .reset_index(

#                 name="failures"
#             )
#         )


#     # ---------------------------------
#     # Top Failed Tenants
#     # ---------------------------------
#     def get_top_failed_tenants(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp[
#             temp["status"] >= 400
#         ]

#         return (

#             temp["tenant"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis("tenant")

#             .reset_index(

#                 name="failures"
#             )
#         )


#     # ---------------------------------
#     # Top Failed IPs
#     # ---------------------------------
#     def get_top_failed_ips(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp[
#             temp["status"] >= 400
#         ]

#         return (

#             temp["ip"]

#             .value_counts()

#             .head(limit)

#             .rename_axis("ip")

#             .reset_index(

#                 name="failures"
#             )
#         )
#     # ---------------------------------
#     # Delete Operations
#     # ---------------------------------
#     def get_delete_operations(

#         self,

#         limit=100
#     ):

#         temp = self.df.copy()

#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "DELETE"
#         ]

#         return temp.sort_values(

#             by="datetime",

#             ascending=False
#         ).head(limit)
    
#     # ---------------------------------
#     # High 403 Activity
#     # ---------------------------------
#     def get_high_403_activity(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         temp = temp[
#             temp["status"].astype(str) == "403"
#         ]

#         return (

#             temp["ip"]

#             .value_counts()

#             .head(limit)

#             .rename_axis("ip")

#             .reset_index(

#                 name="403_count"
#             )
#         )
#     # ---------------------------------
#     # Anonymous Access
#     # ---------------------------------
#     def get_anonymous_access(

#         self,

#         limit=100
#     ):

#         temp = self.df.copy()

#         temp = temp[

#             temp["user"]

#             .astype(str)

#             == "-"
#         ]

#         return temp.sort_values(

#             by="datetime",

#             ascending=False
#         ).head(limit)
    
#     # ---------------------------------
#     # Large Uploads
#     # ---------------------------------
#     def get_large_uploads(

#         self,

#         min_size=100000000,

#         limit=100
#     ):
#         """
#         Default:
#         100 MB+
#         """

#         temp = self.df.copy()

#         temp["get_size"] = pd.to_numeric(

#             temp["get_size"],

#             errors="coerce"
#         )

#         temp = temp[

#             temp["get_size"] >= min_size
#         ]

#         return temp.sort_values(

#             by="get_size",

#             ascending=False
#         ).head(limit)
    
#     # ---------------------------------
#     # Suspicious IPs
#     # ---------------------------------
#     def get_suspicious_ips(

#         self,

#         threshold=100
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp[
#             temp["status"] >= 400
#         ]

#         failed = (

#             temp["ip"]

#             .value_counts()

#             .reset_index()
#         )

#         failed.columns = [

#             "ip",

#             "failures"
#         ]

#         return failed[
#             failed["failures"] >= threshold
#         ]
    
#     # ---------------------------------
#     # Slowest Requests
#     # ---------------------------------
#     def get_slowest_requests(

#         self,

#         limit=100
#     ):

#         temp = self.df.copy()

#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["resptime"]
#         )

#         return temp.sort_values(

#             by="resptime",

#             ascending=False
#         ).head(limit)
    
#     # ---------------------------------
#     # High Latency Paths
#     # ---------------------------------
#     def get_high_latency_paths(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["resptime"]
#         )

#         result = (

#             temp.groupby("path")["resptime"]

#             .mean()

#             .sort_values(

#                 ascending=False
#             )

#             .head(limit)

#             .reset_index()
#         )

#         result.columns = [

#             "path",

#             "avg_resptime"
#         ]

#         return result
    
#     # ---------------------------------
#     # High Latency Tenants
#     # ---------------------------------
#     def get_high_latency_tenants(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["resptime"]
#         )

#         result = (

#             temp.groupby("tenant")["resptime"]

#             .mean()

#             .sort_values(

#                 ascending=False
#             )

#             .head(limit)

#             .reset_index()
#         )

#         result.columns = [

#             "tenant",

#             "avg_resptime"
#         ]

#         return result
    
#     # ---------------------------------
#     # Average Response Time
#     # ---------------------------------
#     def get_average_response_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         avg_rt = temp["resptime"].mean()

#         return pd.DataFrame({

#             "metric": [
#                 "average_response_time"
#             ],

#             "value": [
#                 round(avg_rt, 2)
#             ]
#         })
    
#     # ---------------------------------
#     # Requests Per Hour
#     # ---------------------------------
#     def requests_per_hour(

#         self
#     ):

#         temp = self.df.copy()

#         temp["datetime"] = pd.to_datetime(

#             temp["datetime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["datetime"]
#         )

#         temp["hour"] = temp["datetime"].dt.floor("h")

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(
#                 name="requests"
#             )
#         )

#         return result.sort_values(
#             by="hour"
#         )
    
#     # ---------------------------------
#     # Requests Per Day
#     # ---------------------------------
#     def requests_per_day(

#         self
#     ):

#         temp = self.df.copy()

#         temp["datetime"] = pd.to_datetime(

#             temp["datetime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["datetime"]
#         )

#         temp["day"] = temp["datetime"].dt.date

#         result = (

#             temp.groupby("day")

#             .size()

#             .reset_index(
#                 name="requests"
#             )
#         )

#         return result.sort_values(
#             by="day"
#         )
    
#     # ---------------------------------
#     # Errors Over Time
#     # ---------------------------------
#     def errors_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["datetime"] = pd.to_datetime(

#             temp["datetime"],

#             errors="coerce"
#         )

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         temp = temp.dropna(

#             subset=[

#                 "datetime",

#                 "status"
#             ]
#         )

#         temp = temp[
#             temp["status"] >= 400
#         ]

#         temp["hour"] = temp["datetime"].dt.floor("h")

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(
#                 name="errors"
#             )
#         )

#         return result.sort_values(
#             by="hour"
#         )
    
#     # ---------------------------------
#     # S3 Activity Over Time
#     # ---------------------------------
#     def s3_activity_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["datetime"] = pd.to_datetime(

#             temp["datetime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["datetime"]
#         )

#         temp = temp[
#             temp["protocol_type"] == "S3"
#         ]

#         temp["hour"] = temp["datetime"].dt.floor("h")

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(
#                 name="s3_requests"
#             )
#         )

#         return result.sort_values(
#             by="hour"
#         )
    
#     # ---------------------------------
#     # REST Activity Over Time
#     # ---------------------------------
#     def rest_activity_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["datetime"] = pd.to_datetime(

#             temp["datetime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(
#             subset=["datetime"]
#         )

#         temp = temp[
#             temp["protocol_type"] == "REST"
#         ]

#         temp["hour"] = temp["datetime"].dt.floor("h")

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(
#                 name="rest_requests"
#             )
#         )

#         return result.sort_values(
#             by="hour"
#         )
    
#     # ---------------------------------
#     # Trace IP Activity
#     # ---------------------------------
#     def trace_ip_activity(

#         self,

#         ip,

#         limit=500
#     ):

#         temp = self.df.copy()

#         temp = temp[

#             temp["ip"]

#             .astype(str)

#             == str(ip)
#         ]

#         return temp.sort_values(

#             by="datetime"
#         ).head(limit)
    
#         # ---------------------------------
#     # Trace User Activity
#     # ---------------------------------
#     def trace_user_activity(

#         self,

#         user,

#         limit=500
#     ):

#         temp = self.df.copy()

#         temp = temp[

#             temp["user"]

#             .astype(str)

#             == str(user)
#         ]

#         return temp.sort_values(

#             by="datetime"
#         ).head(limit)
    
#     # ---------------------------------
#     # Trace Namespace Activity
#     # ---------------------------------
#     def trace_namespace_activity(

#         self,

#         namespace,

#         limit=500
#     ):

#         temp = self.df.copy()

#         temp = temp[

#             temp["namespace"]

#             .astype(str)

#             .str.contains(

#                 namespace,

#                 case=False,

#                 na=False
#             )
#         ]

#         return temp.sort_values(

#             by="datetime"
#         ).head(limit)
    
#     # ---------------------------------
#     # Trace Object Activity
#     # ---------------------------------
#     def trace_object_activity(

#         self,

#         keyword,

#         limit=500
#     ):

#         temp = self.df.copy()

#         temp = temp[

#             temp["path"]

#             .astype(str)

#             .str.contains(

#                 keyword,

#                 case=False,

#                 na=False
#             )
#         ]

#         return temp.sort_values(

#             by="datetime"
#         ).head(limit)
    
#     # ---------------------------------
#     # 4XX Errors Over Time
#     # ---------------------------------
#     def errors_4xx_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Status
#         # ---------------------------------
#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Filter 4XX
#         # ---------------------------------
#         temp = temp[

#             (temp["status"] >= 400)

#             &

#             (temp["status"] < 500)
#         ]

#         # ---------------------------------
#         # Group By Hour
#         # ---------------------------------
#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(name="errors")
#         )

#         return result
    
#     # ---------------------------------
#     # 5XX Errors Over Time
#     # ---------------------------------
#     def errors_5xx_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Filter 5XX
#         # ---------------------------------
#         temp = temp[

#             (temp["status"] >= 500)

#             &

#             (temp["status"] < 600)
#         ]

#         # ---------------------------------
#         # Group By Hour
#         # ---------------------------------
#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(name="errors")
#         )

#         return result
    
#     # ---------------------------------
#     # DELETE Activity Over Time
#     # ---------------------------------
#     def delete_activity_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Filter DELETE
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "DELETE"
#         ]

#         # ---------------------------------
#         # Group By Hour
#         # ---------------------------------
#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(name="requests")
#         )

#         return result
    
#     # ---------------------------------
#     # PUT Activity Over Time
#     # ---------------------------------
#     def put_activity_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Filter PUT
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "PUT"
#         ]

#         # ---------------------------------
#         # Group By Hour
#         # ---------------------------------
#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby("hour")

#             .size()

#             .reset_index(name="requests")
#         )

#         return result
    
#     # ---------------------------------
#     # Requests Per Node Over Time
#     # ---------------------------------
#     def requests_per_node_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby([

#                 "hour",
#                 "node"

#             ])

#             .size()

#             .reset_index(name="requests")
#         )

#         return result
    
#     # ---------------------------------
#     # Tenant Activity Over Time
#     # ---------------------------------
#     def tenant_activity_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby([

#                 "hour",
#                 "tenant"

#             ])

#             .size()

#             .reset_index(name="requests")
#         )

#         return result
#     # ---------------------------------
#     # Namespace Activity Over Time
#     # ---------------------------------
#     def namespace_activity_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby([

#                 "hour",
#                 "namespace"

#             ])

#             .size()

#             .reset_index(name="requests")
#         )

#         return result
    
#     # ---------------------------------
#     # Average Response Time Over Time
#     # ---------------------------------
#     def average_resptime_over_time(

#         self
#     ):

#         temp = self.df.copy()

#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         temp["hour"] = (
#             temp["datetime"]
#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby("hour")[

#                 "resptime"

#             ]

#             .mean()

#             .reset_index()
#         )

#         result.rename(

#             columns={

#                 "resptime":
#                 "avg_resptime"

#             },

#             inplace=True
#         )

#         return result
    
#     # ---------------------------------
#     # After Hours Activity
#     # ---------------------------------
#     def after_hours_activity(

#         self
#     ):

#         temp = self.df.copy()

#         temp["hour_of_day"] = (
#             temp["datetime"]
#             .dt.hour
#         )

#         # ---------------------------------
#         # After Hours Filter
#         # ---------------------------------
#         temp = temp[

#             (temp["hour_of_day"] < 8)

#             |

#             (temp["hour_of_day"] > 18)
#         ]

#         result = (

#             temp.groupby(

#                 "hour_of_day"

#             )

#             .size()

#             .reset_index(name="requests")
#         )

#         return result
#     # ---------------------------------
#     # Top Tenant Reads
#     # ---------------------------------
#     def top_tenants_reads(

#         self,

#         limit=10
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # GET + HEAD = Reads
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             .isin([

#                 "GET",

#                 "HEAD"
#             ])
#         ]

#         return (

#             temp["tenant"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "tenant"
#             )

#             .reset_index(

#                 name="requests"
#             )
#         )
    
#     # ---------------------------------
#     # Top Tenant Writes
#     # ---------------------------------
#     def top_tenants_writes(

#         self,

#         limit=10
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # PUT = Write Activity
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "PUT"
#         ]

#         return (

#             temp["tenant"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "tenant"
#             )

#             .reset_index(

#                 name="requests"
#             )
#         )
    
#     # ---------------------------------
#     # Top IP Reads
#     # ---------------------------------
#     def top_ips_reads(

#         self,

#         limit=10
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # GET + HEAD = Read Activity
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             .isin([

#                 "GET",

#                 "HEAD"
#             ])
#         ]

#         return (

#             temp["ip"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "ip"
#             )

#             .reset_index(

#                 name="requests"
#             )
#         )
    
#     # ---------------------------------
#     # Top IPS Writes
#     # ---------------------------------
#     def top_ips_writes(

#         self,

#         limit=10
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # PUT = Write Activity
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "PUT"
#         ]

#         return (

#             temp["ip"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "ip"
#             )

#             .reset_index(

#                 name="requests"
#             )
#         )
#     # ---------------------------------
#     # Top Extensions
#     # ---------------------------------
#     def top_extensions(

#         self,

#         limit=10
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Normalize Path
#         # ---------------------------------
#         temp["clean_path"] = (

#             temp["path"]

#             .astype(str)

#             .str.split("?")

#             .str[0]

#             .str.lower()
#         )

#         # ---------------------------------
#         # Known Compound Extensions
#         # ---------------------------------
#         compound_ext = [

#             "tar.gz",

#             "tar.xz",

#             "tar.bz2"
#         ]

#         def extract_extension(path):

#             for ext in compound_ext:

#                 if path.endswith(

#                     "." + ext
#                 ):

#                     return ext

#             # ---------------------------------
#             # Standard Extension
#             # ---------------------------------
#             if "." in path:

#                 return (

#                     path.split(".")[-1]
#                 )

#             return "unknown"

#         temp["extension"] = (

#             temp["clean_path"]

#             .apply(

#                 extract_extension
#             )
#         )

#         return (

#             temp["extension"]

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "extension"
#             )

#             .reset_index(

#                 name="requests"
#             )
#         )
    
#     # ---------------------------------
#     # Top Users with 403 Errors
#     # ---------------------------------
#     def top_403_users(
#         self,
#         limit=10
#     ):
#         temp = self.df.copy()

#         # ---------------------------------
#         # Filter only 403 status
#         # ---------------------------------
#         temp = temp[
#             temp["status"] == 403
#         ]

#         # ---------------------------------
#         # Count by user
#         # ---------------------------------
#         result = (
#             temp["user"]
#             .value_counts()
#             .head(limit)
#             .reset_index()
#         )

#         # ---------------------------------
#         # Rename columns
#         # ---------------------------------
#         result.columns = [
#             "user",
#             "403_count"
#         ]

#         return result
#     # ---------------------------------
#     # Top 404 Objects
#     # ---------------------------------
#     def top_404_objects(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Status
#         # ---------------------------------
#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Filter 404
#         # ---------------------------------
#         temp = temp[

#             temp["status"]

#             == 404
#         ]

#         return (

#             temp["path"]

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "path"
#             )

#             .reset_index(

#                 name="failures"
#             )
#         )
    
#     # ---------------------------------
#     # Error Rate By Tenant
#     # ---------------------------------
#     def error_rate_by_tenant(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Status
#         # ---------------------------------
#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Total Requests Per Tenant
#         # ---------------------------------
#         total_requests = (

#             temp.groupby(

#                 "tenant"
#             )

#             .size()

#             .reset_index(

#                 name="total_requests"
#             )
#         )

#         # ---------------------------------
#         # Failed Requests (4XX + 5XX)
#         # ---------------------------------
#         failed_requests = (

#             temp[

#                 temp["status"]

#                 >= 400
#             ]

#             .groupby(

#                 "tenant"
#             )

#             .size()

#             .reset_index(

#                 name="failed_requests"
#             )
#         )

#         # ---------------------------------
#         # Merge
#         # ---------------------------------
#         result = total_requests.merge(

#             failed_requests,

#             on="tenant",

#             how="left"
#         )

#         result["failed_requests"] = (

#             result["failed_requests"]

#             .fillna(0)
#         )

#         # ---------------------------------
#         # Error Rate %
#         # ---------------------------------
#         result["error_rate_pct"] = (

#             result["failed_requests"]

#             /

#             result["total_requests"]

#             * 100
#         ).round(2)

#         # ---------------------------------
#         # Sort By Error Rate
#         # ---------------------------------
#         result = result.sort_values(

#             by="error_rate_pct",

#             ascending=False
#         )

#         return result.head(limit)
    

#     # ---------------------------------
#     # Failure Percentage
#     # ---------------------------------
#     def failure_percentage(

#         self
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Status
#         # ---------------------------------
#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Total Requests
#         # ---------------------------------
#         total_requests = len(

#             temp
#         )

#         # ---------------------------------
#         # Failed Requests
#         # ---------------------------------
#         failed_requests = len(

#             temp[

#                 temp["status"]

#                 >= 400
#             ]
#         )

#         # ---------------------------------
#         # Failure %
#         # ---------------------------------
#         failure_pct = round(

#             (

#                 failed_requests

#                 /

#                 total_requests

#             )

#             * 100,

#             2
#         )

#         return pd.DataFrame([

#             {

#                 "total_requests":
#                     total_requests,

#                 "failed_requests":
#                     failed_requests,

#                 "failure_percentage":
#                     failure_pct
#             }
#         ])
    
#     # ---------------------------------
#     # High 403 Activity
#     # ---------------------------------
#     def get_high_403_activity(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Status
#         # ---------------------------------
#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Filter 403
#         # ---------------------------------
#         temp = temp[

#             temp["status"]

#             == 403
#         ]

#         return (

#             temp["user"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "user"
#             )

#             .reset_index(

#                 name="failures"
#             )
#         )
    
#     # ---------------------------------
#     # Large Uploads
#     # ---------------------------------
#     def get_large_uploads(

#         self,

#         min_size_mb=100,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # PUT Only
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "PUT"
#         ]

#         # ---------------------------------
#         # Convert PUT Size
#         # ---------------------------------
#         temp["put_size"] = pd.to_numeric(

#             temp["put_size"],

#             errors="coerce"
#         ).fillna(0)

#         # ---------------------------------
#         # Threshold
#         # ---------------------------------
#         min_size_bytes = (

#             min_size_mb

#             * 1024

#             * 1024
#         )

#         temp = temp[

#             temp["put_size"]

#             >= min_size_bytes
#         ]

#         # ---------------------------------
#         # Human Readable Size
#         # ---------------------------------
#         temp["size_mb"] = (

#             temp["put_size"]

#             /

#             (1024 ** 2)

#         ).round(2)

#         return (

#             temp[

#                 [

#                     "datetime",

#                     "tenant",

#                     "namespace",

#                     "user",

#                     "ip",

#                     "path",

#                     "size_mb"
#                 ]
#             ]

#             .sort_values(

#                 by="size_mb",

#                 ascending=False
#             )

#             .head(limit)

#             .reset_index(

#                 drop=True
#             )
#         )
    
#     # ---------------------------------
#     # Failed Login Patterns
#     # ---------------------------------
#     def get_failed_login_patterns(

#         self,

#         threshold=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Status
#         # ---------------------------------
#         temp["status"] = pd.to_numeric(

#             temp["status"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Authentication Failures
#         # ---------------------------------
#         temp = temp[

#             temp["status"]

#             .isin([

#                 401,

#                 403
#             ])
#         ]

#         if temp.empty:

#             return pd.DataFrame()

#         # ---------------------------------
#         # Group Per Hour
#         # ---------------------------------
#         temp["hour"] = (

#             temp["datetime"]

#             .dt.floor("h")
#         )

#         result = (

#             temp.groupby(

#                 [

#                     "hour",

#                     "user",

#                     "ip",

#                     "tenant"
#                 ]
#             )

#             .size()

#             .reset_index(

#                 name="failures"
#             )
#         )

#         # ---------------------------------
#         # Threshold Filter
#         # ---------------------------------
#         result = result[

#             result["failures"]

#             >= threshold
#         ]

#         return (

#             result

#             .sort_values(

#                 by="failures",

#                 ascending=False
#             )

#             .reset_index(

#                 drop=True
#             )
#         )
    
#     # ---------------------------------
#     # Delete Activity By Tenant
#     # ---------------------------------
#     def get_delete_by_tenant(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # DELETE Only
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "DELETE"
#         ]

#         return (

#             temp["tenant"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "tenant"
#             )

#             .reset_index(

#                 name="deletes"
#             )
#         )
    
#     # ---------------------------------
#     # Delete Activity By User
#     # ---------------------------------
#     def get_delete_by_user(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # DELETE Only
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "DELETE"
#         ]

#         return (

#             temp["user"]

#             .dropna()

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "user"
#             )

#             .reset_index(

#                 name="deletes"
#             )
#         )
    
#     # ---------------------------------
#     # High Latency Nodes
#     # ---------------------------------
#     def get_high_latency_nodes(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Convert Response Time
#         # ---------------------------------
#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         # ---------------------------------
#         # Remove Nulls
#         # ---------------------------------
#         temp = temp.dropna(

#             subset=[

#                 "resptime",

#                 "node"
#             ]
#         )

#         result = (

#             temp.groupby(

#                 "node"
#             )["resptime"]

#             .mean()

#             .reset_index()
#         )

#         result["avg_resptime_ms"] = (

#             result["resptime"]

#             .round(2)
#         )

#         return (

#             result[

#                 [

#                     "node",

#                     "avg_resptime_ms"
#                 ]
#             ]

#             .sort_values(

#                 by="avg_resptime_ms",

#                 ascending=False
#             )

#             .head(limit)

#             .reset_index(

#                 drop=True
#             )
#         )
    
#     # ---------------------------------
#     # High Request Nodes
#     # ---------------------------------
#     def get_high_requests_nodes(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # Remove Missing Nodes
#         # ---------------------------------
#         temp = temp.dropna(

#             subset=[

#                 "node"
#             ]
#         )

#         return (

#             temp["node"]

#             .value_counts()

#             .head(limit)

#             .rename_axis(

#                 "node"
#             )

#             .reset_index(

#                 name="requests"
#             )
#         )
    
#     # ---------------------------------
#     # Slow PUT Requests
#     # ---------------------------------
#     def slow_puts(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # PUT Only
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             == "PUT"
#         ]

#         # ---------------------------------
#         # Convert Response Time
#         # ---------------------------------
#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(

#             subset=[

#                 "resptime"
#             ]
#         )

#         return (

#             temp[

#                 [

#                     "datetime",

#                     "tenant",

#                     "namespace",

#                     "user",

#                     "ip",

#                     "node",

#                     "path",

#                     "put_size",

#                     "resptime"
#                 ]
#             ]

#             .sort_values(

#                 by="resptime",

#                 ascending=False
#             )

#             .head(limit)

#             .reset_index(

#                 drop=True
#             )
#         )
    
#     # ---------------------------------
#     # Slow GET Requests
#     # ---------------------------------
#     def slow_gets(

#         self,

#         limit=20
#     ):

#         temp = self.df.copy()

#         # ---------------------------------
#         # GET + HEAD
#         # ---------------------------------
#         temp = temp[

#             temp["method"]

#             .astype(str)

#             .str.upper()

#             .isin([

#                 "GET",

#                 "HEAD"
#             ])
#         ]

#         # ---------------------------------
#         # Convert Response Time
#         # ---------------------------------
#         temp["resptime"] = pd.to_numeric(

#             temp["resptime"],

#             errors="coerce"
#         )

#         temp = temp.dropna(

#             subset=[

#                 "resptime"
#             ]
#         )

#         return (

#             temp[

#                 [

#                     "datetime",

#                     "tenant",

#                     "namespace",

#                     "user",

#                     "ip",

#                     "node",

#                     "path",

#                     "get_size",

#                     "resptime"
#                 ]
#             ]

#             .sort_values(

#                 by="resptime",

#                 ascending=False
#             )

#             .head(limit)

#             .reset_index(
#                 drop=True
#             )
#         )
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

            .reset_index()

            .rename(

                columns={

                    "index": "ip",

                    "ip": "requests"
                }
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

            .reset_index()

            .rename(

                columns={

                    "index": "user",

                    "user": "requests"
                }
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

            .reset_index()

            .rename(

                columns={

                    "index": "tenant",

                    "tenant": "requests"
                }
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

            .reset_index()

            .rename(

                columns={

                    "index": "namespace",

                    "namespace": "requests"
                }
            )
        )

    # ---------------------------------
    # HTTP Methods
    # ---------------------------------
    def top_methods(self):

        return (

            self.df["method"]

            .value_counts()

            .reset_index()

            .rename(

                columns={

                    "index": "method",

                    "method": "requests"
                }
            )
        )

    # ---------------------------------
    # Status Codes
    # ---------------------------------
    def top_status_codes(self):

        return (

            self.df["status"]

            .value_counts()

            .reset_index()

            .rename(

                columns={

                    "index": "status",

                    "status": "requests"
                }
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

            .reset_index()

            .rename(

                columns={

                    "index": "path",

                    "path": "failures"
                }
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

            .reset_index()

            .rename(

                columns={

                    "index": "tenant",

                    "tenant": "failures"
                }
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

            .reset_index()

            .rename(

                columns={

                    "index": "ip",

                    "ip": "failures"
                }
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
    # Top IPs Writes
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

    # ---------------------------------
    # Read / Write Ratio By Tenant
    # ---------------------------------
    def read_write_ratio(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Normalize method
        # ---------------------------------
        temp["method"] = (

            temp["method"]

            .astype(str)

            .str.upper()
        )

        # ---------------------------------
        # Read operations
        # ---------------------------------
        reads = (

            temp[

                temp["method"]

                .isin([

                    "GET",

                    "HEAD"
                ])
            ]

            .groupby(

                "tenant"
            )

            .size()

            .reset_index(

                name="reads"
            )
        )

        # ---------------------------------
        # Write operations
        # ---------------------------------
        writes = (

            temp[

                temp["method"]

                .isin([

                    "PUT",

                    "POST",

                    "DELETE"
                ])
            ]

            .groupby(

                "tenant"
            )

            .size()

            .reset_index(

                name="writes"
            )
        )

        # ---------------------------------
        # Merge
        # ---------------------------------
        result = (

            reads.merge(

                writes,

                on="tenant",

                how="outer"
            )

            .fillna(0)
        )

        # ---------------------------------
        # Ratio
        # ---------------------------------
        result["read_write_ratio"] = (

            result["reads"]

            / result["writes"]

            .replace(

                0,

                1
            )
        ).round(2)

        return (

            result

            .sort_values(

                "read_write_ratio",

                ascending=False
            )

            .reset_index(

                drop=True
            )
        )

    # ---------------------------------
    # Object Size Distribution
    # ---------------------------------
    def object_size_distribution(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Normalize method
        # ---------------------------------
        temp["method"] = (

            temp["method"]

            .astype(str)

            .str.upper()
        )

        # ---------------------------------
        # Effective object size
        # PUT -> put_size
        # GET/HEAD -> get_size
        # ---------------------------------
        temp["object_size"] = None

        put_mask = (

            temp["method"]

            == "PUT"
        )

        temp.loc[

            put_mask,

            "object_size"

        ] = pd.to_numeric(

            temp.loc[

                put_mask,

                "put_size"
            ],

            errors="coerce"
        )

        temp.loc[

            ~put_mask,

            "object_size"

        ] = pd.to_numeric(

            temp.loc[

                ~put_mask,

                "get_size"
            ],

            errors="coerce"
        )

        # ---------------------------------
        # Remove invalid / zero sizes
        # ---------------------------------
        temp = temp.dropna(

            subset=[

                "object_size"
            ]
        )

        temp = temp[

            temp["object_size"]

            > 0
        ]

        # ---------------------------------
        # Size buckets
        # ---------------------------------
        bins = [

            0,

            1 * 1024 * 1024,

            10 * 1024 * 1024,

            100 * 1024 * 1024,

            1024 * 1024 * 1024,

            float("inf")
        ]

        labels = [

            "<1 MB",

            "1-10 MB",

            "10-100 MB",

            "100 MB-1 GB",

            ">1 GB"
        ]

        temp["size_bucket"] = pd.cut(

            temp["object_size"],

            bins=bins,

            labels=labels,

            include_lowest=True
        )

        # ---------------------------------
        # Aggregate
        # ---------------------------------
        result = (

            temp["size_bucket"]

            .value_counts()

            .sort_index()

            .reset_index()
        )

        result.columns = [

            "size_bucket",

            "requests"
        ]

        # ---------------------------------
        # Percentage
        # ---------------------------------
        total = result[

            "requests"
        ].sum()

        result["percentage"] = (

            result["requests"]

            / total

            * 100
        ).round(2)

        return result

    # ---------------------------------
    # Peak Traffic Hours
    # ---------------------------------
    def peak_traffic_hours(

        self
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Validate datetime
        # ---------------------------------
        temp = temp.dropna(

            subset=[

                "datetime"
            ]
        )

        # ---------------------------------
        # Hour bucket
        # ---------------------------------
        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        # ---------------------------------
        # Aggregate
        # ---------------------------------
        result = (

            temp.groupby(

                "hour"
            )

            .size()

            .reset_index(

                name="requests"
            )

            .sort_values(

                "requests",

                ascending=False
            )
        )

        return (
            result
            .reset_index(
                drop=True
            )
        )

    # ---------------------------------
    # Traffic Trend By Tenant
    # ---------------------------------
    def traffic_trend_by_tenant(

        self,

        limit=10
    ):

        temp = self.df.copy()

        # ---------------------------------
        # Validate columns
        # ---------------------------------
        temp = temp.dropna(

            subset=[

                "datetime",

                "tenant"
            ]
        )

        # ---------------------------------
        # Top tenants only
        # ---------------------------------
        top_tenants = (

            temp["tenant"]

            .value_counts()

            .head(limit)

            .index
        )

        temp = temp[

            temp["tenant"]

            .isin(

                top_tenants
            )
        ]

        # ---------------------------------
        # Hour bucket
        # ---------------------------------
        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        # ---------------------------------
        # Aggregate
        # ---------------------------------
        result = (

            temp.groupby(

                [

                    "hour",

                    "tenant"
                ]
            )

            .size()

            .reset_index(

                name="requests"
            )

            .sort_values(

                [

                    "hour",

                    "requests"
                ],

                ascending=[

                    True,

                    False
                ]
            )
        )

        return (

            result

            .reset_index(

                drop=True
            )
        )


# ---------------------------------
# Traffic Insights
# ---------------------------------
def run_traffic_insights(

    insights,

    display,

    exporter,

    charts
):

    datasets = {}

    # ---------------------------------
    # Top IPs
    # ---------------------------------
    top_ips = insights.top_ips()

    exporter.show_and_export(

        "🌐 TOP CLIENT IPS",

        top_ips,

        display
    )

    datasets[
        "top_client_ips"
    ] = top_ips

    # ---------------------------------
    # Top Users
    # ---------------------------------
    top_users = insights.top_users()

    exporter.show_and_export(

        "👤 TOP USERS",

        top_users,

        display
    )

    datasets[
        "top_users"
    ] = top_users

    # ---------------------------------
    # Top Tenants
    # ---------------------------------
    top_tenants = insights.top_tenants()

    exporter.show_and_export(

        "🏢 TOP TENANTS",

        top_tenants,

        display
    )

    datasets[
        "top_tenants"
    ] = top_tenants

    # ---------------------------------
    # Top Namespaces
    # ---------------------------------
    top_namespaces = insights.top_namespaces()

    exporter.show_and_export(

        "📦 TOP NAMESPACES",

        top_namespaces,

        display
    )

    datasets[
        "top_namespaces"
    ] = top_namespaces

    # ---------------------------------
    # HTTP Methods
    # ---------------------------------
    top_methods = insights.top_methods()

    exporter.show_and_export(

        "🌐 HTTP METHODS",

        top_methods,

        display
    )

    datasets[
        "http_methods"
    ] = top_methods

    # ---------------------------------
    # Status Codes
    # ---------------------------------
    top_status_codes = insights.top_status_codes()

    exporter.show_and_export(

        "🚦 STATUS CODES",

        top_status_codes,

        display
    )

    datasets[
        "status_codes"
    ] = top_status_codes

    # ---------------------------------
    # Response Times
    # ---------------------------------
    top_responsetime = (
        insights.get_top_responsetime()
    )

    exporter.show_and_export(

        "⏱ TOP RESPONSE TIMES",

        top_responsetime,

        display
    )

    datasets[
        "top_response_times"
    ] = top_responsetime

    # ---------------------------------
    # Top tenant reads
    # ---------------------------------
    top_tenants_reads = (
        insights.top_tenants_reads()
    )

    exporter.show_and_export(

        "📈 TOP TENANTS READS",

        top_tenants_reads,

        display
    )

    datasets[
        "top_tenants_reads"
    ] = top_tenants_reads

    # ---------------------------------
    # Top tenant writes
    # ---------------------------------
    top_tenants_writes = (
        insights.top_tenants_writes()
    )

    exporter.show_and_export(

        "📈 TOP TENANTS WRITES",

        top_tenants_writes,

        display
    )

    datasets[
        "top_tenants_writes"
    ] = top_tenants_writes

    # ---------------------------------
    # Top ips reads
    # ---------------------------------
    top_ips_reads = (
        insights.top_ips_reads()
    )

    exporter.show_and_export(

        "📈 TOP IPS READS",

        top_ips_reads,

        display
    )

    datasets[
        "top_ips_reads"
    ] = top_ips_reads

    # ---------------------------------
    # Top IPS Writes
    # ---------------------------------
    top_ips_writes = (
        insights.top_ips_writes()
    )

    exporter.show_and_export(

        "📈 TOP IPS WRITES",

        top_ips_writes,

        display
    )

    datasets[
        "top_ips_writes"
    ] = top_ips_writes

    # ---------------------------------
    # Top Extensions
    # ---------------------------------
    top_extensions = (
        insights.top_extensions()
    )

    exporter.show_and_export(

        "⏱ TOP EXTENSIONS",

        top_extensions,

        display
    )

    datasets[
        "top_extensions"
    ] = top_extensions

    # ---------------------------------
    # Read / Write Ratio By Tenant
    # ---------------------------------
    read_write_ratio_by_tenant = (
        insights.read_write_ratio()
    )

    exporter.show_and_export(

        "⏱ READ / WRITE RATIO BY TENANT",

        read_write_ratio_by_tenant,

        display
    )

    datasets[
        "read_write_ratio_by_tenant"
    ] = read_write_ratio_by_tenant

    # ---------------------------------
    # Object Size Distribution
    # ---------------------------------
    object_size_dist = (
        insights.object_size_distribution()
    )

    exporter.show_and_export(

        "⏱ OBJECT SIZE DISTRUBUTION",

        object_size_dist,

        display
    )

    datasets[
        "object_size_dist"
    ] = object_size_dist

    # ---------------------------------
    # Peak Traffic Hours
    # ---------------------------------
    peak_traffic_hours = (
        insights.peak_traffic_hours()
    )

    exporter.show_and_export(

        "⏱ PEAK TRAFFIC HOURS",

        peak_traffic_hours,

        display
    )

    datasets[
        "peak_traffic_hours"
    ] = peak_traffic_hours

    # ---------------------------------
    # Traffic Trend By Tenant
    # ---------------------------------
    traffic_trend_by_tenant = (
        insights.traffic_trend_by_tenant()
    )

    exporter.show_and_export(

        "⏱ TRAFFICE TREND BY TENANT",

        traffic_trend_by_tenant,

        display
    )

    datasets[
        "traffic_trend_by_tenant"
    ] = traffic_trend_by_tenant

    # ---------------------------------
    # Export All
    # ---------------------------------
    exporter.export_multiple(datasets, "traffic_insights")


# ---------------------------------
# Error Insights
# ---------------------------------
def run_error_insights(

    insights,

    display,

    exporter,

    charts
):

    datasets = {}

    # ---------------------------------
    # 4XX Errors
    # ---------------------------------
    errors_4xx = (
        insights.get_4xx_errors()
    )

    exporter.show_and_export(

        "⚠️ 4XX ERRORS",

        errors_4xx,

        display
    )

    datasets[
        "4xx_errors"
    ] = errors_4xx

    # ---------------------------------
    # 5XX Errors
    # ---------------------------------
    errors_5xx = (
        insights.get_5xx_errors()
    )

    exporter.show_and_export(

        "🔥 5XX ERRORS",

        errors_5xx,

        display
    )

    datasets[
        "5xx_errors"
    ] = errors_5xx

    # ---------------------------------
    # Top Failed Paths
    # ---------------------------------
    failed_paths = (
        insights.get_top_failed_paths()
    )

    exporter.show_and_export(

        "❌ TOP FAILED PATHS",

        failed_paths,

        display
    )

    datasets[
        "top_failed_paths"
    ] = failed_paths

    # ---------------------------------
    # Top Failed Tenants
    # ---------------------------------
    failed_tenants = (
        insights.get_top_failed_tenants()
    )

    exporter.show_and_export(

        "🏢 TOP FAILED TENANTS",

        failed_tenants,

        display
    )

    datasets[
        "top_failed_tenants"
    ] = failed_tenants

    # ---------------------------------
    # Top Failed IPs
    # ---------------------------------
    failed_ips = (
        insights.get_top_failed_ips()
    )

    exporter.show_and_export(

        "❌ TOP FAILED IPS",

        failed_ips,

        display
    )

    datasets[
        "top_failed_ips"
    ] = failed_ips

    # ---------------------------------
    # Top Users with 403 Errors
    # ---------------------------------
    top_403_users = (
        insights.top_403_users()
    )

    exporter.show_and_export(

        "⚠️ TOP USERS WITH 403 ERRORS",

        top_403_users,

        display
    )

    datasets[
        "top_403_users"
    ] = top_403_users

    # ---------------------------------
    # Top 404 Objects
    # ---------------------------------
    top_404_objects = (
        insights.top_404_objects()
    )

    exporter.show_and_export(

        "❌ TOP 404 OBJECTS",

        top_404_objects,

        display
    )

    datasets[
        "top_404_objects"
    ] = top_404_objects

    # ---------------------------------
    # Error Rate By Tenant
    # ---------------------------------
    error_rate_by_tenant = (
        insights.error_rate_by_tenant()
    )

    exporter.show_and_export(

        "❌ ERROR RATE BY TENANT",

        error_rate_by_tenant,

        display
    )

    datasets[
        "error_rate_by_tenant"
    ] = error_rate_by_tenant

    # ---------------------------------
    # Failure Percentage
    # ---------------------------------
    failure_percentage = (
        insights.failure_percentage()
    )

    exporter.show_and_export(

        "⚠️ FAILURE PERCENTAGE",

        failure_percentage,

        display
    )

    datasets[
        "failure_percentage"
    ] = failure_percentage

    # ---------------------------------
    # Export All
    # ---------------------------------
    exporter.export_multiple(

        datasets,

        "error_insights"
    )


# ---------------------------------
# Security Insights
# ---------------------------------
def run_security_insights(

    insights,

    display,

    exporter,

    charts
):

    datasets = {}

    # ---------------------------------
    # Delete Operations
    # ---------------------------------
    delete_ops = insights.get_delete_operations()

    exporter.show_and_export(

        "🗑 DELETE OPERATIONS",

        delete_ops,

        display
    )

    datasets[
        "delete_operations"
    ] = delete_ops

    # ---------------------------------
    # High 403 Activity
    # ---------------------------------
    high_403 = insights.get_high_403_activity()

    exporter.show_and_export(

        "🚫 HIGH 403 ACTIVITY",

        high_403,

        display
    )

    datasets[
        "high_403_activity"
    ] = high_403

    # ---------------------------------
    # Anonymous Access
    # ---------------------------------
    anonymous = insights.get_anonymous_access()

    exporter.show_and_export(

        "👻 ANONYMOUS ACCESS",

        anonymous,

        display
    )

    datasets[
        "anonymous_access"
    ] = anonymous

    # ---------------------------------
    # Large Uploads
    # ---------------------------------
    uploads = insights.get_large_uploads()

    exporter.show_and_export(

        "📦 LARGE UPLOADS",

        uploads,

        display
    )

    datasets[
        "large_uploads"
    ] = uploads

    # ---------------------------------
    # Suspicious IPs
    # ---------------------------------
    suspicious = insights.get_suspicious_ips()

    exporter.show_and_export(

        "⚠️ SUSPICIOUS IPS",

        suspicious,

        display
    )

    datasets[
        "suspicious_ips"
    ] = suspicious

    # ---------------------------------
    # Failed Login Patterns
    # ---------------------------------
    failed_login_patterns = insights.get_failed_login_patterns()

    exporter.show_and_export(

        "⚠️ FAILED LOGIN PATTERNS",

        failed_login_patterns,

        display
    )

    datasets[
        "failed_login_patterns"
    ] = failed_login_patterns

    # ---------------------------------
    # Delete Activity By Tenant
    # ---------------------------------
    delete_by_tenant = insights.get_delete_by_tenant()

    exporter.show_and_export(

        "⚠️ DELETE ACTIVITY BY TENANT",

        delete_by_tenant,

        display
    )

    datasets[
        "delete_by_tenant"
    ] = delete_by_tenant

    # ---------------------------------
    # Delete Activity By User
    # ---------------------------------
    delete_by_user = insights.get_delete_by_user()

    exporter.show_and_export(

        "⚠️ DELETE ACTIVITY BY USER",

        delete_by_user,

        display
    )

    datasets[
        "delete_by_user"
    ] = delete_by_user

    # ---------------------------------
    # Export All
    # ---------------------------------
    exporter.export_multiple(

        datasets,

        "security_insights"
    )


# ---------------------------------
# Performance Insights
# ---------------------------------
def run_performance_insights(

    insights,

    display,

    exporter,

    charts

):

    datasets = {}

    # ---------------------------------
    # Slowest Requests
    # ---------------------------------
    slowest_requests = (
        insights.get_slowest_requests()
    )

    exporter.show_and_export(

        "🐢 SLOWEST REQUESTS",

        slowest_requests,

        display
    )

    datasets[
        "slowest_requests"
    ] = slowest_requests

    # ---------------------------------
    # High Latency Paths
    # ---------------------------------
    high_latency_paths = (
        insights.get_high_latency_paths()
    )

    exporter.show_and_export(

        "📡 HIGH LATENCY PATHS",

        high_latency_paths,

        display
    )

    datasets[
        "high_latency_paths"
    ] = high_latency_paths

    # ---------------------------------
    # High Latency Tenants
    # ---------------------------------
    high_latency_tenants = (
        insights.get_high_latency_tenants()
    )

    exporter.show_and_export(

        "🏢 HIGH LATENCY TENANTS",

        high_latency_tenants,

        display
    )

    datasets[
        "high_latency_tenants"
    ] = high_latency_tenants

    # ---------------------------------
    # Average Response Time
    # ---------------------------------
    average_response_time = (
        insights.get_average_response_time()
    )

    exporter.show_and_export(

        "⚡ AVERAGE RESPONSE TIME",

        average_response_time,

        display
    )

    datasets[
        "average_response_time"
    ] = average_response_time

    # ---------------------------------
    # High Latency Nodes
    # ---------------------------------
    high_latency_nodes = insights.get_high_latency_nodes()

    exporter.show_and_export(

        "⚠️ HIGH LATENCY NODES",

        high_latency_nodes,

        display
    )

    datasets[
        "high_latency_nodes"
    ] = high_latency_nodes

    # ---------------------------------
    # High Request Nodes
    # ---------------------------------
    high_requests_nodes = insights.get_high_requests_nodes()

    exporter.show_and_export(

        "⚠️ HIGH REQUESTS NODES",

        high_requests_nodes,

        display
    )

    datasets[
        "high_requests_nodes"
    ] = high_requests_nodes

    # ---------------------------------
    # Slow Puts
    # ---------------------------------
    slow_puts = insights.slow_puts()

    exporter.show_and_export(

        "⚠️ SLOW PUTS",

        slow_puts,

        display
    )

    datasets[
        "slow_puts"
    ] = slow_puts

    # ---------------------------------
    # Slow Gets
    # ---------------------------------
    slow_gets = insights.slow_gets()

    exporter.show_and_export(

        "⚠️ SLOW GETS",

        slow_gets,

        display
    )

    datasets[
        "slow_gets"
    ] = slow_gets

    # ---------------------------------
    # Export All
    # ---------------------------------
    exporter.export_multiple(

        datasets,

        "performance_insights"
    )


# ---------------------------------
# Timeline Insights
# ---------------------------------
def run_timeline_insights(

    insights,

    display,

    exporter,

    charts

):

    datasets = {}

    # ---------------------------------
    # Requests Per Hour
    # ---------------------------------
    requests_per_hour = (
        insights.requests_per_hour()
    )

    exporter.show_and_export(

        "🕒 REQUESTS PER HOUR",

        requests_per_hour,

        display
    )

    charts.save_line_chart(

        requests_per_hour,

        "hour",

        "requests",

        "Requests Per Hour",

        "requests_per_hour.png"
    )

    datasets[
        "requests_per_hour"
    ] = requests_per_hour

    # ---------------------------------
    # Requests Per Day
    # ---------------------------------
    requests_per_day = (
        insights.requests_per_day()
    )

    exporter.show_and_export(

        "📅 REQUESTS PER DAY",

        requests_per_day,

        display
    )

    charts.save_line_chart(

        requests_per_day,

        "day",

        "requests",

        "Requests Per Day",

        "requests_per_day.png"
    )

    datasets[
        "requests_per_day"
    ] = requests_per_day

    # ---------------------------------
    # Errors Over Time
    # ---------------------------------
    errors_over_time = (
        insights.errors_over_time()
    )

    exporter.show_and_export(

        "⚠️ ERRORS OVER TIME",

        errors_over_time,

        display
    )

    charts.save_line_chart(

        errors_over_time,

        "hour",

        "errors",

        "Errors Over Time",

        "errors_over_time.png"
    )

    datasets[
        "errors_over_time"
    ] = errors_over_time

    # ---------------------------------
    # S3 Activity Over Time
    # ---------------------------------
    s3_activity = (
        insights.s3_activity_over_time()
    )

    exporter.show_and_export(

        "☁️ S3 ACTIVITY OVER TIME",

        s3_activity,

        display
    )

    charts.save_line_chart(

        s3_activity,

        "hour",

        "s3_requests",

        "S3 Activity Over Time",

        "s3_activity_over_time.png"
    )

    datasets[
        "s3_activity_over_time"
    ] = s3_activity

    # ---------------------------------
    # REST Activity Over Time
    # ---------------------------------
    rest_activity = (
        insights.rest_activity_over_time()
    )

    exporter.show_and_export(

        "🌐 REST ACTIVITY OVER TIME",

        rest_activity,

        display
    )

    charts.save_line_chart(

        rest_activity,

        "hour",

        "rest_requests",

        "REST Activity Over Time",

        "rest_activity_over_time.png"
    )

    datasets[
        "rest_activity_over_time"
    ] = rest_activity

    # ---------------------------------
    # 4XX Errors Over Time
    # ---------------------------------
    errors_4xx = (
        insights.errors_4xx_over_time()
    )

    exporter.show_and_export(

        "🌐 4XX Errors Over Time",

        errors_4xx,

        display
    )

    charts.save_line_chart(

        errors_4xx,

        "hour",

        "errors",

        "4XX Errors Over Time",

        "errors_4xx_over_time.png"
    )

    datasets[
        "errors_4xx_over_time"
    ] = errors_4xx

    # ---------------------------------
    # 5XX Errors Over Time
    # ---------------------------------
    errors_5xx = (
        insights.errors_5xx_over_time()
    )

    exporter.show_and_export(

        "🌐 5XX Errors Over Time",

        errors_5xx,

        display
    )

    charts.save_line_chart(

        errors_5xx,

        "hour",

        "errors",

        "5XX Errors Over Time",

        "errors_5xx_over_time.png"
    )

    datasets[
        "errors_5xx_over_time"
    ] = errors_5xx

    # ---------------------------------
    # DELETE Activity Over Time
    # ---------------------------------
    delete_activity = (
        insights.delete_activity_over_time()
    )

    exporter.show_and_export(

        "🗑️ DELETE ACTIVITY OVER TIME",

        delete_activity,

        display
    )

    charts.save_line_chart(

        delete_activity,

        "hour",

        "requests",

        "DELETE ACTIVITY OVER TIME",

        "delete_activity_over_time.png"
    )

    datasets[
        "delete_activity_over_time"
    ] = delete_activity

    # ---------------------------------
    # PUT Activity Over Time
    # ---------------------------------
    put_activity = (
        insights.put_activity_over_time()
    )

    exporter.show_and_export(

        "🌐 PUT ACTIVITY OVER TIME",

        put_activity,

        display
    )

    charts.save_line_chart(

        put_activity,

        "hour",

        "requests",

        "PUT Activity Over Time",

        "put_activity_over_time.png"
    )

    datasets[
        "put_activity_over_time"
    ] = put_activity

    # ---------------------------------
    # Requests Per Node Over Time
    # ---------------------------------
    requests_per_node = (
        insights.requests_per_node_over_time()
    )

    exporter.show_and_export(

        "🌐 REQUESTS PER NODE OVER TIME",

        requests_per_node,

        display
    )

    charts.save_multi_line_chart(

        requests_per_node,

        "hour",

        "requests",

        "node",

        "Requests Per Node Over Time",

        "requests_per_node_over_time.png"
    )

    datasets[
        "requests_per_node_over_time"
    ] = requests_per_node

    # ---------------------------------
    # Tenant Activity Over Time
    # ---------------------------------
    tenant_activity = (
        insights.tenant_activity_over_time()
    )

    exporter.show_and_export(

        "🌐 Tenant Activity OVER TIME",

        tenant_activity,

        display
    )

    charts.save_stacked_area_chart(

        tenant_activity,

        "hour",

        "requests",

        "tenant",

        "Tenant Activity Over Time",

        "tenant_activity_over_time.png"
    )

    datasets[
        "tenant_activity_over_time"
    ] = tenant_activity

    # ---------------------------------
    # Namespace Activity Over Time
    # ---------------------------------
    namespace_activity = (
        insights.namespace_activity_over_time()
    )

    exporter.show_and_export(

        "🌐 Namespace Activity OVER TIME",

        namespace_activity,

        display
    )

    charts.save_stacked_area_chart(

        namespace_activity,

        "hour",

        "requests",

        "namespace",

        "Namespace Activity Over Time",

        "namespace_activity_over_time.png"
    )

    datasets[
        "namespace_activity_over_time"
    ] = namespace_activity

    # ---------------------------------
    # Average Resptime Over Time
    # ---------------------------------
    average_resptime = (
        insights.average_resptime_over_time()
    )

    exporter.show_and_export(

        "🌐Average Resptime OVER TIME",

        average_resptime,

        display
    )

    charts.save_line_chart(

        average_resptime,

        "hour",

        "avg_resptime",

        "Average Response Time",

        "average_resptime_over_time.png"
    )

    datasets[
        "average_resptime_over_time"
    ] = average_resptime

    # ---------------------------------
    # After Hours Activity
    # ---------------------------------
    after_hours = (
        insights.after_hours_activity()
    )

    exporter.show_and_export(

        "🌐After Hours Activity",

        after_hours,

        display
    )

    charts.save_bar_chart(

        after_hours,

        "hour_of_day",

        "requests",

        "After Hours Activity",

        "after_hours_activity.png"
    )

    datasets[
        "after_hours_activity"
    ] = after_hours

    # ---------------------------------
    # Export All
    # ---------------------------------
    exporter.export_multiple(

        datasets,

        "timeline_insights"
    )