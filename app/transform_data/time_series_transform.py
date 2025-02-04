import pandas as pd
from app.utils import get_all_columns, get_all_rows
from app.dataframe_operations import convert_columns_to_float64
from typing import Dict

def time_series_transform(dataframe_dict:Dict[str, pd.DataFrame], features_to_ignore:list=[]) -> dict:
    columns = sorted(list(get_all_columns(dataframe_dict)))
    rows = sorted(list(get_all_rows(dataframe_dict)))
    transformed_data = {}

    for f in columns:
        if f not in features_to_ignore:
            transformed_data[f] = _create_dataframe_for_feature(f, rows, dataframe_dict)
    
    return transformed_data

def _create_dataframe_for_feature(f:str, rows:list, dataframe_dict:Dict[str, pd.DataFrame]) -> pd.DataFrame:
    feature_df = pd.DataFrame() 
    for df in dataframe_dict.values():
        feature_df = pd.concat([feature_df, df[f]], axis=1)

    feature_df = feature_df.T
    feature_df.index = [name for name in dataframe_dict]
    feature_df.columns = rows
    convert_columns_to_float64(feature_df)

    return feature_df
