import os
from functools import reduce

import pandas as pd


def import_share_stata(
    folder_path, file_names, merge_columns, convert_categoricals=False
):
    """
    Import and merge Stata datasets from a specified folder.

    Parameters:
    - folder_path (str): The path to the folder containing Stata datasets.
    - file_names (list): A list of file names (or file extensions) to consider for import.
    - merge_columns (list): Columns based on which the datasets will be merged.
    - convert_categoricals (bool, optional): Whether to convert categorical columns. Default is False.

    Returns:
    - pd.DataFrame: Merged DataFrame containing data from all the Stata datasets.

    Example:
    ```python
    folder_path = '/path/to/datasets/'
    file_names = ['data1.dta', 'data2.dta']
    merge_columns = ['id', 'date']
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
