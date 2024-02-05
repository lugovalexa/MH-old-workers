import os

import pandas as pd


def merge_share_ewcs(
    output_csv,
    not_country_wise=False,
    convert_to_3_digits=False,
):
    """
    Merge two datasets (SHARE and EWCS) based on specified conditions.

    Parameters:
    - output_csv (str): The path to save the merged dataset CSV file.
    - not_country_wise (bool, optional): If True, aggregate indexes by year and isco only.
    - convert_to_3_digits (bool, optional): If True, convert isco codes to 3 digits.
    - exclude_wave_5 (bool, optional): If True, exclude data from wave 5.
    - balanced (bool, optional): If True, create a balanced panel by keeping only common IDs between waves.

    Note:
    The function reads two CSV files, 'share_clean_w46.csv' and either 'work_quality_indexes_year_country_3digits.csv'
    or 'work_quality_indexes_year_country_4digits.csv', depending on the `convert_to_3_digits` parameter.
    The merged dataset is saved to the specified `output_csv` file.

    Examples:
    >>> merge_share_ewcs("output_merged_data.csv", not_country_wise=True, convert_to_3_digits=True)
    """
    # Set directory
    os.chdir(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/"
    )

    # Read input CSVs
    df = pd.read_csv("share_clean_w46.csv")
    if convert_to_3_digits:
        indexes = pd.read_csv("work_quality_indexes_year_country_3digits.csv")
    else:
        indexes = pd.read_csv("work_quality_indexes_year_country_4digits.csv")

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

    # Merge on specified columns
    if not_country_wise:
        df = df.merge(indexes, on=["year", "isco"], how="left")
    else:
        df = df.merge(indexes, on=["year", "country", "isco"], how="left")

    df = df.dropna(subset="jqi_sum").reset_index(drop=True)

    # Ensure a balanced panel
    # unique_mergeid_2011 = set(df[df.year == 2011]["mergeid"].unique())
    # unique_mergeid_2015 = set(df[df.year == 2015]["mergeid"].unique())
    # intersection_ids = unique_mergeid_2011.intersection(unique_mergeid_2015)

    # df = df[df["mergeid"].isin(intersection_ids)].reset_index(drop=True)

    # Save to output CSV
    df.to_csv(output_csv, index=False)
