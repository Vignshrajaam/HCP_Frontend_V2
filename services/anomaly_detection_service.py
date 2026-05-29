import pandas as pd


class HCPAnomalyDetectionService:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(

        self,

        df
    ):

        self.df = df.copy()

    # ---------------------------------
    # Generic Spike Detection
    # ---------------------------------
    def detect_spikes(

        self,

        df,

        metric_column,

        threshold_multiplier=3
    ):

        if df.empty:

            return pd.DataFrame()

        mean_value = (
            df[metric_column]
            .mean()
        )

        std_value = (
            df[metric_column]
            .std()
        )

        threshold = (

            mean_value +

            (
                threshold_multiplier
                * std_value
            )
        )

        anomalies = df[

            df[metric_column]
            > threshold
        ].copy()

        anomalies[
            "threshold"
        ] = threshold

        return anomalies

    # ---------------------------------
    # Detect DELETE Spikes
    # ---------------------------------
    def detect_delete_spikes(

        self
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

        # ---------------------------------
        # Group By Hour
        # ---------------------------------
        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        grouped = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="requests"
            )
        )

        return self.detect_spikes(

            grouped,

            "requests"
        )

    # ---------------------------------
    # Print DELETE Spikes
    # ---------------------------------
    def print_delete_spikes(

        self
    ):

        anomalies = (
            self.detect_delete_spikes()
        )

        print(
            "\n🚨 DELETE SPIKE DETECTION\n"
        )

        if anomalies.empty:

            print(
                "No anomalies detected\n"
            )

            return

        print(anomalies)

        print(
            "\n" + "=" * 80 + "\n"
        )
    
    # ---------------------------------
    # Detect Response Time Spikes
    # ---------------------------------
    def detect_resptime_spikes(

        self
    ):

        temp = self.df.copy()

        temp["resptime"] = pd.to_numeric(

            temp["resptime"],

            errors="coerce"
        )

        # ---------------------------------
        # Group By Hour
        # ---------------------------------
        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        grouped = (

            temp.groupby("hour")[

                "resptime"

            ]

            .mean()

            .reset_index(
                name="avg_resptime"
            )
        )

        return self.detect_spikes(

            grouped,

            "avg_resptime"
        )
    
    # ---------------------------------
    # Print Response Time Spikes
    # ---------------------------------
    def print_resptime_spikes(

        self
    ):

        anomalies = (
            self.detect_resptime_spikes()
        )

        print(
            "\n🚨 RESPONSE TIME SPIKES\n"
        )

        if anomalies.empty:

            print(
                "No anomalies detected\n"
            )

            return

        print(anomalies)

        print(
            "\n" + "=" * 80 + "\n"
        )
    
    # ---------------------------------
    # Detect 403 Bursts
    # ---------------------------------
    def detect_403_bursts(

        self
    ):

        temp = self.df.copy()

        temp["status"] = pd.to_numeric(

            temp["status"],

            errors="coerce"
        )

        temp = temp[

            temp["status"] == 403
        ]

        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        grouped = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="requests"
            )
        )

        return self.detect_spikes(

            grouped,

            "requests"
        )
    
    # ---------------------------------
    # Print 403 Bursts
    # ---------------------------------
    def print_403_bursts(

        self
    ):

        anomalies = (
            self.detect_403_bursts()
        )

        print(
            "\n🚨 403 BURST DETECTION\n"
        )

        if anomalies.empty:

            print(
                "No anomalies detected\n"
            )

            return

        print(anomalies)

        print(
            "\n" + "=" * 80 + "\n"
        )
    
    # ---------------------------------
    # Detect REST Floods
    # ---------------------------------
    def detect_rest_floods(

        self
    ):

        temp = self.df.copy()

        temp = temp[

            temp["protocol_type"]

            .astype(str)

            .str.upper()

            == "REST"
        ]

        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        grouped = (

            temp.groupby("hour")

            .size()

            .reset_index(
                name="requests"
            )
        )

        return self.detect_spikes(

            grouped,

            "requests"
        )
    
    # ---------------------------------
    # Print REST Floods
    # ---------------------------------
    def print_rest_floods(

        self
    ):

        anomalies = (
            self.detect_rest_floods()
        )

        print(
            "\n🚨 REST FLOOD DETECTION\n"
        )

        if anomalies.empty:

            print(
                "No anomalies detected\n"
            )

            return

        print(anomalies)

        print(
            "\n" + "=" * 80 + "\n"
        )
    
    # ---------------------------------
    # Detect Tenant Activity Spikes
    # ---------------------------------
    def detect_tenant_spikes(

        self
    ):

        temp = self.df.copy()

        temp["hour"] = (

            temp["datetime"]

            .dt.floor("h")
        )

        grouped = (

            temp.groupby([

                "hour",
                "tenant"

            ])

            .size()

            .reset_index(
                name="requests"
            )
        )

        return self.detect_spikes(

            grouped,

            "requests"
        )
    
    # ---------------------------------
    # Print Tenant Activity Spikes
    # ---------------------------------
    def print_tenant_spikes(

        self
    ):

        anomalies = (
            self.detect_tenant_spikes()
        )

        print(
            "\n🚨 TENANT ACTIVITY SPIKES\n"
        )

        if anomalies.empty:

            print(
                "No anomalies detected\n"
            )

            return

        print(anomalies)

        print(
            "\n" + "=" * 80 + "\n"
        )