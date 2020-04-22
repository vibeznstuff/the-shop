import json
import os
import pandas as pd


def get_file_paths(dir_path):
    dir_contents = os.listdir(dir_path)
    path_dict = {}

    for file_name in dir_contents:
        try:
            base_name, extension = file_name.split(".")
            if extension.find(".") > -1:
                pass
            else:
                path_dict[base_name.lower()] = dir_path + "\\" + file_name
        except:
            pass

    return path_dict


def get_df_from_csv(file_path):
    return pd.read_csv(file_path)


def get_dict_from_json(file_path):
    with open(file_path,'r') as f:
        return json.load(f)


