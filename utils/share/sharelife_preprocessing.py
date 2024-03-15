import pandas as pd
from pandas.io.stata import StataReader


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


def find_column_highest_before_2011(row):
    """
    Retrieve the index for the last available isco before or in 2011.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of data.

    Returns:
    - pd.Series or pd.NA: The last valid value in the row, or pd.NA if no valid value is found.
    """
    start_columns = [f"re011_{i}" for i in range(1, 21)]
    valid_values = [
        row[column]
        for column in start_columns
        if pd.notna(row[column]) and row[column] <= 2011
    ]
    if not valid_values:
        return pd.NA
    max_value = max(valid_values)
    column_name = [column for column in start_columns if row[column] == max_value][0]
    return column_name.split("_")[-1]


def find_column_highest_before_2013(row):
    """
    Retrieve the index for the last available isco before or in 2013.

    Parameters:
    - row (pd.Series): A Pandas Series representing a row of data.

    Returns:
    - pd.Series or pd.NA: The last valid value in the row, or pd.NA if no valid value is found.
    """
    start_columns = [f"re011_{i}" for i in range(1, 21)]
    valid_values = [
        row[column]
        for column in start_columns
        if pd.notna(row[column]) and row[column] <= 2013
    ]
    if not valid_values:
        return pd.NA
    max_value = max(valid_values)
    column_name = [column for column in start_columns if row[column] == max_value][0]
    return column_name.split("_")[-1]


def sharelife_gender_country_age(df):
    """
    Perform data preprocessing for Sharelife data, focusing on gender, country, and age-related information.

    Parameters:
    - df (pd.DataFrame): The Sharelife DataFrame containing individual information.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with formatted gender, country, and age-related data.

    Note:
    - The function reads country labels from the SHARE dataset and replaces country numbers with country names.
    - It fills gaps in the 'yr1country' column with birth year when not available and renames the column accordingly.
    - Gender is transformed to 1 for female and 0 for male.
    - The DataFrame is filtered to include individuals aged 50 and above as of the year 2011.
    - Gaps in the 'mobirth' column are filled with 1.
    """
    # Replace country numbers with names
    with StataReader(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew7_rel8-0-0_ALL_datasets_stata/sharew7_rel8-0-0_cv_r.dta",
        convert_categoricals=True,
    ) as reader:
        data = reader.read()
        value_labels = reader.value_labels()
    df["country"] = df["country"].replace(value_labels.get("country"))

    # 1st year in country
    df["dn006_"] = df["dn006_"].fillna(df["yrbirth"])
    df.loc[df["dn006_"] < 0, "dn006_"] = df.loc[df["dn006_"] < 0, "yrbirth"]
    df = df.rename(columns={"dn006_": "yr1country"})

    # Transform gender to 1 for female and 0 for male
    df["gender"] = df["gender"].replace({1: 0, 2: 1})

    # Filter for aged 50 and above as for 2011
    df = df[df.age2017 >= 56].reset_index(drop=True)

    # Fill gaps in month of birth with 1 (not very important)
    df["mobirth"] = df["mobirth"].fillna(1)

    print("Gender, country, 1st year in country - formatted, age 50+ filter - applied")

    return df


