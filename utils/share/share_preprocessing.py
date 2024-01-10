import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer
from scipy.linalg import eigh


def calculate_age(row):
    if not pd.isnull(row["age2011"]):
        return row["age2011"] + (row["year"] - 2011)
    elif not pd.isnull(row["age2013"]):
        return row["age2013"] - (2013 - row["year"])
    elif not pd.isnull(row["age2015"]):
        return row["age2015"] - (2015 - row["year"])
    else:
        return np.nan


def number_of_children(df):
    # Calculate number of children
    df = df[(df.ch001_ != "Refusal")].reset_index(drop=True)
    df["ch001_"] = df["ch001_"].replace({"Don't know": 0})

    children2011 = (
        df[df.wave == 4]
        .groupby("hhid4")["ch001_"]
        .max()
        .to_frame(name="nb_children2011")
        .reset_index()
        .fillna(0)
    )
    children2013 = (
        df[df.wave == 5]
        .groupby("hhid5")["ch001_"]
        .max()
        .to_frame(name="nb_children2013")
        .reset_index()
        .fillna(0)
    )
    children2015 = (
        df[df.wave == 6]
        .groupby("hhid6")["ch001_"]
        .max()
        .to_frame(name="nb_children2015")
        .reset_index()
        .fillna(0)
    )

    df = df.merge(children2011, on="hhid4", how="left")
    df = df.merge(children2013, on="hhid5", how="left")
    df = df.merge(children2015, on="hhid6", how="left")

    df["nb_children"] = (
        df["nb_children2011"]
        .combine_first(df["nb_children2013"])
        .combine_first(df["nb_children2015"])
    )

    # Calculate number of grandchildren
    df = df[(df.ch021_ != "Refusal")].reset_index(drop=True)
    df["ch021_"] = df["ch021_"].replace({"Don't know": 0})

    children2011 = (
        df[df.wave == 4]
        .groupby("hhid4")["ch021_"]
        .max()
        .to_frame(name="nb_grandchildren2011")
        .reset_index()
        .fillna(0)
    )
    children2013 = (
        df[df.wave == 5]
        .groupby("hhid5")["ch001_"]
        .max()
        .to_frame(name="nb_grandchildren2013")
        .reset_index()
        .fillna(0)
    )
    children2015 = (
        df[df.wave == 6]
        .groupby("hhid6")["ch001_"]
        .max()
        .to_frame(name="nb_grandchildren2015")
        .reset_index()
        .fillna(0)
    )

    df = df.merge(children2011, on="hhid4", how="left")
    df = df.merge(children2013, on="hhid5", how="left")
    df = df.merge(children2015, on="hhid6", how="left")

    df["nb_grandchildren"] = (
        df["nb_grandchildren2011"]
        .combine_first(df["nb_grandchildren2013"])
        .combine_first(df["nb_grandchildren2015"])
    )

    return df


def industry(df):
    jobs = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharewX_rel8-0-0_gv_job_episodes_panel.dta"
    )
    conditions = ["Employee or self-employed", "Short term job (less than 6 months)"]
    ep_data = jobs[jobs["situation"].isin(conditions)].sort_values(["mergeid", "year"])
    last_industry = (
        ep_data.groupby("mergeid")["industry"]
        .apply(lambda x: x.dropna().iloc[-1] if not x.dropna().empty else np.nan)
        .reset_index()
    )
    df = df.merge(last_industry, on="mergeid", how="left")
    df["industry"] = df["industry"].replace(["Don't know", "Refusal"], np.nan)
    df = df.dropna(subset="industry").reset_index(drop=True)

    return df


def finance(df):
    # Add household income
    ws = [4, 5, 6]
    dfs = []

    for wave in ws:
        file_path = f"/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew{wave}_rel8-0-0_ALL_datasets_stata/sharew{wave}_rel8-0-0_gv_imputations.dta"
        data = pd.read_stata(file_path, convert_categoricals=False)
        data["wave"] = wave
        dfs.append(data)

    data = pd.concat(dfs, ignore_index=True)

    df = df.merge(
        data[["mergeid", "wave", "thinc", "thinc2"]], on=["mergeid", "wave"], how="left"
    )

    # Add investments and life insurance
    df[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]] = (
        df[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]]
        .replace({"Yes": 1, "No": 0, "Refusal": 0, "Don't know": 0})
        .fillna(0)
        .astype("int")
    )
    inv2011 = (
        df[df.wave == 4]
        .groupby("hhid4")[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]]
        .max()
        .reset_index()
        .rename(columns={"as067_": "life_insurance4"})
    )
    inv2013 = (
        df[df.wave == 5]
        .groupby("hhid5")[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]]
        .max()
        .reset_index()
        .rename(columns={"as067_": "life_insurance5"})
    )
    inv2015 = (
        df[df.wave == 6]
        .groupby("hhid6")[["as062_", "as063_", "as064_", "as065_", "as066_", "as067_"]]
        .max()
        .reset_index()
        .rename(columns={"as067_": "life_insurance6"})
    )

    inv2011["investment4"] = (
        (inv2011[["as062_", "as063_", "as064_", "as065_", "as066_"]] == 1)
        .any(axis=1)
        .astype(int)
    )
    inv2013["investment5"] = (
        (inv2013[["as062_", "as063_", "as064_", "as065_", "as066_"]] == 1)
        .any(axis=1)
        .astype(int)
    )
    inv2015["investment6"] = (
        (inv2015[["as062_", "as063_", "as064_", "as065_", "as066_"]] == 1)
        .any(axis=1)
        .astype(int)
    )
    df = df.merge(
        inv2011[["hhid4", "investment4", "life_insurance4"]], on="hhid4", how="left"
    )
    df = df.merge(
        inv2013[["hhid5", "investment5", "life_insurance5"]], on="hhid5", how="left"
    )
    df = df.merge(
        inv2015[["hhid6", "investment6", "life_insurance6"]], on="hhid6", how="left"
    )

    df["investment"] = (
        df["investment4"]
        .combine_first(df["investment5"])
        .combine_first(df["investment6"])
    )
    df["life_insurance"] = (
        df["life_insurance4"]
        .combine_first(df["life_insurance5"])
        .combine_first(df["life_insurance6"])
    )

    return df


def health(df):
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
    df = df[(df.ep071dno == "Selected") | (df.ep671dno == "Selected")].reset_index(
        drop=True
    )

    print("Currently not working and eligible to special pensions - deleted")

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
