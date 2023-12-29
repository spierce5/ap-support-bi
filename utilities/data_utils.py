import pandas as pd
import json
import numpy as np

def convert_dataframe_to_dict(df):
    df_temp = convert_datetime_columns_to_isoformat(df)
    df_temp.fillna(value='', inplace=True)
    converted_dict = df_temp.to_dict(orient='records')
    return converted_dict

def convert_datetime_columns_to_isoformat(df):
    df_temp = df.copy()
    for col in df.select_dtypes(['datetime']).columns:
        df_temp[col] = df_temp[col].apply(lambda d: d.isoformat() if not pd.isnull(d) else '')
    return df_temp

def get_table_columns(table_name):
    with open('dataset.json') as f:
        ds = json.load(f)
        return [ col['name'] for col in list(filter(lambda x: x['name'] == table_name, ds.get('tables')))[0].get('columns')]