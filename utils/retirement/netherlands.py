def netherlands_age(row):
    # Waves 1-7
    if row["wave"] < 8:
        return 65
    # Wave 8
    else:
        return 66


def netherlands_change(row):
    # Wave 8
    if row["wave"] == 8:
        return 1
    else:
        return 0
