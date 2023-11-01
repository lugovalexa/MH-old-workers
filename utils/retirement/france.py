def france_age(row):
    # Waves 1-2
    if row["wave"] < 3:
        if row["yrscontribution"] + 60 - row["age"] >= 40:
            return 60
        elif row["age"] + 40 - row["yrscontribution"] >= 65:
            return 65
        else:
            return row["age"] + 40 - row["yrscontribution"]
    # Wave 4
    elif row["wave"] == 4:
        if (row["yrbirth"] == 1951 and row["mbirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 40:
                return 60
            elif row["age"] + 40 - row["yrscontribution"] >= 65:
                return 65
            else:
                return row["age"] + 40 - row["yrscontribution"]
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.33 - row["age"] >= 40:
                return 60.33
            elif row["age"] + 40 - row["yrscontribution"] >= 65.33:
                return 65.33
            else:
                return row["age"] + 40 - row["yrscontribution"]
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.67 - row["age"] >= 41:
                return 60.67
            elif row["age"] + 41 - row["yrscontribution"] >= 65.67:
                return 65.67
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1953:
            if row["yrscontribution"] + 61 - row["age"] >= 41:
                return 61
            elif row["age"] + 41 - row["yrscontribution"] >= 66:
                return 66
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.33 - row["age"] >= 41:
                return 61.33
            elif row["age"] + 41 - row["yrscontribution"] >= 66.33:
                return 66.33
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1955:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41:
                return 61.67
            elif row["age"] + 41 - row["yrscontribution"] >= 66.67:
                return 66.67
            else:
                return row["age"] + 41 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 41:
                return 62
            elif row["age"] + 41 - row["yrscontribution"] >= 67:
                return 67
            else:
                return row["age"] + 41 - row["yrscontribution"]
    # Waves 5 and 6
    elif row["wave"] == 5 or row["wave"] == 6:
        if (row["yrbirth"] == 1951 and row["mbirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 41:
                return 60
            elif row["age"] + 41 - row["yrscontribution"] >= 65:
                return 65
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.42 - row["age"] >= 41:
                return 60.42
            elif row["age"] + 41 - row["yrscontribution"] >= 65.42:
                return 65.42
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.83 - row["age"] >= 41:
                return 60.83
            elif row["age"] + 41 - row["yrscontribution"] >= 65.83:
                return 65.83
            else:
                return row["age"] + 41 - row["yrscontribution"]
        elif row["yrbirth"] == 1953:
            if row["yrscontribution"] + 61.25 - row["age"] >= 41.25:
                return 61.25
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.25:
                return 66.25
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41.25:
                return 61.67
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.67:
                return 66.67
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 41.5:
                return 62
            elif row["age"] + 41.5 - row["yrscontribution"] >= 67:
                return 67
            else:
                return row["age"] + 41.5 - row["yrscontribution"]
    # Waves 7 and 8
    elif row["wave"] == 7 or row["wave"] == 8:
        if (row["yrbirth"] == 1951 and row["mbirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 41.25:
                return 60
            elif row["age"] + 41.25 - row["yrscontribution"] >= 65:
                return 65
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.42 - row["age"] >= 41.25:
                return 60.42
            elif row["age"] + 41.25 - row["yrscontribution"] >= 65.42:
                return 65.42
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.83 - row["age"] >= 41.25:
                return 60.83
            elif row["age"] + 41.25 - row["yrscontribution"] >= 65.83:
                return 65.83
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] == 1953:
            if row["yrscontribution"] + 61.25 - row["age"] >= 41.25:
                return 61.25
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.25:
                return 66.25
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41.25:
                return 61.67
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.67:
                return 66.67
            else:
                return row["age"] + 41.25 - row["yrscontribution"]
        elif row["yrbirth"] >= 1955 and row["yrbirth"] < 1973:
            if row["yrscontribution"] + 62 - row["age"] >= 41.5:
                return 62
            elif row["age"] + 41.5 - row["yrscontribution"] >= 67:
                return 67
            else:
                return row["age"] + 41.5 - row["yrscontribution"]
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 43:
                return 62
            elif row["age"] + 43 - row["yrscontribution"] >= 67:
                return 67
            else:
                return row["age"] + 43 - row["yrscontribution"]


def france_change(row):
    # Wave 4
    if row["wave"] == 4:
        if row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.33 - row["age"] >= 40:
                return 0.33
            elif row["age"] + 40 - row["yrscontribution"] >= 65.33:
                return 0.33
            else:
                return 0
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.67 - row["age"] >= 41:
                return 0.66
            elif row["age"] + 41 - row["yrscontribution"] >= 65.67:
                return 0.66
            else:
                return 1
        elif row["yrbirth"] == 1953:
            return 1
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.33 - row["age"] >= 41:
                return 1.33
            elif row["age"] + 41 - row["yrscontribution"] >= 66.33:
                return 1.33
            else:
                return 1
        elif row["yrbirth"] == 1955:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41:
                return 1.67
            elif row["age"] + 41 - row["yrscontribution"] >= 66.67:
                return 1.67
            else:
                return 1
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 41:
                return 2
            elif row["age"] + 41 - row["yrscontribution"] >= 67:
                return 2
            else:
                return 1
    # Wave 5
    elif row["wave"] == 5:
        if (row["yrbirth"] == 1951 and row["mbirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 41:
                return 0
            elif row["age"] + 41 - row["yrscontribution"] >= 65:
                return 0
            else:
                return 1
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.42 - row["age"] >= 41:
                return 0.08
            elif row["age"] + 41 - row["yrscontribution"] >= 65.42:
                return 0.08
            else:
                return 0
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.83 - row["age"] >= 41:
                return 0.16
            elif row["age"] + 41 - row["yrscontribution"] >= 65.83:
                return 0.16
            else:
                return 0
        elif row["yrbirth"] == 1953:
            return 0.25
        elif row["yrbirth"] == 1954:
            if row["yrscontribution"] + 61.67 - row["age"] >= 41.25:
                return 0.34
            elif row["age"] + 41.25 - row["yrscontribution"] >= 66.67:
                return 0.34
            else:
                return 0.25
        else:
            if row["yrscontribution"] + 62 - row["age"] >= 41.5:
                return 0
            elif row["age"] + 41.5 - row["yrscontribution"] >= 67:
                return 0
            else:
                return 0.5
    # Wave 7
    elif row["wave"] == 7:
        if (row["yrbirth"] == 1951 and row["mbirth"] < 7) or (row["yrbirth"] <= 1951):
            if row["yrscontribution"] + 60 - row["age"] >= 41.25:
                return 0
            elif row["age"] + 41.25 - row["yrscontribution"] >= 65:
                return 0
            else:
                return 0.25
        elif row["yrbirth"] == 1951 and row["mbirth"] >= 7:
            if row["yrscontribution"] + 60.42 - row["age"] >= 41.25:
                return 0
            elif row["age"] + 41.25 - row["yrscontribution"] >= 65.42:
                return 0
            else:
                return 0.25
        elif row["yrbirth"] == 1952:
            if row["yrscontribution"] + 60.83 - row["age"] >= 41.25:
                return 0
            elif row["age"] + 41.25 - row["yrscontribution"] >= 65.83:
                return 0
            else:
                return 0.25
        elif row["yrbirth"] > 1973:
            if row["yrscontribution"] + 62 - row["age"] >= 43:
                return 0
            elif row["age"] + 43 - row["yrscontribution"] >= 67:
                return 0
            else:
                return 1.5
        else:
            return 0
    else:
        return 0
