import os

import numpy as np
import pandas as pd


def merge_share_ewcs(output_csv, convert_to_3_digits=False, balanced=False):
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

    # Create harmonized cciw weight
    grouped = (
        df.groupby("mergeid")[["cciw_w4", "cciw_w5", "cciw_w6"]].mean().reset_index()
    )
    grouped["cciw_new"] = grouped[["cciw_w4", "cciw_w5", "cciw_w6"]].mean(axis=1)
    df = pd.merge(df, grouped[["mergeid", "cciw_new"]], on="mergeid", how="left")

    # Create some new variables
    df["post"] = ((df["year"] == 2013) & (df["wblock56"] == 0)) | (df["year"] == 2015)
    df["post"] = df["post"].astype(int)

    df["cell"] = (
        df["country"]
        + "_"
        + df["gender"].astype(str)
        + "_"
        + df["wblock56"].astype(str)
    )
    df["cell_encoded"] = pd.factorize(df["cell"])[0]

    df["mergeid_encoded"] = pd.factorize(df["mergeid"])[0]

    df["agesq"] = df["age"] ** 2
    df["thinclog"] = np.log(df["thinc"])

    if balanced:
        # Leave a balanced sample by block of waves
        df1 = df[(df["wave"].isin([4, 5])) & (df["wblock56"] == 0)]
        mergeid_counts = df1["mergeid"].value_counts()
        df1 = df1[df1["mergeid"].isin(mergeid_counts[mergeid_counts == 2].index)]

        df2 = df[(df["wave"].isin([5, 6])) & (df["wblock56"] == 1)]
        mergeid_counts = df2["mergeid"].value_counts()
        df2 = df2[df2["mergeid"].isin(mergeid_counts[mergeid_counts == 2].index)]

        df = pd.concat([df1, df2], ignore_index=True)

        # Save to output CSV
        df.to_csv(output_csv, index=False)
    else:
        df.to_csv(output_csv, index=False)
