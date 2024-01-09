import os

import pandas as pd


def merge_share_ewcs(
    output_csv,
    not_country_wise=False,
    convert_to_3_digits=False,
    exclude_wave_5=False,
    balanced=False,
):
    # Set directory
    os.chdir(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/"
    )

    # Read input CSVs
    df = pd.read_csv("data_clean_w456.csv")
    indexes = pd.read_csv("work_quality_indexes_year_country.csv")

    # Optional: aggregate indexes if year only-wise merge
    if not_country_wise:
        indexes = (
            indexes.drop(columns="country")
            .groupby(["year", "isco"])
            .mean()
            .reset_index()
        )

    # Optional: Convert isco to 3 digits
    if convert_to_3_digits:
        df["isco"] = df["isco"].apply(lambda x: int(str(x)[:-1]) if x >= 1000 else x)
        indexes["isco"] = indexes["isco"].apply(
            lambda x: int(str(x)[:-1]) if x >= 1000 else x
        )

    # Optional: exclude wave 5
    if exclude_wave_5:
        df = df[df.wave != 5].reset_index(drop=True)

    # Optional: balanced panel
    if balanced:
        if exclude_wave_5:
            unique_mergeid_w4 = set(df[df.wave == 4]["mergeid"].unique())
            unique_mergeid_w6 = set(df[df.wave == 6]["mergeid"].unique())
            intersection_ids = unique_mergeid_w4.intersection(unique_mergeid_w6)
            df = df[df["mergeid"].isin(intersection_ids)].reset_index(drop=True)
        else:
            unique_mergeid_w4 = set(df[df.wave == 4]["mergeid"].unique())
            unique_mergeid_w5 = set(df[df.wave == 5]["mergeid"].unique())
            unique_mergeid_w6 = set(df[df.wave == 6]["mergeid"].unique())
            intersection_ids = unique_mergeid_w4.intersection(
                unique_mergeid_w5
            ).intersection(unique_mergeid_w6)
            df = df[df["mergeid"].isin(intersection_ids)].reset_index(drop=True)

    # Merge on specified columns
    if not_country_wise:
        df = df.merge(indexes, on=["year", "isco"], how="inner")
    else:
        df = df.merge(indexes, on=["year", "country", "isco"], how="inner")

    # Save to output CSV
    df.to_csv(output_csv, index=False)
