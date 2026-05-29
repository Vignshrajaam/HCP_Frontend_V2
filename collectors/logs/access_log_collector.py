from pathlib import Path
import os

import pandas as pd

from parsers.regex_parser import parse_log_file


class AccessLogCollector:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(self, base_path):

        self.base_path = Path(base_path)

    # ---------------------------------
    # Collect Logs
    # ---------------------------------
    def collect(

        self,

        unparsed_log=(
            "unparsed_lines.txt"
        )
    ):

        dfs = []

        # -----------------------------
        # Find access logs
        # -----------------------------
        for path, _, files in os.walk(
            self.base_path
        ):

            for file in files:

                # -------------------------
                # Match rotated gateway logs
                # -------------------------
                if file.startswith(
                    "http_gateway_request.log."
                ):

                    full_path = os.path.join(
                        path,
                        file
                    )

                    print(

                        f"📄 Parsing: "
                        f"{full_path}"
                    )

                    # ---------------------
                    # Parse log
                    # ---------------------
                    df = parse_log_file(

                        full_path,

                        unparsed_file=(
                            unparsed_log
                        )
                    )

                    # ---------------------
                    # Skip empty
                    # ---------------------
                    if not df.empty:

                        dfs.append(df)

        # -----------------------------
        # No logs found
        # -----------------------------
        if not dfs:

            print(
                "\n❌ No access logs parsed\n"
            )

            return pd.DataFrame()

        # -----------------------------
        # Merge
        # -----------------------------
        merged_df = pd.concat(

            dfs,

            ignore_index=True
        )

        print(

            f"\n✅ Total Parsed "
            f"Records: "
            f"{len(merged_df)}"
        )

        return merged_df
