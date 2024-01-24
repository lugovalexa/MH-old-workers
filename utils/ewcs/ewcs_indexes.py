import pandas as pd


def social_environment_index(df, df2010):
    """
    Calculate and create the Social Environment Index on EWCS data to reproduce the original one (as it is only given for 2015).
    The number of metrics included in the index is limited to those present both in 2015 and 2010.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing survey responses for the year 2015.
    - df2010 (pd.DataFrame): The DataFrame containing survey responses for the year 2010.

    Returns:
    pd.DataFrame: A DataFrame with columns 'id', 'jqi_social_environment', and 'year' representing
                  individual IDs, calculated Social Environment Index, and the respective survey year.
    """
    # Calculate index for 2010
    # Choose columns
    soc10 = df2010[
        [
            "id",
            "q70a",
            "q70b",
            "q70c",
            "q71a",
            "q71c",
            "q71b",
            "q58b",
            "q58a",
            "q51a",
            "q51b",
        ]
    ]

    # Drop missing values
    soc10 = soc10.dropna().reset_index(drop=True)
    for col in soc10.columns:
        if col != "id":
            soc10[col] = soc10[col].astype("int")
            soc10 = soc10[soc10[col] < 7].reset_index(drop=True)

    # Transform some questions
    soc10[["q58a", "q58b"]] = soc10[["q58a", "q58b"]].replace({1: 2, 2: 1})
    soc10[["q51a", "q51b"]] = soc10[["q51a", "q51b"]].replace({1: 5, 2: 4, 4: 2, 5: 1})

    # Calculate index
    soc10["jqi_social_environment"] = (
        soc10["q58a"]
        + soc10["q58b"]
        + soc10["q51a"]
        + soc10["q51b"]
        + soc10["q70a"]
        + soc10["q70b"]
        + soc10["q70c"]
        + soc10["q71a"]
        + soc10["q71b"]
        + soc10["q71c"]
    )

    # Re-scale to 0-100
    old_min = 10
    old_max = 26
    new_min = 0
    new_max = 100

    soc10["jqi_social_environment"] = (
        (soc10["jqi_social_environment"] - old_min) / (old_max - old_min)
    ) * (new_max - new_min) + new_min

    soc10 = soc10[["id", "jqi_social_environment"]]
    soc10["year"] = 2010

    # The same for 2015
    soc15 = df[
        [
            "id",
            "y15_Q80a",
            "y15_Q80b",
            "y15_Q80c",
            "y15_Q81a",
            "y15_Q81b",
            "y15_Q81c",
            "y15_Q63a",
            "y15_Q63e",
            "y15_Q61a",
            "y15_Q61b",
        ]
    ]
    soc15 = soc15.dropna().reset_index(drop=True)
    for col in soc15.columns:
        if col != "id":
            soc15[col] = soc15[col].astype("int")
            soc15 = soc15[soc15[col] < 7].reset_index(drop=True)
    soc15[["y15_Q61a", "y15_Q61b", "y15_Q63a", "y15_Q63e"]] = soc15[
        ["y15_Q61a", "y15_Q61b", "y15_Q63a", "y15_Q63e"]
    ].replace({1: 5, 2: 4, 4: 2, 5: 1})

    soc15["jqi_social_environment"] = (
        soc15["y15_Q80a"]
        + soc15["y15_Q80b"]
        + soc15["y15_Q80c"]
        + soc15["y15_Q81a"]
        + soc15["y15_Q81b"]
        + soc15["y15_Q81c"]
        + soc15["y15_Q63a"]
        + soc15["y15_Q63e"]
        + soc15["y15_Q61a"]
        + soc15["y15_Q61b"]
    )

    old_min = 10
    old_max = 32
    new_min = 0
    new_max = 100

    soc15["jqi_social_environment"] = (
        (soc15["jqi_social_environment"] - old_min) / (old_max - old_min)
    ) * (new_max - new_min) + new_min

    soc15 = soc15[["id", "jqi_social_environment"]]
    soc15["year"] = 2015

    # Concatenate both datasets
    soc = pd.concat([soc10, soc15], axis=0).reset_index(drop=True)

    # Merge with the main dataframe
    soc["id"] = soc["id"].astype(str)
    soc["id"] = soc["id"].astype(str).apply(lambda x: x[:-2] if x.endswith(".0") else x)
    soc["id"] = soc["id"].str.replace(r"[^ -~]+", "", regex=True)

    print("JQI social environment")
    print(soc.groupby("year").jqi_social_environment.describe())

    return soc


