def belgium(row):
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


def hello2(str):
    print(str)