def sharelife_add_gender_country_age(df):
    """
    Perform data preprocessing for additional data coming from main SHARE datasets, focusing on gender, country, and age-related information.

    Parameters:
    - df (pd.DataFrame): The DataFrame coming from SHARE main datasets containing individual information.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with formatted gender, country, and age-related data.

    Note:
    - It fills gaps in the 'yr1country' column with birth year when not available and renames the column accordingly.
    - Gender is transformed to 1 for female and 0 for male.
    - The DataFrame is filtered to include individuals aged 50 and above as of the year 2011.
    -  'mobirth' column is tranformed to numeric, gaps are filled with 1.
    """
    # 1st year in country
    df = df.dropna(subset="yrbirth").reset_index(drop=True)
    df["dn006_"] = df["dn006_"].fillna(df["yrbirth"])
    df.loc[(df.dn006_ == "Refusal") | (df.dn006_ == "Don't know"), "dn006_"] = df.loc[
        (df.dn006_ == "Refusal") | (df.dn006_ == "Don't know"), "yrbirth"
    ]
    df = df.rename(columns={"dn006_": "yr1country"})
    df["yr1country"] = df["yr1country"].astype("int")

    # Transform gender to 1 for female and 0 for male
    df["gender"] = df["gender"].replace({"Male": 0, "Female": 1})

    # Filter for aged 50 and above as for 2011
    df = df[(df.age2015 >= 54) | (df.age2017 >= 56) | (df.age2020 >= 59)].reset_index(
        drop=True
    )

    # Fill gaps in month of birth with 1 (not very important)
    month_to_numeric = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    df["mobirth"] = df["mobirth"].map(month_to_numeric)
    df["mobirth"] = df["mobirth"].fillna(1)

    print("Gender, country, 1st year in country - formatted, age 50+ filter - applied")

    return df


def calculate_education_years(waves):
    """
    Calculate the total years of education based on SHARE survey data.

    Parameters:
    - waves (list): List of wave numbers for which education data is available.

    Returns:
    - pd.DataFrame: DataFrame containing the total years of education for each individual.

    Note:
    - The function reads education data from SHARE wave datasets part "dn".
    - It calculates the total years of education ('yrseducation') for each individual.
    - The resulting DataFrame is filtered to include values of years of education between 0 and 40 years.
    - The function returns a DataFrame with 'mergeid' and 'yrseducation' columns.

    """
    dfs = []
    for wave in waves:
        file_path = f"/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew{wave}_rel8-0-0_ALL_datasets_stata/sharew{wave}_rel8-0-0_dn.dta"
        data = pd.read_stata(file_path, convert_categoricals=False)
        dfs.append(data)

    dn_data = pd.concat(dfs, axis=0, ignore_index=True)

    mean_edu = dn_data[(dn_data.dn041_ >= 0) | (dn_data.dn041_ <= 40)]["dn041_"].mean()
    dn_data.loc[(dn_data.dn041_ < 0) | (dn_data.dn041_ > 40), "dn041_"] = mean_edu

    edu_sum = dn_data.groupby("mergeid").dn041_.sum().to_frame().reset_index()

    edu_sum = edu_sum.rename(columns={"dn041_": "yrseducation"})

    print("Years of education - calculated")

    return edu_sum


