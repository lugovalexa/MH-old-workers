import os
from functools import reduce

import pandas as pd


def import_share_stata(
    folder_path, file_names, convert_categoricals=False, merge_columns=[]
):
    """
    Import and merge Stata datasets from a specified folder.

    Parameters:
    - folder_path (str): The path to the folder containing Stata datasets.
    - file_names (list): A list of file names (or file extensions) to consider for import.
    - convert_categoricals (bool, optional): Whether to convert categorical columns. Default is False.

    Returns:
    - pd.DataFrame: Merged DataFrame containing data from all the Stata datasets.

    Example:
    ```python
    folder_path = '/path/to/datasets/'
    file_names = ['data1.dta', 'data2.dta']
    merged_df = import_share_stata(folder_path, file_names, merge_columns, convert_categoricals=True)
    ```

    Note:
    - The function assumes that the Stata datasets have compatible structures for merging.
    - If convert_categoricals is set to True, categorical columns will be converted to the corresponding Pandas categorical dtype.
    """
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


def import_share_stata1(file_names, convert_categoricals=False, waves=[4, 5, 6]):
    datasets_folder = []

    for wave in waves:
        folder = f"/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/sharew{wave}_rel8-0-0_ALL_datasets_stata/"

        datasets = []

        for filename in os.listdir(folder):
            if any(filename.endswith(file) for file in file_names):
                file_path = os.path.join(folder, filename)
                dataset = pd.read_stata(
                    file_path, convert_categoricals=convert_categoricals
                )
                dataset["wave"] = wave
                dataset = dataset.rename(
                    columns={
                        f"hhid{wave}": "hhid",
                        f"mergeidp{wave}": "mergeidp",
                        f"coupleid{wave}": "coupleid",
                    }
                )
                datasets.append(dataset)

        dataset_folder = reduce(
            lambda left, right: pd.merge(
                left,
                right,
                on=[
                    "mergeid",
                    "hhid",
                    "mergeidp",
                    "coupleid",
                    "country",
                    "language",
                    "wave",
                ],
            ),
            datasets,
        )
        datasets_folder.append(dataset_folder)

    df = pd.concat(datasets_folder, sort=False, axis=0).reset_index(drop=True)

    return df
