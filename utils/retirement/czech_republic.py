def czech_republic_age(row):
    # Male
    if row["gender"] == "Male":
        # Wave 1
        if row["wave"] == 1:
            if row["yrscontribution"] + 61.33 - row["age"] >= 25:
                return 61.33
            elif row["age"] + 25 - row["yrscontribution"] < 65:
                return row["age"] + 25 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 65
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 2
        elif row["wave"] == 2:
            if row["yrscontribution"] + 61.67 - row["age"] >= 25:
                return 61.67
            elif row["age"] + 25 - row["yrscontribution"] < 65:
                return row["age"] + 25 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 15:
                return 65
            else:
                return row["age"] + 15 - row["yrscontribution"]
        # Wave 4
        elif row["wave"] == 4:
            if row["yrscontribution"] + 62.17 - row["age"] >= 27:
                return 62.17
            elif row["age"] + 27 - row["yrscontribution"] < 65:
                return row["age"] + 27 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 17:
                return 65
            else:
                return row["age"] + 17 - row["yrscontribution"]
        # Wave 5
        elif row["wave"] == 5:
            if row["yrscontribution"] + 62.5 - row["age"] >= 29:
                return 62.5
            elif row["age"] + 29 - row["yrscontribution"] < 65:
                return row["age"] + 29 - row["yrscontribution"]
            elif row["yrscontribution"] + 65 - row["age"] >= 19:
                return 65
            else:
                return row["age"] + 19 - row["yrscontribution"]
        # Wave 6
        elif row["wave"] == 6:
            if row["yrscontribution"] + 62.83 - row["age"] >= 31:
                return 62.83
            elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                return row["age"] + 31 - row["yrscontribution"]
            elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                return 62.83 + 5
            else:
                return row["age"] + 20 - row["yrscontribution"]
        # Wave 7
        elif row["wave"] == 7:
            if row["yrscontribution"] + 63.17 - row["age"] >= 33:
                return 63.17
            elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                return row["age"] + 33 - row["yrscontribution"]
            elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                return 63.17 + 5
            else:
                return row["age"] + 20 - row["yrscontribution"]
        # Wave 8
        else:
            if row["yrscontribution"] + 63.67 - row["age"] >= 35:
                return 63.67
            elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                return row["age"] + 35 - row["yrscontribution"]
            elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                return 63.67 + 5
            else:
                return row["age"] + 20 - row["yrscontribution"]

    # Female
    else:
        # Wave 1
        if row["wave"] == 1:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 59.33 - row["age"] >= 25:
                    return 59.33
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 58.33 - row["age"] >= 25:
                    return 58.33
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 57.33 - row["age"] >= 25:
                    return 57.33
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 56.33 - row["age"] >= 25:
                    return 56.33
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 55.33 - row["age"] >= 25:
                    return 55.33
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
        # Wave 2
        elif row["wave"] == 2:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 60 - row["age"] >= 25:
                    return 60
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 59 - row["age"] >= 25:
                    return 59
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 58 - row["age"] >= 25:
                    return 58
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 57 - row["age"] >= 25:
                    return 57
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 56 - row["age"] >= 25:
                    return 56
                elif row["age"] + 25 - row["yrscontribution"] < 65:
                    return row["age"] + 25 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 15:
                    return 65
                else:
                    return row["age"] + 15 - row["yrscontribution"]
        # Wave 4
        elif row["wave"] == 4:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 61 - row["age"] >= 27:
                    return 61
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 60 - row["age"] >= 27:
                    return 60
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 59 - row["age"] >= 27:
                    return 59
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 58 - row["age"] >= 27:
                    return 58
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 57 - row["age"] >= 27:
                    return 57
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return row["age"] + 27 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 17:
                    return 65
                else:
                    return row["age"] + 17 - row["yrscontribution"]
        # Wave 5
        elif row["wave"] == 5:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 61.67 - row["age"] >= 29:
                    return 61.67
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return row["age"] + 29 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 19:
                    return 65
                else:
                    return row["age"] + 19 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 60.67 - row["age"] >= 29:
                    return 60.67
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return row["age"] + 29 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 19:
                    return 65
                else:
                    return row["age"] + 19 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 59.67 - row["age"] >= 29:
                    return 59.67
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return row["age"] + 29 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 19:
                    return 65
                else:
                    return row["age"] + 19 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 58.67 - row["age"] >= 29:
                    return 58.67
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return row["age"] + 29 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 19:
                    return 65
                else:
                    return row["age"] + 19 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 57.67 - row["age"] >= 29:
                    return 57.67
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return row["age"] + 29 - row["yrscontribution"]
                elif row["yrscontribution"] + 65 - row["age"] >= 19:
                    return 65
                else:
                    return row["age"] + 19 - row["yrscontribution"]
        # Wave 6
        elif row["wave"] == 6:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 62 - row["age"] >= 31:
                    return 62
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 61 - row["age"] >= 31:
                    return 61
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 60 - row["age"] >= 31:
                    return 60
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 59 - row["age"] >= 31:
                    return 59
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 58 - row["age"] >= 31:
                    return 58
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return row["age"] + 31 - row["yrscontribution"]
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
        # Wave 7
        elif row["wave"] == 7:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 62.67 - row["age"] >= 33:
                    return 62.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return row["age"] + 33 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 61.67 - row["age"] >= 33:
                    return 61.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return row["age"] + 33 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 60.67 - row["age"] >= 33:
                    return 60.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return row["age"] + 33 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 59.67 - row["age"] >= 33:
                    return 59.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return row["age"] + 33 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 58.67 - row["age"] >= 33:
                    return 58.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return row["age"] + 33 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
        # Wave 8
        else:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 63.67 - row["age"] >= 35:
                    return 63.67
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return row["age"] + 35 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 62.67 - row["age"] >= 35:
                    return 62.67
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return row["age"] + 35 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 61.67 - row["age"] >= 35:
                    return 61.67
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return row["age"] + 35 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 60.67 - row["age"] >= 35:
                    return 60.67
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return row["age"] + 35 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]
            else:
                if row["yrscontribution"] + 59.67 - row["age"] >= 35:
                    return 59.67
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return row["age"] + 35 - row["yrscontribution"]
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5
                else:
                    return row["age"] + 20 - row["yrscontribution"]


