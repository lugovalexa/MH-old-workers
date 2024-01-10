import os

import pandas as pd

from ..retirement import *


def calculate_contribution(row):
    if row["year"] == 2011:
        return row["yrscontribution2017"] - 6
    elif row["year"] == 2013:
        return row["yrscontribution2017"] - 4
    else:
        return row["yrscontribution2017"] - 2


def calculate_retirement_age(row):
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


def calculate_horizon_change(row):
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


def add_weights(df, weights_folder_path):
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
    df["work_horizon_change"] = df.apply(calculate_horizon_change, axis=1)

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
