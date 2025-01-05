import pandas as pd
from app.config import CONFIG_SHEET_NAME, DATA_FILENAME, BASE_DIR_PATH
import os

def get_all_rows(dataframe_dict) -> set:
    """ Retrieves all products that exist in the data

    Args:
        dataframe_dict (dict[str:pd.DataFrame]):
    """
    index_set = set()
    for name, df in dataframe_dict.items():
        index_set = index_set.union(df.index)
    return index_set

def get_all_columns(dataframe_dict) -> set:
    """ Retrieves all product features that exist in the data

    Args:
        dataframe_dict (dict[str:pd.DataFrame]):
    """
    column_set = set()
    for name, df in dataframe_dict.items():
        column_set = column_set.union(df.columns)
    return column_set

def sort_time_strings(time_strings: list) -> list:
    """
    Sorts a list of time strings in the format <M>.<Y> (e.g., "1.24", "12.23").
    
    Args:
        time_strings (List[str]): List of time strings to be sorted.
    
    Returns:
        List[str]: Sorted list of time strings.
    """
    time_tuples = [(int(t.split('.')[1]), int(t.split('.')[0])) for t in time_strings]
    
    sorted_tuples = sorted(time_tuples)
    sorted_strings = [f"{month}.{year:02}" for year, month in sorted_tuples]
    
    return sorted_strings

def convert_columns_to_float64(df:pd.DataFrame) -> None:
    int_cols = df.select_dtypes(include=['int','object']).columns
    df[int_cols] = df[int_cols].astype('float64')

def read_categories_dataframe() -> pd.DataFrame:
    return pd.read_excel(os.path.join(BASE_DIR_PATH, DATA_FILENAME), sheet_name=CONFIG_SHEET_NAME)