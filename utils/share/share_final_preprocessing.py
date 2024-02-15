import os

import pandas as pd

from ..retirement import *


def calculate_contribution(row):
    """
    Calculate the years of contribution to social security for the current year.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of a DataFrame containing relevant information.

    Returns:
    - int: The calculated years of contribution to social security for the current year.
    """
    if row["year"] == 2011:
        return row["yrscontribution2017"] - 6
    else:
        return row["yrscontribution2017"] - 2


def calculate_retirement_age(row):
    """
    Calculate the retirement age based on country- and year-specific retirement rules.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of a DataFrame containing relevant information.

    Returns:
    - int or None: The calculated retirement age for the given country, or None if the country is not found.

    Note:
    - This function relies on specific functions for each country to calculate retirement age.
    - The functions for each country should are defined separately (e.g., austria_age, belgium_age) and are located in utils/retirement folder.
    """
    country = row["country"]
    country_functions_age = {
        "Austria": austria_age,
        "Belgium": belgium_age,
        "Czech Republic": czech_republic_age,
        "Denmark": denmark_age,
        "Estonia": estonia_age,
        "France": france_age,
        "Germany": germany_age,
        "Greece": greece_age,
        "Hungary": hungary_age,
        "Italy": italy_age,
        "Luxembourg": luxembourg_age,
        "Netherlands": netherlands_age,
        "Poland": poland_age,
        "Portugal": portugal_age,
        "Slovenia": slovenia_age,
        "Spain": spain_age,
        "Sweden": sweden_age,
        "Switzerland": switzerland_age,
    }
    if country in country_functions_age:
        return country_functions_age[country](row)
    else:
        return None


def calculate_retirement_age_early(row):
    """
    Calculate the early retirement age based on country- and year-specific retirement rules.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of a DataFrame containing relevant information.

    Returns:
    - int or None: The calculated early retirement age for the given country, or None if the country is not found.

    Note:
    - This function relies on specific functions for each country to calculate early retirement age.
    - The functions for each country should are defined separately (e.g., austria_age_early, belgium_age_early) and are located in utils/retirement folder.
    """
    country = row["country"]
    country_functions_age = {
        "Austria": austria_age_early,
        "Belgium": belgium_age_early,
        "Czech Republic": czech_republic_age_early,
        "Denmark": denmark_age_early,
        "Estonia": estonia_age_early,
        "France": france_age_early,
        "Germany": germany_age_early,
        "Greece": greece_age_early,
        "Hungary": hungary_age_early,
        "Italy": italy_age_early,
        "Luxembourg": luxembourg_age_early,
        "Netherlands": netherlands_age_early,
        "Poland": poland_age_early,
        "Portugal": portugal_age_early,
        "Slovenia": slovenia_age_early,
        "Spain": spain_age_early,
        "Sweden": sweden_age_early,
        "Switzerland": switzerland_age_early,
    }
    if country in country_functions_age:
        return country_functions_age[country](row)
    else:
        return None


def add_weights_longitudinal(df, weights_folder_path):
    """
    Add longitudinal weights to a DataFrame based on STATA-calculated weights following SHARE templates.

    Parameters:
    - df (pd.DataFrame): The DataFrame to which weights will be added.
    - weights_folder_path (str): The path to the folder containing STATA-calculated weight files.

    Returns:
    - pd.DataFrame: The DataFrame with longitudinal weights added.

    Note:
    - The function assumes that weight files in the specified folder follow SHARE templates.
    - Weight files are expected to be in Stata format (.dta) and contain columns "mergeid", "dw_w4", and "my_wgt".
    - The resulting DataFrame will be merged with the input DataFrame based on the "mergeid" column.
    """
    file_list = os.listdir(weights_folder_path)
    datasets = []
    for file in file_list:
        if file.endswith(".dta"):
            file_path = os.path.join(weights_folder_path, file)
            data = pd.read_stata(file_path)
            datasets.append(data)
    weights = pd.concat(datasets, ignore_index=True)[["mergeid", "my_wgt"]]

    df = df.merge(weights, on="mergeid", how="left")

    return df


