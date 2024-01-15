import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer
from scipy.linalg import eigh


def calculate_age(row):
    """
    Calculate the current age based on available information in the input row.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of a DataFrame containing relevant information.

    Returns:
    - float or np.nan: The calculated current age, or np.nan if there is insufficient information.
    """
    if not pd.isnull(row["age2011"]):
        return row["age2011"] + (row["year"] - 2011)
    elif not pd.isnull(row["age2013"]):
        return row["age2013"] - (2013 - row["year"])
    elif not pd.isnull(row["age2015"]):
        return row["age2015"] - (2015 - row["year"])
    else:
        return np.nan


def number_of_children(df):
    """
    Calculate the number of children and grandchildren for each individual in the DataFrame for the years 2011, 2013, and 2015.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing information about individuals and their children/grandchildren.

    Returns:
    - pd.DataFrame: The DataFrame with added columns for the number of children and grandchildren for each individual.
    """
    # Calculate number of children
    # Handle missing values
    df = df[(df.ch001_ != "Refusal")].reset_index(drop=True)
    df["ch001_"] = df["ch001_"].replace({"Don't know": 0})

    # Calculate number of children by household for each year
    children = (
        df.groupby(["hhid", "year"])["ch001_"]
        .max()
        .to_frame(name="nb_children")
        .reset_index()
        .fillna(0)
    )

    # Merge with main dataframe
    df = df.merge(children, on=["hhid", "year"], how="left")

    # Calculate number of grandchildren - the same process
    df = df[(df.ch021_ != "Refusal")].reset_index(drop=True)
    df["ch021_"] = df["ch021_"].replace({"Don't know": 0})

    grandchildren = (
        df.groupby(["hhid", "year"])["ch021_"]
        .max()
        .to_frame(name="nb_grandchildren")
        .reset_index()
        .fillna(0)
    )

    df = df.merge(grandchildren, on=["hhid", "year"], how="left")
    return df


def industry(df):
    """
    Identify the industry in which each individual works based on SHARE job episodes panel data.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing information about individuals.

    Returns:
    - pd.DataFrame: The DataFrame with an added 'industry' column representing the identified industry for each individual.
    ```
    """
    # Load job episodes panel
    jobs = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharewX_rel8-0-0_gv_job_episodes_panel.dta"
    )
    # Choose only employed individuals
    conditions = ["Employee or self-employed", "Short term job (less than 6 months)"]
    ep_data = jobs[jobs["situation"].isin(conditions)].sort_values(["mergeid", "year"])
    # Find the latest industry of employment
    last_industry = (
        ep_data.groupby("mergeid")["industry"]
        .apply(lambda x: x.dropna().iloc[-1] if not x.dropna().empty else np.nan)
        .reset_index()
    )
    # Merge with main df and drop missing values
    df = df.merge(last_industry, on="mergeid", how="left")
    df["industry"] = df["industry"].replace(["Don't know", "Refusal"], np.nan)
    df = df.dropna(subset="industry").reset_index(drop=True)

    return df