def sharelife_job(df):
    """
    Perform data preprocessing for job-related information in Sharelife data.

    Parameters:
    - df (pd.DataFrame): The Sharelife DataFrame containing individual information.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with identified current job ISCO codes.

    Note:
    - The function identifies the current job ISCO code for each individual based on available columns.
    - Individuals with missing or non-positive ISCO codes are dropped from the DataFrame.
    - Some ISCO codes are corrected by appending a missing '0' at the end for specific cases.
    - The resulting DataFrame includes columns such as 'mergeid', 'isco', and 'job_start'.

    """
    # Identify current job start
    start_columns = [f"re011_{i}" for i in range(1, 21)]
    df["job_start"] = df[start_columns].apply(get_last_valid, axis=1)

    # Identify isco if the last job started before or in 2011
    isco_columns = [f"re012isco_{i}" for i in range(1, 21)]
    df_lastbefore2011 = df[df["job_start"] <= 2011].reset_index(drop=True)
    df_lastbefore2011["isco2011"] = df_lastbefore2011[isco_columns].apply(
        get_last_valid, axis=1
    )
    df_lastbefore2011["isco2013"] = df_lastbefore2011[isco_columns].apply(
        get_last_valid, axis=1
    )
    df_lastbefore2011["isco2015"] = df_lastbefore2011[isco_columns].apply(
        get_last_valid, axis=1
    )

    # Identify isco if the last job started after 2011 and before or in 2013
    df_lastafter2011 = df[
        (df["job_start"] > 2011) & (df["job_start"] <= 2013)
    ].reset_index(drop=True)
    df_lastafter2011["isco2015"] = df_lastafter2011[isco_columns].apply(
        get_last_valid, axis=1
    )
    df_lastafter2011["isco2013"] = df_lastafter2011[isco_columns].apply(
        get_last_valid, axis=1
    )
    df_lastafter2011["index_before2011"] = df_lastafter2011[start_columns].apply(
        find_column_highest_before_2011, axis=1
    )
    df_lastafter2011 = df_lastafter2011.dropna(subset="index_before2011").reset_index(
        drop=True
    )
    df_lastafter2011["isco2011"] = pd.NA
    for i in range(len(df_lastafter2011)):
        index_before2011 = df_lastafter2011["index_before2011"][i]
        df_lastafter2011["isco2011"][i] = df_lastafter2011[
            f"re012isco_{index_before2011}"
        ][i]

    # Identify isco if the last job started after 2013 and before or in 2015
    df_lastafter2013 = df[
        (df["job_start"] > 2013) & (df["job_start"] <= 2015)
    ].reset_index(drop=True)
    df_lastafter2013["isco2015"] = df_lastafter2013[isco_columns].apply(
        get_last_valid, axis=1
    )

    df_lastafter2013["index_before2013"] = df_lastafter2013[start_columns].apply(
        find_column_highest_before_2013, axis=1
    )
    df_lastafter2013 = df_lastafter2013.dropna(subset="index_before2013").reset_index(
        drop=True
    )
    df_lastafter2013["isco2013"] = pd.NA
    for i in range(len(df_lastafter2013)):
        index_before2013 = df_lastafter2013["index_before2013"][i]
        df_lastafter2013["isco2013"][i] = df_lastafter2013[
            f"re012isco_{index_before2013}"
        ][i]

    df_lastafter2013["isco2011"] = df_lastafter2013["isco2013"]

    # Combine to datasets
    df = pd.concat(
        [df_lastbefore2011, df_lastafter2011, df_lastafter2013], ignore_index=True
    )

    # Drop individuals with missing values
    df = df[(df.isco2011 > 0) & (df.isco2013 > 0) & (df.isco2015 > 0)].reset_index(
        drop=True
    )
    df = df.dropna(subset=["isco2011", "isco2013", "isco2015"]).reset_index(drop=True)
    df[["isco2011", "isco2013", "isco2015"]] = df[
        ["isco2011", "isco2013", "isco2015"]
    ].astype(int)
    # Correct codes when one 0 is missing at the end
    df["isco2011"] = df["isco2011"].apply(lambda x: x * 10 if 99 < x < 1000 else x)
    df["isco2013"] = df["isco2013"].apply(lambda x: x * 10 if 99 < x < 1000 else x)
    df["isco2015"] = df["isco2015"].apply(lambda x: x * 10 if 99 < x < 1000 else x)

    print("Current ISCO - identified")

    return df


def sharelife_add_job(df):
    """
    Perform data preprocessing for job-related information in additional data from main SHARE datasets.

    Parameters:
    - df (pd.DataFrame): The SHARE DataFrame containing individual information.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with identified current job ISCO codes.

    Note:
    - The function identifies the current job ISCO code for each individual based on available columns.
    - Individuals with missing or non-positive ISCO codes are dropped from the DataFrame.
    - Some ISCO codes are corrected by appending a missing '0' at the end for specific cases.
    - Individuals who changed jobs between 2011 and 2017 are excluded from the DataFrame.
    - The resulting DataFrame includes columns such as 'mergeid', 'isco', and 'job_start'.

    """
    # Identify current job isco
    df = df.rename(columns={"ep616isco": "isco2011"})
    df["isco2011"] = df["isco2011"].astype(int)
    df["isco2013"] = df["isco2011"]
    df["isco2015"] = df["isco2011"]

    # Leave only those who did not change job between 2011 and 2015
    ws = [5, 6]
    dfs = []

    for wave in ws:
        file_path = f"/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew{wave}_rel8-0-0_ALL_datasets_stata/sharew{wave}_rel8-0-0_ep.dta"
        data = pd.read_stata(file_path, convert_categoricals=False)
        dfs.append(data)
    ep_data = pd.concat(dfs, axis=0, ignore_index=True)
    ep_data = ep_data[
        (ep_data.ep141d1 != "Selected")
        & (ep_data.ep141d2 != "Selected")
        & (ep_data.ep141d3 != "Selected")
    ].reset_index(drop=True)

    df = df[df["mergeid"].isin(ep_data["mergeid"])].reset_index(drop=True)

    print("Current ISCO - identified, those changed job - deleted")

    return df


