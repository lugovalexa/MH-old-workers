def belgium_age(row):
    if row["yrscontribution"] + 65 - row["age"] >= 45:
        return 65
    else:
        return row["age"] + 45 - row["yrscontribution"]
