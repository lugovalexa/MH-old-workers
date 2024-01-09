import os

import pandas as pd


def add_weights():
    def read_dta_files(folder_path):
        file_list = os.listdir(folder_path)
        dfs = []
        for file in file_list:
            if file.endswith(".dta"):
                file_path = os.path.join(folder_path, file)
                df = pd.read_stata(file_path)
                dfs.append(df)
        return pd.concat(dfs, ignore_index=True)[["mergeid", "dw_w4", "my_wgt"]]

    def update_csv_files(folder_path, weights):
        file_list = os.listdir(folder_path)
        for file in file_list:
            if file.startswith("3digits") or file.startswith("4digits"):
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                df = df.merge(weights, on="mergeid", how="left")
                df = df.dropna(subset=["my_wgt"]).reset_index(drop=True)
                df.to_csv(file_path, index=False)

    weights_folder_path = (
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/weights/"
    )
    results_folder_path = (
        "/Users/alexandralugova/Documents/GitHub/MH-old-workers/data/datasets/results/"
    )

    weights = read_dta_files(weights_folder_path)
    update_csv_files(results_folder_path, weights)
