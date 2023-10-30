def austria(row):
    # Male
    if row["gender"] == "Male":
        if row["yrscontribution"] + 65 - row["age"] >= 15:
            return 65
        else:
            return row["age"] + 15 - row["yrscontribution"]

    # Female
    else:
        if row["yrscontribution"] + 60 - row["age"] >= 15:
            return 60
        else:
            return row["age"] + 15 - row["yrscontribution"]


def hello(str):
    print(str)
