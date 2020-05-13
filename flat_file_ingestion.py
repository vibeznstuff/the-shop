import json
import os
import pandas as pd
import data_diagnostics as dd


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


def show_files_in_dir(dir_path):
    return os.listdir(dir_path)


def load_files_in_bulk(dir_path, print_diagnostics=True, files_to_ignore=None, 
    files_to_load=None):

    if files_to_ignore != None and files_to_load != None:
        raise ValueError("Cannot supply arguments to both files_to_ignore parameter \
            and files_to_load parameter. Please only use one.")

    file_paths = get_file_paths(dir_path)
    if files_to_ignore == None:
        files_to_ignore = []

    data_dict = {}
    diagnostics = {}

    for file_name in file_paths:
        if files_to_load != None:
            if '.csv' in file_paths[file_name] and file_name in files_to_load:
                print("Loading file: {}".format(file_name))
                data_dict[file_name] = get_df_from_csv(file_paths[file_name])
                diagnostics[file_name] = dd.get_diagnostic_summary(data_dict[file_name])
                print("\n\n")
        else:
            if '.csv' in file_paths[file_name] and file_name not in files_to_ignore:
                print("Loading file: {}".format(file_name))
                data_dict[file_name] = get_df_from_csv(file_paths[file_name])
                diagnostics[file_name] = dd.get_diagnostic_summary(data_dict[file_name])
                print("\n\n")

    return data_dict, diagnostics

