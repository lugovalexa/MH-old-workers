import pandas as pd


def ewcs_preprocessing(df, meta):
    """
    Perform preprocessing on European Working Conditions Survey data.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing EWCS survey data.
    - meta (pyreadstat._readstat_parser.metadata_container.MetadataContainer): Metadata information.

    Returns:
    pd.DataFrame: A preprocessed DataFrame with selected columns and modified values.

    The function renames specific columns to standard names related to the Job Quality Indexes.
    It maps the 'countid' column to actual country names based on the provided metadata.
    Filters the data to include only specific countries, years from 2010 onwards, and non-null ISCO_08 values.
    Modifies the 'ISCO_08' values to ensure consistent formatting.
    Renames columns and cleans the 'id' column by removing non-printable characters and leading/trailing spaces.
    """
    # Rename index columns
    df = df.rename(
        columns={
            "adincome_mth": "jqi_monthly_earnings",
            "wq": "jqi_skills_discretion",
            "envsec": "jqi_physical_environment",
            "wlb_slim": "jqi_working_time_quality",
        }
    )
    # Replace country numbers with names
    countid_mapping = meta.value_labels["COUNTID"]
    df["countid"] = df["countid"].map(countid_mapping)

    countries = [
        "Austria",
        "Belgium",
        "Czech Republic",
        "Denmark",
        "Estonia",
        "France",
        "Germany",
        "Italy",
        "Slovenia",
        "Spain",
        "Switzerland",
    ]
    df = df[df["countid"].isin(countries)].reset_index(drop=True)
    # Leave only 2010 and 2015
    df = df[df.year >= 2010].reset_index(drop=True)
    # Drop lines with missing isco codes
    df = df.dropna(subset="ISCO_08").reset_index(drop=True)

    # Modify some isco values with erroneous format
    def modify_isco(value):
        if len(str(value)) == 1:
            return value * 1000
        elif len(str(value)) == 2:
            return value * 100
        elif len(str(value)) == 3:
            return value * 10
        else:
            return value

    df["ISCO_08"] = df["ISCO_08"].apply(modify_isco)
    # Rename some columns
    df = df.rename(columns={"countid": "country", "ISCO_08": "isco"})
    # Format id column
    df["id"] = df["id"].astype(str)
    df["id"] = df["id"].str.replace(r"[^ -~]+", "", regex=True)
    df["id"] = df["id"].str.strip()

    return df
