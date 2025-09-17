import pandas as pd
import json

def load_data(path_list):
    dfs = []
    prefix_path = "data/json/"
    for file_path in path_list:
        full_path = prefix_path+file_path
        try:
            with open(full_path,"r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File not found! path: {full_path}")
        # flatten nested JSON into a DataFrame
        df = pd.json_normalize(data)
        dfs.append(df)
    
    final_df = pd.concat(dfs,ignore_index=True)
    final_df.shape
    return final_df

def add_cols(df):
    # per-row string length
    # In case any values are missing (NaN) or non-string types (like numbers), .str.len() would raise an error.
    try:
        df["name_length"] = df["user.name"].str.len()
        df["department_length"] = df["user.department"].str.len()
        df["email_length"] = df["user.email"].str.len()
        return df
    except Exception as e:
        print(f"Error occured: {e}")
    

