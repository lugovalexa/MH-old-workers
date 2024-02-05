def switzerland_age(row):
    # Male
    if row["gender"] == "Male":
        return 65

    # Female
    else:
        return 63


def switzerland_age_early(row):
    # Male
    if row["gender"] == "Male":
        return 63

    # Female
    else:
        return 62
