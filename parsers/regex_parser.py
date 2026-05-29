import re
import pandas as pd


# --------------------------------------------------
# HCP Gateway Access Log Pattern
# --------------------------------------------------
LOG_PATTERN = re.compile(

    r'(?P<ip>\S+)\s+-\s+'

    r'(?P<user>\S+)\s+'

    r'\[(?P<datetime>[^\]]+)\]\s+'

    r'"(?P<method>\S+)\s+'

    r'(?P<path>[^\s]+)\s+'

    r'(?P<http_protocol>[^"]+)"\s+'

    r'(?P<status>\d+)\s+'

    r'(?P<get_size>\d+)\s+' # Size of GET response in bytes

    r'(?P<host>\S+)\s+' # Namespace.Tenant@hs3 or Namespace.Tenant

    r'(?P<resptime>\d+)\s+' # Processing time in milliseconds

    r'(?P<node>\d+)'

    r'(?:\s+(?P<put_size>\S+))?' # Size of PUT response in bytes    
)


# --------------------------------------------------
# Normalize HCP Host Semantics
# --------------------------------------------------
def normalize_host_fields(record):

    host = str(
        record.get(
            "host",
            ""
        )
    )

    # ----------------------------------------------
    # S3 Protocol
    # namespace.tenant@hs3
    # ----------------------------------------------
    if "@hs3" in host:

        base = host.replace(
            "@hs3",
            ""
        )

        if "." in base:

            namespace, tenant = (
                base.split(".", 1)
            )

        else:

            namespace = base
            tenant = None

        record["namespace"] = namespace

        record["tenant"] = tenant

        record["protocol_type"] = "S3"

    # ----------------------------------------------
    # REST Protocol
    # namespace.tenant
    # ----------------------------------------------
    elif "." in host:

        namespace, tenant = (
            host.split(".", 1)
        )

        record["namespace"] = namespace

        record["tenant"] = tenant

        record["protocol_type"] = "REST"

    # ----------------------------------------------
    # Unknown / System
    # ----------------------------------------------
    else:

        record["namespace"] = None

        record["tenant"] = None

        record["protocol_type"] = "UNKNOWN"

    return record


# --------------------------------------------------
# Parse Single Access Log File
# --------------------------------------------------
def parse_log_file(

    filepath,

    unparsed_file=None
):
    """
    Parse a single HCP access log file.

    Args:
        filepath (str):
            Access log file path

        unparsed_file (str):
            File to save unmatched lines

    Returns:
        pandas.DataFrame
    """

    rows = []

    with open(

        filepath,

        "r",

        encoding="utf-8",

        errors="ignore"
    ) as f:

        for line in f:

            line = line.strip()

            match = LOG_PATTERN.search(
                line
            )

            # ------------------------------------------
            # Parsed Successfully
            # ------------------------------------------
            if match:

                row = match.groupdict()

                # --------------------------------------
                # Add source file
                # --------------------------------------
                row["source_file"] = filepath

                # --------------------------------------
                # Normalize HCP semantics
                # --------------------------------------
                row = normalize_host_fields(
                    row
                )

                rows.append(row)

            # ------------------------------------------
            # Save unparsed lines
            # ------------------------------------------
            elif unparsed_file:

                with open(

                    unparsed_file,

                    "a",

                    encoding="utf-8"
                ) as uf:

                    uf.write(
                        line + "\n"
                    )

    # --------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------
    df = pd.DataFrame(rows)

    # --------------------------------------------------
    # Convert Timestamp
    # --------------------------------------------------
    if (

        not df.empty

        and "datetime" in df.columns
    ):

        df["datetime"] = pd.to_datetime(

            df["datetime"],

            format="%d/%b/%Y:%H:%M:%S %z",

            errors="coerce"
        )

    # --------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------
    if (

        not df.empty

        and "datetime" in df.columns
    ):

        df = df.sort_values(
            by="datetime"
        )

    return df