def prospects_index(df, df2010):
    """
    Calculate and create the Prospects Index on EWCS data to reproduce the original one (as it is not represented in its fullest version).
    The number of metrics included in the index is limited to those present both in 2015 and 2010.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing survey responses for the year 2015.
    - df2010 (pd.DataFrame): The DataFrame containing survey responses for the year 2010.

    Returns:
    pd.DataFrame: A DataFrame with columns 'id', 'jqi_prospects', and 'year' representing
                  individual IDs, calculated Prospects Index, and the respective survey year.
    """
    # Calculate index for 2010
    # Choose columns
    pro10 = df2010[["id", "q77c", "q77a"]]

    # Drop missing values
    pro10 = pro10.dropna().reset_index(drop=True)
    for col in pro10.columns:
        if col != "id":
            pro10[col] = pro10[col].astype("int")
            pro10 = pro10[pro10[col] < 7].reset_index(drop=True)
    # Transform some questions
    pro10["q77a"] = pro10["q77a"].replace({1: 5, 2: 4, 4: 2, 5: 1})

    # Calculate index
    pro10["jqi_prospects"] = pro10["q77c"] + pro10["q77a"]

    # Re-scale to 0-100
    old_min = 2
    old_max = 10
    new_min = 0
    new_max = 100

    pro10["jqi_prospects"] = (
        (pro10["jqi_prospects"] - old_min) / (old_max - old_min)
    ) * (new_max - new_min) + new_min

    pro10 = pro10[["id", "jqi_prospects"]]
    pro10["year"] = 2010

    # The same for 2015
    pro15 = df[["id", "y15_Q89b", "y15_Q89g"]]
    pro15 = pro15.dropna().reset_index(drop=True)
    for col in pro15.columns:
        if col != "id":
            pro15[col] = pro15[col].astype("int")
            pro15 = pro15[pro15[col] < 7].reset_index(drop=True)
    pro15["y15_Q89b"] = pro15["y15_Q89b"].replace({1: 5, 2: 4, 4: 2, 5: 1})

    pro15["jqi_prospects"] = pro15["y15_Q89g"] + pro15["y15_Q89b"]

    old_min = 2
    old_max = 10
    new_min = 0
    new_max = 100

    pro15["jqi_prospects"] = (
        (pro15["jqi_prospects"] - old_min) / (old_max - old_min)
    ) * (new_max - new_min) + new_min

    pro15 = pro15[["id", "jqi_prospects"]]
    pro15["year"] = 2015

    # Merge two datasets
    pro = pd.concat([pro10, pro15], axis=0).reset_index(drop=True)

    # Format id column
    pro["id"] = pro["id"].astype(str)
    pro["id"] = pro["id"].astype(str).apply(lambda x: x[:-2] if x.endswith(".0") else x)
    pro["id"] = pro["id"].str.replace(r"[^ -~]+", "", regex=True)

    print("JQI prospects")
    print(pro.groupby("year").jqi_prospects.describe())

    return pro


