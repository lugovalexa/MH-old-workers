import matplotlib.pyplot as plt
import pandas as pd


def describe_data(df):
    """
    Summarizes and visualizes various aspects of the input DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data to be described.

    This function performs the following tasks:

    1. **ID Analysis:**
        - Number of unique IDs.
        - Number of unique IDs by country.
        - Number of unique IDs by year.

    2. **Demographics:**
        - Displays descriptive statistics for age, gender, number of children, and years of education.

    3. **Demographics Plotting:**
        - Histograms for age, gender, number of children, and years of education.

    4. **Job Status and Industry:**
        - Displays the distribution of job statuses.
        - Displays the distribution of industries of employment.

    5. **Income, Investment, and Insurance:**
        - Displays descriptive statistics for total income, investment, and life insurance.

    6. **Employment Details:**
        - Displays descriptive statistics for years of contribution, retirement age, work horizon, and work horizon change.

    7. **Employment Details Plotting:**
        - Histograms for years of contribution, retirement age, work horizon, and work horizon change.

    8. **Physical Health and Chronic Diseases:**
        - Displays the distribution of physical health status and chronic diseases.

    9. **Mental Health:**
        - Displays the distribution of EuroD category.
        - Displays EuroD scale score histogram.

    10. **Working Conditions:**
        - Displays descriptive statistics for various working conditions.

    """

    # Number of unique IDs
    print("Number of unique IDs:", df["mergeid"].nunique())
    print("Number of unique IDs by country:")
    print(df.groupby("country")["mergeid"].nunique())
    print("Number of unique IDs by year:")
    print(df.groupby("year")["mergeid"].nunique())

    # Demographics
    print("\nDemographics:")
    print(round(df[["age", "gender", "nb_children", "yrseducation"]].describe(), 2))

    # Plotting demographics
    fig, axs = plt.subplots(2, 2, figsize=(7, 5))

    axs[0, 0].hist(df["age"], bins=30, color="skyblue", alpha=0.7)
    axs[0, 0].set_title("Age")

    axs[0, 1].hist(df["gender"], bins=30, color="salmon", alpha=0.7)
    axs[0, 1].set_title("Gender")

    axs[1, 0].hist(df["nb_children"], bins=30, color="lightgreen", alpha=0.7)
    axs[1, 0].set_title("Number of children")

    axs[1, 1].hist(df["yrseducation"], bins=30, color="gold", alpha=0.7)
    axs[1, 1].set_title("Years of education")

    plt.tight_layout()
    plt.show()

    # Job status and industry of employment
    print("\nJob Status:")
    print(round(df["job_status"].value_counts(normalize=True), 2))
    print("\nIndustry of Employment:")
    print(round(df["industry"].value_counts(normalize=True), 2))

    # Income and investment
    print("\nIncome, investment and insurance:")
    print(round(df[["thinc", "investment", "life_insurance"]].describe(), 2))

    # Employment details
    print("\nEmployment:")
    print(
        round(
            df[
                [
                    "yrscontribution",
                    "retirement_age",
                    "work_horizon",
                    "work_horizon_change",
                ]
            ].describe(),
            2,
        )
    )

    # Plotting employment details
    fig, axs = plt.subplots(2, 2, figsize=(7, 5))

    axs[0, 0].hist(df["yrscontribution"], bins=30, color="skyblue", alpha=0.7)
    axs[0, 0].set_title("Years of contribution")

    axs[0, 1].hist(df["retirement_age"], bins=30, color="salmon", alpha=0.7)
    axs[0, 1].set_title("Retirement age")

    axs[1, 0].hist(df["work_horizon"], bins=30, color="lightgreen", alpha=0.7)
    axs[1, 0].set_title("Work horizon, years")

    axs[1, 1].hist(df["work_horizon_change"], bins=30, color="gold", alpha=0.7)
    axs[1, 1].set_title("Work horizon change by reform")

    plt.tight_layout()
    plt.show()

    # Physical health and chronic diseases
    print("\nPhysical Health and Chronic Diseases:")
    print(round(df[["sphus2", "chronic2"]].value_counts(normalize=True), 2))

    # Mental health
    print("\nMental Health:")
    print(round(df["eurodcat"].value_counts(normalize=True), 2))
    print("EuroD scale score:")
    print(df["eurod"].value_counts())

    # Plotting EuroD scale score
    plt.figure(figsize=(6, 4))
    plt.hist(df["eurod"], bins=13, color="skyblue", alpha=0.7)
    plt.title("EuroD scale score")
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    # Working conditions
    print("\nWorking Conditions:")
    print(
        round(
            df[
                [
                    "jqi_monthly_earnings",
                    "jqi_skills_discretion",
                    "jqi_social_environment",
                    "jqi_physical_environment",
                    "jqi_intensity",
                    "jqi_prospects",
                    "jqi_working_time_quality",
                    "jqi_sum",
                ]
            ].describe(),
            2,
        )
    )
