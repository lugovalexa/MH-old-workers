def denmark_age(row):
    # Waves 1-7
    if row["wave"] < 8:
        if (row["yrbirth"] == 1932 and row["mobirth"] < 7) or (row["yrbirth"] < 1932):
            return 67
        else:
            return 65
    # Wave 8
    else:
        return 66


def denmark_change(row):
    if row["wave"] == 8:
        if (row["yrbirth"] == 1932 and row["mobirth"] > 7) or (row["yrbirth"] > 1932):
            return 1
        else:
            return 0
    else:
        return 0


def denmark_change1(row):
    if row["wave"] == 8:
        if (row["yrbirth"] == 1932 and row["mobirth"] > 7) or (row["yrbirth"] > 1932):
            return 1
        else:
            return 0
    else:
        return 0