def finance(df):
    """
    Add financial information to the DataFrame, including household income, investments, and life insurance.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing information about individuals.

    Returns:
    - pd.DataFrame: The DataFrame with added columns representing financial information.

    Note:
    - The function reads household income data for waves 4, 5, and 6 from specific file paths.
    - It merges the household income information based on 'mergeid' and 'wave'.
    - Investments and life insurance columns are converted to binary (Yes: 1, No/Refusal/Don't know: 0).
    - All types of investments are aggregated into a single column to indicate 1 - has investments and 0 - no investments.
    - The resulting DataFrame includes additional columns: 'thinc' (household income), 'thinc2' (household income alternative), 'investment' (1 if present), and 'life_insurance' (1 if present).
    """
    # Add household income
    ws = [4, 5, 6]
    dfs = []

    for wave in ws:
        file_path = f"/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew{wave}_rel8-0-0_ALL_datasets_stata/sharew{wave}_rel8-0-0_gv_imputations.dta"
        data = pd.read_stata(file_path, convert_categoricals=False)
        data["wave"] = wave
        data = data.rename(columns={f"hhid{wave}": "hhid"})
        data = data.groupby(["hhid", "wave"])[["thinc", "thinc2"]].max().reset_index()
        dfs.append(data)

    data = pd.concat(dfs, axis=0, ignore_index=True)
    data["thinc"] = np.where(data["thinc"] < 0, data["thinc2"], data["thinc"])

    df = df.merge(data, on=["hhid", "wave"], how="left")

    # Add investments and life insurance
    df[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]] = (
        df[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]]
        .replace({"Yes": 1, "No": 0, "Refusal": 0, "Don't know": 0})
        .fillna(0)
        .astype("int")
    )

    inv = (
        df.groupby(["hhid", "year"])[
            ["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]
        ]
        .max()
        .reset_index()
    )
    inv["investment"] = (
        (inv[["as062_", "as063_", "as064_", "as065_", "as066_"]] == 1)
        .any(axis=1)
        .astype(int)
    )
    inv = inv.rename(columns={"as067_": "life_insurance"})

    df = df.merge(
        inv[["hhid", "year", "investment", "life_insurance"]],
        on=["hhid", "year"],
        how="left",
    )

    return df


def health(df):
    """
    Add health-related information to the DataFrame, including overall physical health indexes,
    number of chronic diseases, and Euro-D scale scores for mental health.
    Additionaly, a PCA is done on Euro-D data to obtain separate factors for motivation lack and affective suffering.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing information about individuals.

    Returns:
    - pd.DataFrame: The DataFrame with added columns representing health-related information.
    """
    # Add overall physical health indexes
    df["sphus"] = df["sphus"].replace(
        {"Poor": 1, "Fair": 2, "Good": 3, "Very good": 4, "Excellent": 5}
    )

    df["sphus"] = df["sphus"].replace(["Don't know", "Refusal"], np.nan)
    df = df.dropna(subset="sphus").reset_index(drop=True)

    df["sphus2"] = df["sphus2"].replace(
        {"Less than very good": 0, "Very good/excellent": 1}
    )
    # Add number of chronic diseases
    df["chronic"] = (
        df["chronicw4"].combine_first(df["chronicw5"]).combine_first(df["chronicw6c"])
    )
    df["chronic2"] = (
        df["chronic2w4"].combine_first(df["chronic2w5"]).combine_first(df["chronic2w6"])
    )

    df["chronic"] = df["chronic"].replace(["Don't know", "Refusal"], np.nan)
    df = df.dropna(subset="chronic").reset_index(drop=True)

    df["chronic2"] = df["chronic2"].replace(
        {"Less than 2 diseases": 0, "2+ chronic diseases": 1}
    )
    # Add Euro-D scale score for mental health
    df = df.dropna(subset=["eurod"]).reset_index(drop=True)
    # Transform to numeric
    df["eurod"] = df["eurod"].replace({"Not depressed": 0, "Very depressed": 12})
    df["eurodcat"] = df["eurodcat"].replace({"Yes": 1, "No": 0})
    df[
        [
            "euro1",
            "euro2",
            "euro3",
            "euro4",
            "euro5",
            "euro6",
            "euro7",
            "euro8",
            "euro9",
            "euro10",
            "euro11",
            "euro12",
        ]
    ] = df[
        [
            "euro1",
            "euro2",
            "euro3",
            "euro4",
            "euro5",
            "euro6",
            "euro7",
            "euro8",
            "euro9",
            "euro10",
            "euro11",
            "euro12",
        ]
    ].applymap(
        lambda x: 1 if x == "Selected" else 0
    )
    # Add PCA for affective suffering and motivation luck
    columns_for_pca = [
        "euro1",
        "euro2",
        "euro3",
        "euro4",
        "euro5",
        "euro6",
        "euro7",
        "euro8",
        "euro9",
        "euro10",
        "euro11",
        "euro12",
    ]
    data_pca = df[columns_for_pca]

    corr_mat = np.corrcoef(data_pca, rowvar=False)  # Tetrachoric correlation matrix

    evals, evecs = eigh(corr_mat)  # Eigenvalues and eigenvectors

    fa = FactorAnalyzer(n_factors=2, rotation="varimax", method="ml")
    fa.fit(data_pca)

    factor_scores = fa.transform(data_pca)

    cutoff = 0.55

    df["affective_suffering"] = 0
    df["motivation_lack"] = 0

    df["affective_suffering"] = (factor_scores[:, 0] >= cutoff).astype(int)
    df["motivation_lack"] = (factor_scores[:, 1] >= cutoff).astype(int)

    return df


def share_preprocessing(df, data_with_isco):
    """
    Perform preprocessing on SHARE survey data, integrating information from multiple sources.

    Parameters:
    - df (pd.DataFrame): The main SHARE survey DataFrame containing individual information.
    - data_with_isco (pd.DataFrame): DataFrame containing ISCO codes for individuals.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with integrated information.

    Note:
    - The function first filters out individuals without ISCO codes.
    - It adds the 'year' column based on the 'wave'.
    - Current age is calculated using the 'calculate_age' function.
    - Number of children and grandchildren is calculated using the 'number_of_children' function.
    - Employment status is filtered to include only employed individuals.
    - Individuals eligible for disability or special state pensions are excluded.
    - 'job_status' and 'industry' information is added using the 'industry' function.
    - Financial information including household income, investments, and life insurance is added using the 'finance' function.
    - Physical and mental health indicators are added using the 'health' function.
    - The final DataFrame is selected with relevant columns.

    """
    # Leave only also those with isco codes
    unique_mergeid_share = set(df["mergeid"].unique())
    unique_mergeid_isco = set(data_with_isco["mergeid"].unique())
    intersection_ids = unique_mergeid_share.intersection(unique_mergeid_isco)
    df = df[df["mergeid"].isin(intersection_ids)].reset_index(drop=True)

    print("Those without ISCO codes - deleted")

    # Add year
    wave_to_year = {4: 2011, 5: 2013, 6: 2015}
    df["year"] = df["wave"].map(wave_to_year).astype(int)

    # Calculate current age
    df["age"] = df.apply(calculate_age, axis=1)

    # Calculate number of children and grandchildren
    df = number_of_children(df)

    # Indicate if lives with a partner
    df["partnerinhh"] = df["partnerinhh"].replace({"Yes": 1, "No": 0})

    print("Current year, age, number of children and living with a partner - imputed")
    # Leave only employed
    df = df[
        df.ep005_ == "Employed or self-employed (including working for family business)"
    ].reset_index(drop=True)

    # Delete those eligible to disability or other special state pensions
    # df = df[(df.ep071dno == "Selected") | (df.ep671dno == "Selected")].reset_index(
    #    drop=True
    # )

    # print("Currently not working and eligible to special pensions - deleted")
    # Add job status
    df["ep009_"] = (
        df["ep009_"]
        .replace({"Don't know": "Employee", "Refusal": "Employee"})
        .fillna("Employee")
    )
    df = df.rename(columns={"ep009_": "job_status"})

    # Add industry of employment
    df = industry(df)

    print("Job status, industry of employment - added")

    # Add household income, investments, life insurance
    df = finance(df)

    print("Household income, investments, life insurance - added")

    # Add physical and mental health indicators
    df = health(df)

    print("Physical and mental health indicators - added")

    # Choose columns
    df = df[
        [
            "mergeid",
            "hhid",
            "wave",
            "year",
            "age",
            "nb_children",
            "nb_grandchildren",
            "partnerinhh",
            "job_status",
            "industry",
            "thinc",
            "thinc2",
            "investment",
            "life_insurance",
            "sphus",
            "sphus2",
            "chronic",
            "chronic2",
            "eurod",
            "eurodcat",
            "affective_suffering",
            "motivation_lack",
        ]
    ]
    return df