def share_final_preprocessing(df):
    """
    Perform SHARE dataset final preprocessing steps, including age column removal, years of contribution recalculation,
    data type corrections, setting legal retirement age, filtering individuals above retirement age,
    calculating work horizon, change of retirement age induced by reform, and adding longitudinal weights.

    Parameters:
    - df (pd.DataFrame): The input DataFrame representing SHARE survey data.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with added features and applied modifications.
    """
    print(f"N obs initial: {len(df)}")

    # Convert gender to text
    df["gender"] = df["gender"].replace({1: "Female", 0: "Male"})

    # Drop extra age columns
    df = df.drop(columns=["age2015", "age2017", "age2020"])

    # Recalculate years of contribution
    df["yrscontribution"] = df.apply(calculate_contribution, axis=1)
    df = df.drop(columns="yrscontribution2017")

    print("Current years of contribution - calculated")

    # Change some data types
    columns_to_convert = ["partnerinhh", "eurod", "eurodcat", "yrbirth"]
    df[columns_to_convert] = df[columns_to_convert].apply(
        pd.to_numeric, errors="coerce"
    )
    df.dropna(subset=columns_to_convert, inplace=True)

    print("Data types - corrected")
    print(f"N obs after data types: {len(df)}")

    # Set legal retirement age

    # Synthesize data for wave 4 for those only present in wave 6
    mergeid_counts6 = df["mergeid"].value_counts()
    unique_mergeids6 = mergeid_counts6[mergeid_counts6 == 1].index
    unique_rows6 = df[df["mergeid"].isin(unique_mergeids6)]
    unique_rows6 = unique_rows6[unique_rows6.wave == 6].reset_index(drop=True)
    unique_rows6["age"] = unique_rows6["age"] - 4
    unique_rows6["year"] = unique_rows6["year"] - 4
    unique_rows6["yrscontribution"] = unique_rows6["yrscontribution"] - 4
    unique_rows6["wave"] = unique_rows6["wave"] - 2

    # Synthesize data for wave 6 for those only present in wave 4
    unique_rows4 = df[df["mergeid"].isin(unique_mergeids6)]
    unique_rows4 = unique_rows4[unique_rows4.wave == 4].reset_index(drop=True)
    unique_rows4["age"] = unique_rows4["age"] + 4
    unique_rows4["year"] = unique_rows4["year"] + 4
    unique_rows4["yrscontribution"] = unique_rows4["yrscontribution"] + 4
    unique_rows4["wave"] = unique_rows4["wave"] + 2

    # Concatenate additional synthetisized data with main df
    retirement = pd.concat([df, unique_rows6, unique_rows4], ignore_index=True)

    # Run retirement age functions
    retirement["retirement_age"] = retirement.apply(calculate_retirement_age, axis=1)
    retirement = retirement.dropna(subset="retirement_age").reset_index(drop=True)
    retirement["retirement_age_early"] = retirement.apply(
        calculate_retirement_age_early, axis=1
    )
    retirement["retirement_age_minimum"] = retirement[
        ["retirement_age", "retirement_age_early"]
    ].min(axis=1)

    # Calculate resting work horizon
    retirement["work_horizon"] = retirement["retirement_age"] - retirement["age"]

    retirement["work_horizon_minimum"] = (
        retirement["retirement_age_minimum"] - retirement["age"]
    )

    retirement = retirement[
        (retirement.work_horizon >= 1) & (retirement.work_horizon <= 15)
    ].reset_index(drop=True)

    # Change in work horizon
    horizon2011 = (
        retirement[retirement.year == 2011]
        .groupby("mergeid")[["work_horizon", "work_horizon_minimum"]]
        .max()
        .reset_index()
        .rename(
            columns={
                "work_horizon": "work_horizon2011",
                "work_horizon_minimum": "work_horizon2011_minimum",
            }
        )
    )
    horizon2015 = (
        retirement[retirement.year == 2015]
        .groupby("mergeid")[["work_horizon", "work_horizon_minimum"]]
        .max()
        .reset_index()
        .rename(
            columns={
                "work_horizon": "work_horizon2015",
                "work_horizon_minimum": "work_horizon2015_minimum",
            }
        )
    )
    horizon_change = horizon2011.merge(horizon2015, on="mergeid", how="inner")
    horizon_change["work_horizon2015_expected"] = horizon_change["work_horizon2011"] - 4
    horizon_change["work_horizon_change"] = (
        horizon_change["work_horizon2015"] - horizon_change["work_horizon2015_expected"]
    )
    horizon_change["work_horizon2015_minimum_expected"] = (
        horizon_change["work_horizon2011_minimum"] - 4
    )
    horizon_change["work_horizon_change_minimum"] = (
        horizon_change["work_horizon2015_minimum"]
        - horizon_change["work_horizon2015_minimum_expected"]
    )
    retirement = retirement.merge(
        horizon_change[
            ["mergeid", "work_horizon_change", "work_horizon_change_minimum"]
        ],
        on="mergeid",
        how="inner",
    )
    retirement = retirement[
        (retirement.work_horizon_change >= 0)
        & (retirement.work_horizon_change_minimum >= 0)
    ].reset_index(drop=True)

    # Merge resulting columns with main df
    df = df.merge(
        retirement[
            [
                "mergeid",
                "wave",
                "retirement_age",
                "retirement_age_early",
                "retirement_age_minimum",
                "work_horizon",
                "work_horizon_minimum",
                "work_horizon_change",
                "work_horizon_change_minimum",
            ]
        ],
        on=["mergeid", "wave"],
        how="inner",
    )

    print(
        "Retirement age, work horizon and work horizon change by reforms - calculated"
    )
    print(f"N obs after work horizon change: {len(df)}")

    # Add longitudinal weights imputed in STATA
    df = add_weights_longitudinal(
        df,
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/weights/",
    )

    # Add crossectional weights provided by SHARE
    weights2011 = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew4_rel8-0-0_ALL_datasets_stata/sharew4_rel8-0-0_gv_weights.dta"
    )
    weights2015 = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew6_rel8-0-0_ALL_datasets_stata/sharew6_rel8-0-0_gv_weights.dta"
    )
    df = df.merge(weights2011[["mergeid", "cciw_w4"]], on="mergeid", how="left")
    df = df.merge(weights2015[["mergeid", "cciw_w6"]], on="mergeid", how="left")

    print("Longitudinal and crossectional weights - added")
    print(f"N obs after weights: {len(df)}")

    # Format isco column
    df["isco"] = pd.NA
    df.loc[df["year"] == 2011, "isco"] = df.loc[df["year"] == 2011, "isco2011"]
    df.loc[df["year"] == 2015, "isco"] = df.loc[df["year"] == 2015, "isco2015"]
    df = df.drop(columns=["isco2011", "isco2015"])

    return df
