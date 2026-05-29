import pandas as pd


class AccessLogFilters:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(self, dataframe):

        self.df = dataframe

    # ---------------------------------
    # Filter by IP (Client IP)
    # ---------------------------------
    def by_ip(

        self,

        ip
    ):

        return self.df[

            self.df["ip"]

            .astype(str)

            == str(ip)
        ]

    # ---------------------------------
    # Filter by User
    # ---------------------------------
    def by_user(

        self,

        user
    ):

        return self.df[

            self.df["user"]

            .astype(str)

            == str(user)
        ]

    # ---------------------------------
    # Filter by Datetime
    # ---------------------------------
    def by_datetime(

        self,

        start_date=None,

        end_date=None
    ):

        temp = self.df.copy()

        temp["datetime"] = pd.to_datetime(

            temp["datetime"],

            errors="coerce"
        )

        if start_date:

            temp = temp[

                temp["datetime"]
                >= start_date
            ]

        if end_date:

            temp = temp[

                temp["datetime"]
                <= end_date
            ]

        return temp

    # ---------------------------------
    # Filter by Method
    # ---------------------------------
    def by_method(

        self,

        method
    ):

        return self.df[

            self.df["method"]

            .astype(str)

            .str.upper()

            == method.upper()
        ]

    # ---------------------------------
    # Filter by Path
    # ---------------------------------
    def by_path(

        self,

        keyword
    ):

        return self.df[

            self.df["path"]

            .astype(str)

            .str.contains(

                keyword,

                case=False,

                na=False
            )
        ]

    # ---------------------------------
    # Filter by Protocol
    # ---------------------------------
    def by_http_protocol(

        self,

        protocol
    ):

        return self.df[

            self.df["http_protocol"]

            .astype(str)

            .str.contains(

                protocol,

                case=False,

                na=False
            )
        ]


    # ---------------------------------
    # Filter by HCP Protocol Type
    # ---------------------------------
    def by_protocol_type(

        self,

        protocol_type
    ):

        return self.df[

            self.df["protocol_type"]

            .astype(str)

            .str.upper()

            == protocol_type.upper()
        ]

    # ---------------------------------
    # Filter by Status
    # ---------------------------------
    def by_status(

        self,

        status
    ):

        return self.df[

            self.df["status"]

            .astype(str)

            == str(status)
        ]

    # ---------------------------------
    # Filter by Get_Size
    # ---------------------------------
    def by_get_size(

        self,

        min_size=None,

        max_size=None
    ):

        temp = self.df.copy()

        temp["get_size"] = pd.to_numeric(

            temp["get_size"],

            errors="coerce"
        )

        if min_size is not None:

            temp = temp[

                temp["get_size"]
                >= min_size
            ]

        if max_size is not None:

            temp = temp[

                temp["get_size"]
                <= max_size
            ]

        return temp

    # ---------------------------------
    # Filter by Host
    # ---------------------------------
    def by_host(

        self,

        host
    ):

        return self.df[

            self.df["host"]

            .astype(str)

            .str.contains(

                host,

                case=False,

                na=False
            )
        ]

    # ---------------------------------
    # Filter by Response Time
    # ---------------------------------
    def by_resptime(

        self,

        min_resptime=None,

        max_resptime=None
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        if min_resptime is not None:

            temp = temp[

                temp["resptime"]
                >= min_resptime
            ]

        if max_resptime is not None:

            temp = temp[

                temp["resptime"]
                <= max_resptime
            ]

        return temp

    # ---------------------------------
    # Filter by Node
    # ---------------------------------
    def by_node(

        self,

        node
    ):

        return self.df[

            self.df["node"]

            .astype(str)

            == str(node)
        ]

    # ---------------------------------
    # Filter by Namespace
    # ---------------------------------
    def by_namespace(

        self,

        namespace
    ):

        return self.df[

            self.df["namespace"]

            .astype(str)

            .str.contains(

                namespace,

                case=False,

                na=False
            )
        ]

    # ---------------------------------
    # Filter by Tenant
    # ---------------------------------
    def by_tenant(

        self,

        tenant
    ):

        return self.df[

            self.df["tenant"]

            .astype(str)

            .str.contains(

                tenant,

                case=False,

                na=False
            )
        ]
