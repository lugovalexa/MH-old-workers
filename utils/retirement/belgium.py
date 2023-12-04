def belgium_age(row):
    # Male
    if row["gender"] == "Male":
        return 65

    # Female
    else:
        # Wave 1
        if row["wave"] == 1:
            return 63
        # Wave 2
        elif row["wave"] == 2:
            return 64
        # Waves 4-8
        else:
            return 65


def belgium_change(row):
    # Female
    if row["gender"] == "Female":
        if row["wave"] == 2 or row["wave"] == 4:
            return 1
        else:
            return 0


def belgium_change1(row):
    return 0
