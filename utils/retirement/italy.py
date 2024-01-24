def italy_age(row):
    # Male
    if row["gender"] == "Male":
        # Wave 4
        if row["wave"] == 4:
            if row["yr1contribution"] < 1996:
                if row["yrscontribution"] + 66 - row["age"] >= 20:
                    return 66
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 66 - row["age"] >= 20:
                    return 66
                elif row["age"] + 20 - row["yrscontribution"] < 70:
                    return row["age"] + 20 - row["yrscontribution"]
                elif row["yrscontribution"] + 70 - row["age"] >= 5:
                    return 70
                else:
                    return row["age"] + 5 - row["yrscontribution"]
        # Wave 6
        else:
            if row["yr1contribution"] < 1996:
                if row["yrscontribution"] + 66.25 - row["age"] >= 20:
                    return 66.25
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 66.25 - row["age"] >= 20:
                    return 66.25
                elif row["age"] + 20 - row["yrscontribution"] < 70:
                    return row["age"] + 20 - row["yrscontribution"]
                elif row["yrscontribution"] + 70 - row["age"] >= 5:
                    return 70
                else:
                    return row["age"] + 5 - row["yrscontribution"]

    # Female
    else:
        # Wave 4
        if row["wave"] == 4:
            if row["job_status"] == "Public sector employee":
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 61 - row["age"] >= 20:
                        return 61
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 61 - row["age"] >= 20:
                        return 61
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
            else:
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 60 - row["age"] >= 20:
                        return 60
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 60 - row["age"] >= 20:
                        return 60
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
        # Wave 6
        else:
            if row["job_status"] == "Self-employed":
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 64.75 - row["age"] >= 20:
                        return 64.75
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 64.75 - row["age"] >= 20:
                        return 64.75
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
            elif row["job_status"] == "Civil servant":
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 66.25 - row["age"] >= 20:
                        return 66.25
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 66.25 - row["age"] >= 20:
                        return 66.25
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
            else:
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 63.75 - row["age"] >= 20:
                        return 63.75
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 63.75 - row["age"] >= 20:
                        return 63.75
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
