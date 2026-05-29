import pandas as pd
import os
from datetime import datetime


class ExportManager:

    # ---------------------------------
    # Init
    # ---------------------------------
    def __init__(

        self,

        export_dir="exports/access_logs"
    ):

        self.export_dir = export_dir

        os.makedirs(

            self.export_dir,

            exist_ok=True
        )

    # ---------------------------------
    # Export DataFrame to CSV
    # ---------------------------------
    def to_csv(

        self,

        df,

        filename=None
    ):

        # ---------------------------------
        # Auto Filename
        # ---------------------------------
        if not filename:

            timestamp = datetime.now().strftime(

                "%Y%m%d_%H%M%S"
            )

            filename = (
                f"access_log_export_"
                f"{timestamp}.csv"
            )

        # ---------------------------------
        # Ensure CSV Extension
        # ---------------------------------
        if not filename.endswith(".csv"):

            filename += ".csv"

        # ---------------------------------
        # Full Path
        # ---------------------------------
        full_path = os.path.join(

            self.export_dir,

            filename
        )

        # ---------------------------------
        # Export
        # ---------------------------------
        df.to_csv(

            full_path,

            index=False
        )

        print(
            f"\n✅ Exported: "
            f"{full_path}\n"
        )


    # ---------------------------------
    # Show Results
    # ---------------------------------
    def show_and_export(

        self,

        title,

        df,

        display
    ):

        display.section_header(
            title
        )

        display.dataframe(df)


    # ---------------------------------
    # Export Analytics Workbook
    # ---------------------------------
    def export_multiple(

        self,

        datasets,

        report_name="analytics_report"
    ):

        choice = input(

            "\nExport analytics report "
            "to Excel? (y/n): "

        ).strip().lower()

        if choice != "y":

            return

        filename = input(

            "\nEnter report filename "
            "(leave blank for auto-name): "

        ).strip()

        if not filename:

            filename = report_name

        self.export_to_excel(

            datasets,

            filename
        )


    
    # ---------------------------------
    # Export Multiple DataFrames
    # To Excel Workbook
    # ---------------------------------
    def export_to_excel(

        self,

        datasets,

        filename="analytics_report.xlsx"
    ):

        # ---------------------------------
        # Ensure Extension
        # ---------------------------------
        if not filename.endswith(".xlsx"):

            filename += ".xlsx"

        # ---------------------------------
        # Full Path
        # ---------------------------------
        full_path = os.path.join(

            self.export_dir,

            filename
        )

        # ---------------------------------
        # Write Workbook
        # ---------------------------------
        with pd.ExcelWriter(

            full_path,

            engine="openpyxl"
        ) as writer:

            for sheet_name, df in datasets.items():

                if df.empty:

                    continue

                temp_df = df.copy()

                for col in temp_df.columns:

                    if pd.api.types.is_datetime64tz_dtype(
                        temp_df[col]
                    ):

                        temp_df[col] = (
                            temp_df[col]
                            .dt.tz_localize(None)
                        )

                temp_df.to_excel(

                    writer,

                    sheet_name=sheet_name[:31],

                    index=False
                )

        print(
            f"\n✅ Exported Excel Report: "
            f"{full_path}\n"
        )


    # ---------------------------------
    # Prompt Single CSV Export
    # ---------------------------------
    def prompt_single_export(

        self,

        df,

        default_filename="export"
    ):

        # ---------------------------------
        # Skip Empty DataFrame
        # ---------------------------------
        if df.empty:

            return

        # ---------------------------------
        # Ask Export
        # ---------------------------------
        choice = input(

            "\nExport results to CSV? "
            "(y/n): "

        ).strip().lower()

        if choice != "y":

            return

        # ---------------------------------
        # Ask Filename
        # ---------------------------------
        filename = input(

            "\nEnter filename "
            "(leave blank for auto-name): "

        ).strip()

        if not filename:

            filename = default_filename

        # ---------------------------------
        # Export
        # ---------------------------------
        self.to_csv(

            df,

            filename
        )
