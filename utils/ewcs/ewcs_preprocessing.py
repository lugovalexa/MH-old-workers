import pandas as pd


def ewcs_preprocessing(df, meta):
    df = df.rename(
        columns={
            "adincome_mth": "jqi_monthly_earnings",
            "wq": "jqi_skills_discretion",
            "envsec": "jqi_physical_environment",
            "wlb_slim": "jqi_working_time_quality",
        }
    )

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
    df = df[df.year >= 2010].reset_index(drop=True)
    df = df.dropna(subset="ISCO_08").reset_index(drop=True)

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
    df = df.rename(columns={"countid": "country", "ISCO_08": "isco"})
    df["id"] = df["id"].astype(str)
    df["id"] = df["id"].str.replace(r"[^ -~]+", "", regex=True)
    df["id"] = df["id"].str.strip()

    return df