def contribution_years(df):
    """
    Calculate years of contribution to social security from SHARE job episodes panel and filter individuals based on it.

    Parameters:
    - df (pd.DataFrame): The main DataFrame containing individual information.

    Returns:
    - pd.DataFrame: The filtered DataFrame with calculated years of contribution.

    Note:
    - The function loads job episodes panel data and identifies relevant job situations.
    - It calculates the number of years of work ('yrscontribution2017') for each individual by considering relevant job situations.
    - The year of first contribution ('yr1contribution') is also calculated.
    - The resulting DataFrame is merged with the main dataset.
    - Individuals with less than 10 years of contributions in 2015 and those who started work before the age of 10 are filtered out.
    """
    # Load job episodes panel data (from retrospective waves 3 and 7)
    jobs = pd.read_stata(
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharewX_rel8-0-0_gv_job_episodes_panel.dta"
    )

    # Calculate number of years of work for each individual
    conditions = ["Employee or self-employed", "Short term job (less than 6 months)"]
    relevant_rows = jobs[jobs["situation"].isin(conditions)]

    max_year = relevant_rows.groupby("mergeid")["year"].max().to_frame().reset_index()
    result_jobs = (
        relevant_rows.groupby("mergeid").size().reset_index(name="yrscontribution2017")
    )
    max_year = max_year.merge(result_jobs, on="mergeid", how="left")
    max_year[["yrscontribution2017", "year"]] = max_year[
        ["yrscontribution2017", "year"]
    ].astype("int")
    max_year["yrscontribution2017"] += (2017 - max_year["year"]).where(
        max_year["year"] < 2017, 0
    )
    max_year["yrscontribution2017"] -= (max_year["year"] - 2017).where(
        max_year["year"] > 2017, 0
    )

    # Calculate the year of first contribution
    first_contribution = (
        relevant_rows.groupby("mergeid")["year"]
        .min()
        .reset_index(name="yr1contribution")
    )

    # Merge with main dataset
    df = df.merge(
        max_year[["mergeid", "yrscontribution2017"]], on="mergeid", how="left"
    )
    df = df.merge(first_contribution, on="mergeid", how="left")

    # Delete those with less than 10 years of contributions in 2015
    # df = df[(df["yrscontribution2017"] >= 12)].reset_index(drop=True)

    # Delete those who started work before the age of 10
    df["yr1contribution"] = df["yr1contribution"].fillna(df["yrbirth"] + 20)
    df["yr1contribution"] = df["yr1contribution"].astype("int")

    print("Years of contribution, 1st year of contribution - calculated")
    # print("Those worked less than 10 years - deleted")

    return df


