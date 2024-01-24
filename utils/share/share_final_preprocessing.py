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
        "Italy": italy_age,
        "Slovenia": slovenia_age,
        "Spain": spain_age,
        "Sweden": sweden_age,
        "Switzerland": switzerland_age,
    }
    if country in country_functions_age:
        return country_functions_age[country](row)
    else:
        return None


def add_weights(df, weights_folder_path):
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
    - Rows with missing weights ("my_wgt") will be dropped from the resulting DataFrame.
    """
    file_list = os.listdir(weights_folder_path)
    datasets = []
    for file in file_list:
        if file.endswith(".dta"):
            file_path = os.path.join(weights_folder_path, file)
            data = pd.read_stata(file_path)
            datasets.append(data)
    weights = pd.concat(datasets, ignore_index=True)[["mergeid", "dw_w4", "my_wgt"]]

    df = df.merge(weights, on="mergeid", how="left")
    df = df.dropna(subset=["my_wgt"]).reset_index(drop=True)

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
    df["retirement_age"] = df.apply(calculate_retirement_age, axis=1)

    # Delete those who are above the retirement age (continue to work longer)
    df = df[df["retirement_age"] > df["age"]].reset_index(drop=True)

    print(f"N obs retirement age and filter to be under it: {len(df)}")

    # Calculate resting work horizon
    df["work_horizon"] = df["retirement_age"] - df["age"]
    df = df[df.work_horizon <= 15].reset_index(drop=True)

    # Change in work horizon
    horizon2011 = (
        df[df.year == 2011]
        .groupby("mergeid")["work_horizon"]
        .max()
        .reset_index()
        .rename(columns={"work_horizon": "work_horizon2011"})
    )
    horizon2015 = (
        df[df.year == 2015]
        .groupby("mergeid")["work_horizon"]
        .max()
        .reset_index()
        .rename(columns={"work_horizon": "work_horizon2015"})
    )
    horizon_change = horizon2011.merge(horizon2015, on="mergeid", how="left")
    horizon_change = horizon_change.dropna().reset_index(drop=True)
    horizon_change["work_horizon2015_expected"] = horizon_change["work_horizon2011"] - 4
    horizon_change["work_horizon_change"] = (
        horizon_change["work_horizon2015"] - horizon_change["work_horizon2015_expected"]
    )
    df = df.merge(
        horizon_change[["mergeid", "work_horizon_change"]], on="mergeid", how="left"
    )
    df = df.dropna(subset="work_horizon_change").reset_index(drop=True)
    df = df[df.work_horizon_change >= 0].reset_index(drop=True)

    print(
        "Retirement age, work horizon and work horizon change by reforms - calculated"
    )

    # Add weights imputed in STATA
    df = add_weights(
        df,
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/weights/",
    )

    print("Longitudinal weights imputed in STATA - added")
    print(f"N obs after weights: {len(df)}")

    return df
