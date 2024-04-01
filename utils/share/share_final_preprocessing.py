import os

import pandas as pd

from ..retirement import *


def get_last_valid(row):
    """
    Retrieve the last valid value from a Pandas Series along each row.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of data.

    Returns:
    - pd.Series or pd.NA: The last valid value in the row, or pd.NA if no valid value is found.
    """
    last_valid_index = row.last_valid_index()
    if pd.notnull(last_valid_index):
        return row[last_valid_index]
    else:
        return pd.NA


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
    df = df[df.yrscontribution >= 10].reset_index(drop=True)

    print(
        "Current years of contribution - calculated, those with less 10 years - deleted"
    )

    # Change some data types
    columns_to_convert = ["partnerinhh", "eurod", "eurodcat", "yrbirth"]
    df[columns_to_convert] = df[columns_to_convert].apply(
        pd.to_numeric, errors="coerce"
    )
    df.dropna(subset=columns_to_convert, inplace=True)

    print("Data types - corrected")
    print(f"N obs after data types: {len(df)}")

    # Leave only individuals present at least in two waves
    # id_counts = df["mergeid"].value_counts()
    # ids_to_keep = id_counts[id_counts >= 2].index
    # df = df[df["mergeid"].isin(ids_to_keep)].reset_index(drop=True)

    # print("Only those present in at least 2 waves left")
    # print(f"N obs after id filter: {len(df)}")

    # Set legal retirement age

    # Synthesize data for wave 4 when missing
    # mergeid_counts4 = df[df["wave"].isin([5, 6])]["mergeid"].value_counts()
    # unique_mergeids4 = mergeid_counts4[mergeid_counts4 == 2].index
    # unique_mergeids4 = mergeid_counts4.index
    # mergeid_counts41 = df[df["wave"] == 4]["mergeid"].value_counts()
    # unique_mergeids41 = mergeid_counts41.index
    # unique_rows4 = df[
    #    (df["mergeid"].isin(unique_mergeids4))
    #    & (~df["mergeid"].isin(unique_mergeids41))
    # ]
    # unique_rows4 = unique_rows4[unique_rows4.wave == 5].reset_index(drop=True)
    # unique_rows4["age"] = unique_rows4["age"] - 2
    # unique_rows4["year"] = unique_rows4["year"] - 2
    # unique_rows4["yrscontribution"] = unique_rows4["yrscontribution"] - 2
    # unique_rows4["wave"] = unique_rows4["wave"] - 1

    # Synthesize data for wave 5 when missing
    # mergeid_counts5 = df[df["wave"].isin([4, 6])]["mergeid"].value_counts()
    # unique_mergeids5 = mergeid_counts5[mergeid_counts5 == 2].index
    # mergeid_counts51 = df[df["wave"] == 5]["mergeid"].value_counts()
    # unique_mergeids51 = mergeid_counts51.index
    # unique_rows5 = df[
    #     (df["mergeid"].isin(unique_mergeids5))
    #     & (~df["mergeid"].isin(unique_mergeids51))
    # ]
    # unique_rows5 = unique_rows5[unique_rows5.wave == 6].reset_index(drop=True)
    # unique_rows5["age"] = unique_rows5["age"] - 2
    # unique_rows5["year"] = unique_rows5["year"] - 2
    # unique_rows5["yrscontribution"] = unique_rows5["yrscontribution"] - 2
    # unique_rows5["wave"] = unique_rows5["wave"] - 1

    # Synthesize data for wave 6 when missing
    # mergeid_counts6 = df[df["wave"].isin([4, 5])]["mergeid"].value_counts()
    # unique_mergeids6 = mergeid_counts6[mergeid_counts6 == 2].index
    # mergeid_counts61 = df[df["wave"] == 6]["mergeid"].value_counts()
    # unique_mergeids61 = mergeid_counts61.index
    # unique_rows6 = df[
    #     (df["mergeid"].isin(unique_mergeids6))
    #     & (~df["mergeid"].isin(unique_mergeids61))
    # ]
    # unique_rows6 = unique_rows6[unique_rows6.wave == 5].reset_index(drop=True)
    # unique_rows6["age"] = unique_rows6["age"] + 2
    # unique_rows6["year"] = unique_rows6["year"] + 2
    # unique_rows6["yrscontribution"] = unique_rows6["yrscontribution"] + 2
    # unique_rows6["wave"] = unique_rows6["wave"] + 1

    unique_mergeids6 = df[df["wave"] == 6]["mergeid"].unique()
    unique_mergeids5 = df[df["wave"] == 5]["mergeid"].unique()
    unique_mergeids4 = df[df["wave"] == 4]["mergeid"].unique()

    unique_rows4 = df[
        (df["wave"] == 5) & (~df["mergeid"].isin(unique_mergeids4))
    ].reset_index(drop=True)
    unique_rows4["age"] = unique_rows4["age"] - 2
    unique_rows4["year"] = unique_rows4["year"] - 2
    unique_rows4["yrscontribution"] = unique_rows4["yrscontribution"] - 2
    unique_rows4["wave"] = unique_rows4["wave"] - 1

    unique_rows5 = df[
        (df["wave"] == 6) & (~df["mergeid"].isin(unique_mergeids5))
    ].reset_index(drop=True)
    unique_rows5["age"] = unique_rows5["age"] - 2
    unique_rows5["year"] = unique_rows5["year"] - 2
    unique_rows5["yrscontribution"] = unique_rows5["yrscontribution"] - 2
    unique_rows5["wave"] = unique_rows5["wave"] - 1

    unique_rows51 = df[
        (df["wave"] == 4) & (~df["mergeid"].isin(unique_mergeids5))
    ].reset_index(drop=True)
    unique_rows51["age"] = unique_rows51["age"] + 2
    unique_rows51["year"] = unique_rows51["year"] + 2
    unique_rows51["yrscontribution"] = unique_rows51["yrscontribution"] + 2
    unique_rows51["wave"] = unique_rows51["wave"] + 1

    unique_rows6 = df[
        (df["wave"] == 5) & (~df["mergeid"].isin(unique_mergeids6))
    ].reset_index(drop=True)
    unique_rows6["age"] = unique_rows6["age"] + 2
    unique_rows6["year"] = unique_rows6["year"] + 2
    unique_rows6["yrscontribution"] = unique_rows6["yrscontribution"] + 2
    unique_rows6["wave"] = unique_rows6["wave"] + 1

    # Block of waves 4 and 5
    # Concatenate additional synthetisized data with main df
    retirement1 = pd.concat(
        [df[df.wave.isin([4, 5])], unique_rows4, unique_rows51], ignore_index=True
    )
    retirement1 = retirement1.reset_index(drop=True)

    # Run retirement age functions
    retirement1["retirement_age"] = retirement1.apply(calculate_retirement_age, axis=1)
    retirement1 = retirement1.dropna(subset="retirement_age").reset_index(drop=True)
    retirement1["retirement_age_early"] = retirement1.apply(
        calculate_retirement_age_early, axis=1
    )
    retirement1["retirement_age_minimum"] = retirement1[
        ["retirement_age", "retirement_age_early"]
    ].min(axis=1)

    # Calculate resting work horizon
    retirement1["work_horizon"] = retirement1["retirement_age"] - retirement1["age"]

    retirement1["work_horizon_minimum"] = (
        retirement1["retirement_age_minimum"] - retirement1["age"]
    )

    retirement1 = retirement1[
        (retirement1.work_horizon_minimum >= 1)
        & (retirement1.work_horizon_minimum <= 10)
    ].reset_index(drop=True)

    # Change in work horizon
    horizon2011 = (
        retirement1[retirement1.year == 2011]
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
    horizon2013 = (
        retirement1[retirement1.year == 2013]
        .groupby("mergeid")[["work_horizon", "work_horizon_minimum"]]
        .max()
        .reset_index()
        .rename(
            columns={
                "work_horizon": "work_horizon2013",
                "work_horizon_minimum": "work_horizon2013_minimum",
            }
        )
    )
    horizon_change = horizon2011.merge(horizon2013, on="mergeid", how="inner")
    horizon_change["work_horizon2013_expected"] = horizon_change["work_horizon2011"] - 2
    horizon_change["work_horizon_change"] = (
        horizon_change["work_horizon2013"] - horizon_change["work_horizon2013_expected"]
    )
    horizon_change["work_horizon2013_minimum_expected"] = (
        horizon_change["work_horizon2011_minimum"] - 2
    )
    horizon_change["work_horizon_change_minimum"] = (
        horizon_change["work_horizon2013_minimum"]
        - horizon_change["work_horizon2013_minimum_expected"]
    )
    retirement1 = retirement1.merge(
        horizon_change[
            ["mergeid", "work_horizon_change", "work_horizon_change_minimum"]
        ],
        on="mergeid",
        how="inner",
    )
    retirement1 = retirement1[
        (retirement1.work_horizon_change >= 0)
        & (retirement1.work_horizon_change_minimum >= 0)
    ].reset_index(drop=True)

    # Block of waves 5 and 6
    # Concatenate additional synthetisized data with main df
    retirement2 = pd.concat(
        [df[df.wave.isin([5, 6])], unique_rows5, unique_rows6], ignore_index=True
    )
    retirement2 = retirement2.reset_index(drop=True)

    # Run retirement age functions
    retirement2["retirement_age"] = retirement2.apply(calculate_retirement_age, axis=1)
    retirement2 = retirement2.dropna(subset="retirement_age").reset_index(drop=True)
    retirement2["retirement_age_early"] = retirement2.apply(
        calculate_retirement_age_early, axis=1
    )
    retirement2["retirement_age_minimum"] = retirement2[
        ["retirement_age", "retirement_age_early"]
    ].min(axis=1)

    # Calculate resting work horizon
    retirement2["work_horizon"] = retirement2["retirement_age"] - retirement2["age"]

    retirement2["work_horizon_minimum"] = (
        retirement2["retirement_age_minimum"] - retirement2["age"]
    )

    retirement2 = retirement2[
        (retirement2.work_horizon_minimum >= 1)
        & (retirement2.work_horizon_minimum <= 10)
    ].reset_index(drop=True)

    # Change in work horizon
    horizon2013 = (
        retirement2[retirement2.year == 2013]
        .groupby("mergeid")[["work_horizon", "work_horizon_minimum"]]
        .max()
        .reset_index()
        .rename(
            columns={
                "work_horizon": "work_horizon2013",
                "work_horizon_minimum": "work_horizon2013_minimum",
            }
        )
    )
    horizon2015 = (
        retirement2[retirement2.year == 2015]
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
    horizon_change = horizon2013.merge(horizon2015, on="mergeid", how="inner")
    horizon_change["work_horizon2015_expected"] = horizon_change["work_horizon2013"] - 2
    horizon_change["work_horizon_change"] = (
        horizon_change["work_horizon2015"] - horizon_change["work_horizon2015_expected"]
    )
    horizon_change["work_horizon2015_minimum_expected"] = (
        horizon_change["work_horizon2013_minimum"] - 2
    )
    horizon_change["work_horizon_change_minimum"] = (
        horizon_change["work_horizon2015_minimum"]
        - horizon_change["work_horizon2015_minimum_expected"]
    )
    retirement2 = retirement2.merge(
        horizon_change[
            ["mergeid", "work_horizon_change", "work_horizon_change_minimum"]
        ],
        on="mergeid",
        how="inner",
    )
    retirement2 = retirement2[
        (retirement2.work_horizon_change >= 0)
        & (retirement2.work_horizon_change_minimum >= 0)
    ].reset_index(drop=True)

    # Merge resulting columns with main df
    df1 = df.merge(
        retirement1[
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
    df1["wblock56"] = 0

    df2 = df.merge(
        retirement2[
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
    df2["wblock56"] = 1

    df = pd.concat([df1, df2], ignore_index=True)

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
    weights2011["wave"] = 4
    weights2013 = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew5_rel8-0-0_ALL_datasets_stata/sharew5_rel8-0-0_gv_weights.dta"
    )
    weights2013["wave"] = 5
    weights2015 = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew6_rel8-0-0_ALL_datasets_stata/sharew6_rel8-0-0_gv_weights.dta"
    )
    weights2015["wave"] = 6
    df = df.merge(
        weights2011[["mergeid", "wave", "cciw_w4"]], on=["mergeid", "wave"], how="left"
    )
    df = df.merge(
        weights2013[["mergeid", "wave", "cciw_w5"]], on=["mergeid", "wave"], how="left"
    )
    df = df.merge(
        weights2015[["mergeid", "wave", "cciw_w6"]], on=["mergeid", "wave"], how="left"
    )

    df["cciw"] = df[["cciw_w4", "cciw_w5", "cciw_w6"]].apply(get_last_valid, axis=1)
    df = df.dropna(subset="cciw").reset_index(drop=True)

    print("Longitudinal and crossectional weights - added")
    print(f"N obs after weights: {len(df)}")

    # Format isco column
    df["isco"] = pd.NA
    df.loc[df["year"] == 2011, "isco"] = df.loc[df["year"] == 2011, "isco2011"]
    df.loc[df["year"] == 2013, "isco"] = df.loc[df["year"] == 2013, "isco2013"]
    df.loc[df["year"] == 2015, "isco"] = df.loc[df["year"] == 2015, "isco2015"]

    # Create column for 1 digit ISCO
    df["isco1"] = df["isco"].astype(str).str[0]
    df["isco1"] = df["isco1"].astype(int)

    # Edit gender column
    df["gender"] = df["gender"].replace({"Male": 0, "Female": 1})

    # Create variable first treated
    first_treated_years = (
        df.loc[(df["year"] > 2011) & (df["work_horizon_change_minimum"] > 0)]
        .groupby("mergeid")["year"]
        .min()
        .reset_index()
    )
    first_treated_dict = dict(
        zip(first_treated_years["mergeid"], first_treated_years["year"])
    )
    df["first_treated"] = df["mergeid"].map(lambda x: first_treated_dict.get(x, 0))

    return df
