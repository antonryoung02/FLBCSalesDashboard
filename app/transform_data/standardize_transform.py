import pandas as pd
from app.utils import get_all_columns, get_all_rows
from app.dataframe_operations import convert_columns_to_float64, insert_null_columns, insert_null_rows
from typing import Dict

def standardize_transform(dataframe_dict:Dict[str, pd.DataFrame], inplace:bool=True) -> Dict[str, pd.DataFrame] | None:
    """Normalizes dataframes in the dict to be of same shape, with same columns and index

    Args:
        dataframe_dict (dict): Raw dataframe dict read from extract
        inplace (bool, optional): Whether to operate on the input object. Defaults to True.

    Returns:
        dict | None:
    """
    if not inplace:
        dataframe_dict = {name: df.copy() for name, df in dataframe_dict.items()}
    
    all_rows = get_all_rows(dataframe_dict)
    all_columns = get_all_columns(dataframe_dict)
    for name, df in dataframe_dict.items():
        dataframe_dict[name] = _standardize_dataframe(df, all_rows, all_columns)

    if not inplace:
        return dataframe_dict

def _standardize_dataframe(df:pd.DataFrame, all_rows:set, all_columns:set) -> pd.DataFrame:
    df = _insert_missing_rows(df, all_rows)
    _insert_missing_columns(df, all_columns)
    convert_columns_to_float64(df)
    return df

def _insert_missing_rows(df:pd.DataFrame, all_rows:set) -> pd.DataFrame:
    missing_rows = list(all_rows.difference(set(df.index)))
    df = insert_null_rows(df, missing_rows)
    df.sort_index(axis=0, inplace=True)
    return df

def _insert_missing_columns(df:pd.DataFrame, all_columns:set) -> None: 
    missing_columns = list(all_columns.difference(set(df.columns)))
    insert_null_columns(df, missing_columns)
    df.sort_index(axis=1, inplace=True)