def czech_republic_change(row):
    # Male
    if row["gender"] == "Male":
        # Wave 2
        if row["wave"] == 2:
            if row["yrscontribution"] + 61.67 - row["age"] >= 25:
                return 61.67 - 61.33
            else:
                return 0
        # Wave 4
        elif row["wave"] == 4:
            if row["yrscontribution"] + 62.17 - row["age"] >= 27:
                return 62.17 - 61.67
            elif row["age"] + 27 - row["yrscontribution"] < 65:
                return 2
            elif row["yrscontribution"] + 65 - row["age"] < 17:
                return 2
            else:
                return 0
        # Wave 5
        elif row["wave"] == 5:
            if row["yrscontribution"] + 62.5 - row["age"] >= 29:
                return 62.5 - 62.17
            elif row["age"] + 29 - row["yrscontribution"] < 65:
                return 2
            elif row["yrscontribution"] + 65 - row["age"] < 19:
                return 2
            else:
                return 0
        # Wave 6
        elif row["wave"] == 6:
            if row["yrscontribution"] + 62.83 - row["age"] >= 31:
                return 62.83 - 62.5
            elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                return 2
            elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                return 62.83 + 5 - 65
            else:
                return 1
        # Wave 7
        elif row["wave"] == 7:
            if row["yrscontribution"] + 63.17 - row["age"] >= 33:
                return 63.17 - 62.83
            elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                return 2
            elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                return 63.17 + 5 - (62.83 + 5)
            else:
                return 0
        # Wave 8
        elif row["wave"] == 8:
            if row["yrscontribution"] + 63.67 - row["age"] >= 35:
                return 63.67 - 63.17
            elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                return 2
            elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                return 63.67 + 5 - (63.17 + 5)
            else:
                return 0
        else:
            return 0

    # Female
    else:
        # Wave 2
        if row["wave"] == 2:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 60 - row["age"] >= 25:
                    return 60 - 59.33
                else:
                    return 0
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 59 - row["age"] >= 25:
                    return 59 - 58.33
                else:
                    return 0
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 58 - row["age"] >= 25:
                    return 58 - 57.33
                else:
                    return 0
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 57 - row["age"] >= 25:
                    return 57 - 56.33
                else:
                    return 0
            else:
                if row["yrscontribution"] + 56 - row["age"] >= 25:
                    return 56 - 55.33
                else:
                    return 0
        # Wave 4
        elif row["wave"] == 4:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 61 - row["age"] >= 27:
                    return 1
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 17:
                    return 2
                else:
                    return 0
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 60 - row["age"] >= 27:
                    return 1
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 17:
                    return 2
                else:
                    return 0
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 59 - row["age"] >= 27:
                    return 1
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 17:
                    return 2
                else:
                    return 0
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 58 - row["age"] >= 27:
                    return 1
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 17:
                    return 2
                else:
                    return 0
            else:
                if row["yrscontribution"] + 57 - row["age"] >= 27:
                    return 1
                elif row["age"] + 27 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 17:
                    return 2
                else:
                    return 0
        # Wave 5
        elif row["wave"] == 5:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 61.67 - row["age"] >= 29:
                    return 61.67 - 61
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 19:
                    return 2
                else:
                    return 0
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 60.67 - row["age"] >= 29:
                    return 60.67 - 60
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 19:
                    return 2
                else:
                    return 0
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 59.67 - row["age"] >= 29:
                    return 59.67 - 59
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 19:
                    return 2
                else:
                    return 0
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 58.67 - row["age"] >= 29:
                    return 58.67 - 58
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 19:
                    return 2
                else:
                    return 0
            else:
                if row["yrscontribution"] + 57.67 - row["age"] >= 29:
                    return 57.67 - 57
                elif row["age"] + 29 - row["yrscontribution"] < 65:
                    return 2
                elif row["yrscontribution"] + 65 - row["age"] < 19:
                    return 2
                else:
                    return 0
        # Wave 6
        elif row["wave"] == 6:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 62 - row["age"] >= 31:
                    return 0.33
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return 2
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5 - 65
                else:
                    return 1
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 61 - row["age"] >= 31:
                    return 0.33
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return 2
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5 - 65
                else:
                    return 1
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 60 - row["age"] >= 31:
                    return 0.33
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return 2
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5 - 65
                else:
                    return 1
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 59 - row["age"] >= 31:
                    return 0.33
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return 2
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5 - 65
                else:
                    return 1
            else:
                if row["yrscontribution"] + 58 - row["age"] >= 31:
                    return 0.33
                elif row["age"] + 31 - row["yrscontribution"] < 62.83 + 5:
                    return 2
                elif row["yrscontribution"] + 62.83 + 5 - row["age"] >= 20:
                    return 62.83 + 5 - 65
                else:
                    return 1
        # Wave 7
        elif row["wave"] == 7:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 62.67 - row["age"] >= 33:
                    return 0.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return 2
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5 - (62.83 + 5)
                else:
                    return 0
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 61.67 - row["age"] >= 33:
                    return 0.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return 2
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5 - (62.83 + 5)
                else:
                    return 0
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 60.67 - row["age"] >= 33:
                    return 0.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return 2
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5 - (62.83 + 5)
                else:
                    return 0
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 59.67 - row["age"] >= 33:
                    return 0.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return 2
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5 - (62.83 + 5)
                else:
                    return 0
            else:
                if row["yrscontribution"] + 58.67 - row["age"] >= 33:
                    return 0.67
                elif row["age"] + 33 - row["yrscontribution"] < 63.17 + 5:
                    return 2
                elif row["yrscontribution"] + 63.17 + 5 - row["age"] >= 20:
                    return 63.17 + 5 - (62.83 + 5)
                else:
                    return 0
        # Wave 8
        elif row["wave"] == 8:
            if row["nb_children"] == 0:
                if row["yrscontribution"] + 63.67 - row["age"] >= 35:
                    return 1
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return 2
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5 - (63.17 + 5)
                else:
                    return 0
            elif row["nb_children"] == 1:
                if row["yrscontribution"] + 62.67 - row["age"] >= 35:
                    return 1
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return 2
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5 - (63.17 + 5)
                else:
                    return 0
            elif row["nb_children"] == 2:
                if row["yrscontribution"] + 61.67 - row["age"] >= 35:
                    return 1
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return 2
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5 - (63.17 + 5)
                else:
                    return 0
            elif row["nb_children"] == 3 or row["nb_children"] == 4:
                if row["yrscontribution"] + 60.67 - row["age"] >= 35:
                    return 1
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return 2
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5 - (63.17 + 5)
                else:
                    return 0
            else:
                if row["yrscontribution"] + 59.67 - row["age"] >= 35:
                    return 1
                elif row["age"] + 35 - row["yrscontribution"] < 63.67 + 5:
                    return 2
                elif row["yrscontribution"] + 63.67 + 5 - row["age"] >= 20:
                    return 63.67 + 5 - (63.17 + 5)
                else:
                    return 0
        else:
            return 0