def sharelife_preprocessing(df):
    """
    Perform preprocessing for Sharelife data, including gender, country, age, education, job changes,
    and calculation of contribution years.

    Parameters:
    - df (pd.DataFrame): The main DataFrame containing Sharelife data.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with selected columns.

    Note:
    - The function filters Sharelife data based on 'mn103_' values.
    - It preprocesses gender, country, and age using 'sharelife_gender_country_age' function.
    - Education years are calculated and merged using 'calculate_education_years'.
    - Job changes are preprocessed using 'sharelife_job'.
    - Contribution years are calculated using 'contribution_years'.
    - The resulting DataFrame contains selected columns.
    """
    # Choose Sharelife part
    df = df[df.mn103_ == 1].reset_index(drop=True)

    print(f"Initial n obs: {len(df)}")

    # Preprocess gender, country, and age
    df = sharelife_gender_country_age(df)

    print(f"N obs after processing gender and age: {len(df)}")

    # Calculate education years
    waves = [1, 2, 4, 5, 6]
    edu_sum = calculate_education_years(waves)

    # Merge education data
    df = df.merge(edu_sum, on="mergeid", how="left")
    df["yrseducation"] = df["yrseducation"].fillna(df["yrseducation"].mean())

    print(f"N obs after processing education years: {len(df)}")

    # Preprocess job changes
    df = sharelife_job(df)

    print(f"N obs after isco job changes: {len(df)}")

    # Calculate year of contribution
    df = contribution_years(df)

    print(f"N obs after contribution years: {len(df)}")

    # Choose columns to keep
    df = df[
        [
            "mergeid",
            "country",
            "gender",
            "yrbirth",
            "mobirth",
            "age2017",
            "yr1country",
            "yrseducation",
            "isco2011",
            "isco2013",
            "isco2015",
            "yrscontribution2017",
            "yr1contribution",
        ]
    ]

    return df


def sharelife_add_preprocessing(df, sharelife_data):
    """
    Perform preprocessing for additional data from main SHARE datasets, including gender, country, age, education, job changes,
    and calculation of contribution years.

    Parameters:
    - df (pd.DataFrame): The main DataFrame containing SHARE data.
    - sharelife_data (pd.DataFrame): The DataFrame containing main Sharelife data after preprocessing.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame with selected columns.

    Note:
    - The function filters out individuals without isco code and those already present in main Sharelife dataset.
    - It preprocesses gender, country, and age using 'sharelife_gender_country_age' function.
    - Education years are calculated and merged using 'calculate_education_years'.
    - Job changes are preprocessed using 'sharelife_job'.
    - Contribution years are calculated using 'contribution_years'.
    - The resulting DataFrame contains selected columns.
    """
    print(f"N obs initial: {len(df)}")
    # Leave only those with isco codes
    df = df.dropna(subset="ep616isco").reset_index(drop=True)
    df = df[
        (df.ep616isco != "Don't know") & (df.ep616isco != "Not yet coded")
    ].reset_index(drop=True)

    print(f"N obs dropping missing isco: {len(df)}")

    # Leave only those not already present in Sharelife
    df = df[~df["mergeid"].isin(sharelife_data["mergeid"])].reset_index(drop=True)

    print(f"N obs after drop already present in Sharelife: {len(df)}")

    # Leave only first wave with isco code for each individual
    df = df.loc[df.groupby("mergeid")["wave"].idxmin()].reset_index(drop=True)

    # Preprocess gender, country, and age
    df = sharelife_add_gender_country_age(df)

    print(f"N obs after gender and age: {len(df)}")

    # Calculate education years
    waves = [1, 2, 4, 5, 6]
    edu_sum = calculate_education_years(waves)
    # Merge education data
    df = df.merge(edu_sum, on="mergeid", how="left")
    df["yrseducation"] = df["yrseducation"].fillna(df["yrseducation"].mean())

    print(f"N obs after education: {len(df)}")

    # Preprocess job changes
    df = sharelife_add_job(df)

    print(f"N obs after job and isco: {len(df)}")

    # Calculate year of contribution
    df = contribution_years(df)

    print(f"N obs after contribution years: {len(df)}")

    # Choose columns to keep
    df = df[
        [
            "mergeid",
            "country",
            "gender",
            "yrbirth",
            "mobirth",
            "age2015",
            "age2017",
            "age2020",
            "yr1country",
            "yrseducation",
            "isco2011",
            "isco2013",
            "isco2015",
            "yrscontribution2017",
            "yr1contribution",
        ]
    ]
    return df
