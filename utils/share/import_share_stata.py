import os
from functools import reduce

import pandas as pd


def import_share_stata(
    folder_path, file_names, merge_columns, convert_categoricals=False
):
    datasets = []

    for filename in os.listdir(folder_path):
        if any(filename.endswith(file) for file in file_names):
            file_path = os.path.join(folder_path, filename)
            dataset = pd.read_stata(
                file_path, convert_categoricals=convert_categoricals
            )
            datasets.append(dataset)

    df = reduce(lambda left, right: pd.merge(left, right, on=merge_columns), datasets)
    return df
