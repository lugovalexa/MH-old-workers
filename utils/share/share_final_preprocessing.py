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
    elif row["year"] == 2013:
        return row["yrscontribution2017"] - 4
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
        "Switzerland": switzerland_age,
    }
    if country in country_functions_age:
        return country_functions_age[country](row)
    else:
        return None


def calculate_horizon_change1(row):
    """
    Calculate the retirement age change based on country- and year-specific retirement reforms.
    Takes into account the maximum possible criteria of eligibility to change, including age, gender, number of children, industry of employment, etc.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of a DataFrame containing relevant information.

    Returns:
    - int or None: The calculated retirement age change for the given country, or None if the country is not found.

    Note:
    - This function relies on specific functions for each country to calculate retirement age.
    - The functions for each country should are defined separately (e.g., austria_change, belgium_change) and are located in utils/retirement folder.
    """
    country = row["country"]
    country_functions_change = {
        "Austria": austria_change1,
        "Belgium": belgium_change1,
        "Czech Republic": czech_republic_change1,
        "Denmark": denmark_change1,
        "Estonia": estonia_change1,
        "France": france_change1,
        "Germany": germany_change1,
        "Italy": italy_change1,
        "Slovenia": slovenia_change1,
        "Spain": spain_change1,
        "Switzerland": switzerland_change1,
    }
    if country in country_functions_change:
        return country_functions_change[country](row)
    else:
        return None


def calculate_horizon_change(row):
    """
    Calculate the retirement age change based on country- and year-specific retirement reforms.
    Takes into account the maximum possible criteria of eligibility to change, including age, gender, number of children, industry of employment, etc.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of a DataFrame containing relevant information.

    Returns:
    - int or None: The calculated retirement age change for the given country, or None if the country is not found.

    Note:
    - This function relies on specific functions for each country to calculate retirement age.
    - The functions for each country should are defined separately (e.g., austria_change, belgium_change) and are located in utils/retirement folder.
    """
    country = row["country"]
    country_functions_change = {
        "Austria": austria_change,
        "Belgium": belgium_change,
        "Czech Republic": czech_republic_change,
        "Denmark": denmark_change,
        "Estonia": estonia_change,
        "France": france_change,
        "Germany": germany_change,
        "Italy": italy_change,
        "Slovenia": slovenia_change,
        "Spain": spain_change,
        "Switzerland": switzerland_change,
    }
    if country in country_functions_change:
        return country_functions_change[country](row)
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

    # Set legal retirement age
    df["retirement_age"] = df.apply(calculate_retirement_age, axis=1)

    # Delete those who are above the retirement age (continue to work longer)
    df = df[df["retirement_age"] > df["age"]].reset_index(drop=True)

    # Calculate resting work horizon
    df["work_horizon"] = df["retirement_age"] - df["age"]

    # Calculate change of retirement age induced by reform
    df["work_horizon_change_yearly"] = df.apply(calculate_horizon_change, axis=1)
    df["work_horizon_change"] = df.apply(calculate_horizon_change1, axis=1)

    grouped_df = df.groupby("mergeid")["work_horizon_change_yearly"].sum().reset_index()
    grouped_df.rename(
        columns={"work_horizon_change_yearly": "work_horizon_change_total"},
        inplace=True,
    )
    df = pd.merge(df, grouped_df, on="mergeid", how="left")
    df["work_horizon_change_total"] = df["work_horizon_change_total"].where(
        df["year"] == 2015, 0
    )

    print(
        "Retirement age, work horizon and work horizon change by reforms - calculated"
    )

    # Add weights imputed in STATA
    df = add_weights(
        df,
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/weights/",
    )

    print("Longitudinal weights imputed in STATA - added")

    return df