def intensity_index(df, df2010):
    """
    Calculate and create the Intensity Index on EWCS data to reproduce the original one (as it is only given for 2015).
    The number of metrics included in the index is limited to those present both in 2015 and 2010.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing survey responses for the year 2015.
    - df2010 (pd.DataFrame): The DataFrame containing survey responses for the year 2010.

    Returns:
    pd.DataFrame: A DataFrame with columns 'id', 'jqi_intensity', and 'year' representing
                  individual IDs, calculated Intensity Index, and the respective survey year.
    """
    # Calculate index for 2010
    # Choose columns
    int10 = df2010[
        [
            "id",
            "q45a",
            "q45b",
            "q51g",
            "q46a",
            "q46b",
            "q46c",
            "q46d",
            "q46e",
            "q51p",
            "q24g",
            "q47",
            "q48",
        ]
    ]

    # Drop missing values
    int10 = int10.dropna().reset_index(drop=True)
    for col in int10.columns:
        if col != "id" and col != "q46e":
            int10[col] = int10[col].astype("int")
            int10 = int10[int10[col] < 8].reset_index(drop=True)
        elif col == "q46e":
            int10[col] = int10[col].astype("int")
            int10 = int10[int10[col] < 7].reset_index(drop=True)

    # Transform some questions
    int10["q4748"] = int10["q47"] * int10["q48"]

    int10["q46"] = 2
    for i in range(len(int10)):
        count = 0
        for col in ["q46a", "q46b", "q46c", "q46d", "q46e"]:
            if int10[col][i] == 1:
                count += 1
        if count >= 3:
            int10["q46"][i] = 1

    int10["q51g"] = int10["q51g"].replace({1: 5, 2: 4, 4: 2, 5: 1})

    # Calculate index
    int10["jqi_intensity"] = (
        int10["q45a"]
        + int10["q45b"]
        + int10["q51g"]
        + int10["q46a"]
        + int10["q46b"]
        + int10["q46c"]
        + int10["q46d"]
        + int10["q46e"]
        + int10["q46"]
        + int10["q51p"]
        + int10["q24g"]
        + int10["q4748"]
    )

    # Re-scale to 0-100
    old_min = 11
    old_max = 54
    new_min = 0
    new_max = 100

    int10["jqi_intensity"] = (
        (int10["jqi_intensity"] - old_min) / (old_max - old_min)
    ) * (new_max - new_min) + new_min

    int10 = int10[["id", "jqi_intensity"]]
    int10["year"] = 2010

    # The same for 2015
    int15 = df[
        [
            "id",
            "y15_Q49a",
            "y15_Q49b",
            "y15_Q61g",
            "y15_Q50a",
            "y15_Q50b",
            "y15_Q50c",
            "y15_Q50d",
            "y15_Q50e",
            "y15_Q61o",
            "y15_Q30g",
            "y15_Q51",
            "y15_Q52",
        ]
    ]
    int15 = int15.dropna().reset_index(drop=True)
    for col in int15.columns:
        if col != "id":
            int15[col] = int15[col].astype("int")
            int15 = int15[int15[col] < 7].reset_index(drop=True)

    int15["y15_Q5152"] = int15["y15_Q51"] * int15["y15_Q52"]

    int15["y15_Q50"] = 0
    for i in range(len(int15)):
        count = 0
        for col in ["y15_Q50a", "y15_Q50b", "y15_Q50c", "y15_Q50d", "y15_Q50e"]:
            if int15[col][i] == 1:
                count += 1
        if count >= 3:
            int15["y15_Q50"][i] = 1

    int15["y15_Q61g"] = int15["y15_Q61g"].replace({1: 5, 2: 4, 4: 2, 5: 1})

    int15["jqi_intensity"] = (
        int15["y15_Q49a"]
        + int15["y15_Q49b"]
        + int15["y15_Q61g"]
        + int15["y15_Q50a"]
        + int15["y15_Q50b"]
        + int15["y15_Q50c"]
        + int15["y15_Q50d"]
        + int15["y15_Q50e"]
        + int15["y15_Q50"]
        + int15["y15_Q61o"]
        + int15["y15_Q30g"]
        + int15["y15_Q5152"]
    )

    old_min = 11
    old_max = 54
    new_min = 0
    new_max = 100

    int15["jqi_intensity"] = (
        (int15["jqi_intensity"] - old_min) / (old_max - old_min)
    ) * (new_max - new_min) + new_min

    int15 = int15[["id", "jqi_intensity"]]
    int15["year"] = 2015

    # Merge two datasets
    int = pd.concat([int10, int15], axis=0).reset_index(drop=True)

    # Format id column
    int["id"] = int["id"].astype(str)
    int["id"] = int["id"].astype(str).apply(lambda x: x[:-2] if x.endswith(".0") else x)
    int["id"] = int["id"].str.replace(r"[^ -~]+", "", regex=True)

    print("JQI intensity")
    print(int.groupby("year").jqi_intensity.describe())

    return int


def sum_wq_index(df):
    """
    Calculate and create a Overall Work Quality Index as a sum of all EWCS indexes except monthly earnings.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing different EWCS indexes.

    Returns:
    pd.DataFrame: A DataFrame with added columns 'jqi_sum' and 'jqi_sum_weighted' representing
                  the overall work quality index and the weighted overall work quality index, respectively.
    """
    # Calculate the overall work quality index
    df["jqi_sum"] = (
        +df["jqi_skills_discretion"]
        + df["jqi_social_environment"]
        + df["jqi_physical_environment"]
        + df["jqi_intensity"]
        + df["jqi_prospects"]
        + df["jqi_working_time_quality"]
    )

    # Calculate the weighted version
    df["jqi_sum_pure"] = (
        +df["jqi_skills_discretion_pure"]
        + df["jqi_social_environment_pure"]
        + df["jqi_physical_environment_pure"]
        + df["jqi_intensity_pure"]
        + df["jqi_prospects_pure"]
        + df["jqi_working_time_quality_pure"]
    )

    print("JQI working quality index pure (no weights applied)")
    print(df.groupby("year").jqi_sum_pure.describe())

    return df
