def italy_age(row):
    # Male
    if row["gender"] == "Male":
        # Waves 1-2
        if row["wave"] < 3:
            if row["yr1contribution"] < 1996:
                if row["yrscontribution"] + 65 - row["age"] >= 20:
                    return 65
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 65 - row["age"] >= 20:
                    return 65
                elif row["age"] + 20 - row["yrscontribution"] < 70:
                    return row["age"] + 20 - row["yrscontribution"]
                elif row["yrscontribution"] + 70 - row["age"] >= 5:
                    return 70
                else:
                    return row["age"] + 5 - row["yrscontribution"]
        # Wave 4
        elif row["wave"] == 4:
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
        # Waves 5 and 6
        elif row["wave"] == 5 or row["wave"] == 6:
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
        # Wave 7
        elif row["wave"] == 7:
            if row["yr1contribution"] < 1996:
                if row["yrscontribution"] + 66.58 - row["age"] >= 20:
                    return 66.58
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 66.58 - row["age"] >= 20:
                    return 66.58
                elif row["age"] + 20 - row["yrscontribution"] < 70:
                    return row["age"] + 20 - row["yrscontribution"]
                elif row["yrscontribution"] + 70 - row["age"] >= 5:
                    return 70
                else:
                    return row["age"] + 5 - row["yrscontribution"]
        # Wave 8
        else:
            if row["yr1contribution"] < 1996:
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 67
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 67
                elif row["age"] + 20 - row["yrscontribution"] < 70:
                    return row["age"] + 20 - row["yrscontribution"]
                elif row["yrscontribution"] + 70 - row["age"] >= 5:
                    return 70
                else:
                    return row["age"] + 5 - row["yrscontribution"]

    # Female
    else:
        # Waves 1-2
        if row["wave"] < 3:
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
        # Wave 4
        elif row["wave"] == 4:
            if row["public_job"] == "Yes":
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
        # Wave 5
        elif row["wave"] == 5:
            if row["job_status"] == "Self-employed":
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
                    if row["yrscontribution"] + 62.25 - row["age"] >= 20:
                        return 62.25
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 62.25 - row["age"] >= 20:
                        return 62.25
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
        # Wave 6
        elif row["wave"] == 6:
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
        # Wave 7
        elif row["wave"] == 7:
            if row["job_status"] == "Self-employed":
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 66.08 - row["age"] >= 20:
                        return 66.08
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 66.08 - row["age"] >= 20:
                        return 66.08
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
            elif row["job_status"] == "Civil servant":
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 66.58 - row["age"] >= 20:
                        return 66.58
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 66.58 - row["age"] >= 20:
                        return 66.58
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
            else:
                if row["yr1contribution"] < 1996:
                    if row["yrscontribution"] + 65.58 - row["age"] >= 20:
                        return 65.58
                    else:
                        return row["age"] + 20 - row["yrscontribution"]
                else:
                    if row["yrscontribution"] + 65.58 - row["age"] >= 20:
                        return 65.58
                    elif row["age"] + 20 - row["yrscontribution"] < 70:
                        return row["age"] + 20 - row["yrscontribution"]
                    elif row["yrscontribution"] + 70 - row["age"] >= 5:
                        return 70
                    else:
                        return row["age"] + 5 - row["yrscontribution"]
        # Wave 8
        else:
            if row["yr1contribution"] < 1996:
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 67
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 67
                elif row["age"] + 20 - row["yrscontribution"] < 70:
                    return row["age"] + 20 - row["yrscontribution"]
                elif row["yrscontribution"] + 70 - row["age"] >= 5:
                    return 70
                else:
                    return row["age"] + 5 - row["yrscontribution"]


def italy_change(row):
    # Male
    if row["gender"] == "Male":
        # Wave 4
        if row["wave"] == 4:
            if row["yrscontribution"] + 66 - row["age"] >= 20:
                return 1
            else:
                return 0
        # Wave 5
        elif row["wave"] == 5:
            if row["yrscontribution"] + 66.25 - row["age"] >= 20:
                return 0.25
            else:
                return 0
        # Wave 7
        elif row["wave"] == 7:
            if row["yrscontribution"] + 66.58 - row["age"] >= 20:
                return 0.33
            else:
                return 0
        # Wave 8
        elif row["wave"] == 8:
            if row["yrscontribution"] + 67 - row["age"] >= 20:
                return 0.42
            else:
                return 0
        else:
            return 0

    # Female
    else:
        # Wave 4
        if row["wave"] == 4:
            if row["public_job"] == "Yes":
                if row["yrscontribution"] + 61 - row["age"] >= 20:
                    return 1
                else:
                    return 0
            else:
                return 0
        # Wave 5
        elif row["wave"] == 5:
            if row["job_status"] == "Self-employed":
                if row["yrscontribution"] + 63.75 - row["age"] >= 20:
                    return 3.75
                else:
                    return 0
            elif row["job_status"] == "Civil servant":
                if row["yrscontribution"] + 66.25 - row["age"] >= 20:
                    return 6.25
                else:
                    return 0
            else:
                if row["yrscontribution"] + 62.25 - row["age"] >= 20:
                    return 2.25
                else:
                    return 0
        # Wave 6
        elif row["wave"] == 6:
            if row["job_status"] == "Self-employed":
                if row["yrscontribution"] + 64.75 - row["age"] >= 20:
                    return 1
                else:
                    return 0
            elif row["job_status"] == "Civil servant":
                return 0
            else:
                if row["yrscontribution"] + 63.75 - row["age"] >= 20:
                    return 1.5
                else:
                    return 0
        # Wave 7
        elif row["wave"] == 7:
            if row["job_status"] == "Self-employed":
                if row["yrscontribution"] + 66.08 - row["age"] >= 20:
                    return 1.33
                else:
                    return 0
            elif row["job_status"] == "Civil servant":
                if row["yrscontribution"] + 66.58 - row["age"] >= 20:
                    return 2.83
                else:
                    return 0
            else:
                if row["yrscontribution"] + 65.58 - row["age"] >= 20:
                    return 1.83
                else:
                    return 0
        # Wave 8
        elif row["wave"] == 8:
            if row["job_status"] == "Self-employed":
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 0.92
                else:
                    return 0
            elif row["job_status"] == "Civil servant":
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 0.42
                else:
                    return 0
            else:
                if row["yrscontribution"] + 67 - row["age"] >= 20:
                    return 1.42
                else:
                    return 0
        else:
            return 0
