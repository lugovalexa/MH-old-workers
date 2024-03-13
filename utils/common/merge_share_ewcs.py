import os

import pandas as pd


def merge_share_ewcs(
    output_csv,
    convert_to_3_digits=False,
):
    """
    Merge two datasets (SHARE and EWCS) based on specified conditions.

    Parameters:
    - output_csv (str): The path to save the merged dataset CSV file.
    - convert_to_3_digits (bool, optional): If True, convert isco codes to 3 digits.
    Note:
    The function reads two CSV files, 'share_clean_w46.csv' and either 'work_quality_indexes_country_3digits.csv'
    or 'work_quality_indexes_country_4digits.csv', depending on the `convert_to_3_digits` parameter.
    The merged dataset is saved to the specified `output_csv` file.

    Examples:
    >>> merge_share_ewcs("output_merged_data.csv", convert_to_3_digits=True)
    """
    # Set directory
    os.chdir(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/"
    )

    # Read input CSVs
    df = pd.read_csv("share_clean_w46.csv")
    if convert_to_3_digits:
        indexes = pd.read_csv("work_quality_indexes_country_3digits.csv")
    else:
        indexes = pd.read_csv("work_quality_indexes_country_4digits.csv")

    # Optional: Convert isco to 3 digits
    if convert_to_3_digits:
        df["isco"] = df["isco"].apply(lambda x: int(str(x)[:-1]) if x >= 1000 else x)
        indexes["isco"] = indexes["isco"].apply(
            lambda x: int(str(x)[:-1]) if x >= 1000 else x
        )

    # Merge on specified columns
    df = df.merge(indexes, on=["country", "isco"], how="left")

    df = df.dropna(subset="jqi_sum").reset_index(drop=True)

    # Ensure a balanced panel
    # unique_mergeid_2011 = set(df[df.year == 2011]["mergeid"].unique())
    # unique_mergeid_2015 = set(df[df.year == 2015]["mergeid"].unique())
    # intersection_ids = unique_mergeid_2011.intersection(unique_mergeid_2015)

    # df = df[df["mergeid"].isin(intersection_ids)].reset_index(drop=True)

    # Save to output CSV
    df.to_csv(output_csv, index=False)
