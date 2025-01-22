import pandas as pd
from app.config import CONFIG_SHEET_NAME, DATA_FILENAME, BASE_DIR_PATH
import os
import streamlit as st
import re
from app.base_filter import BaseFilter
import pandas as pd
from typing import Dict

def get_all_rows(dataframe_dict:Dict[str, pd.DataFrame]) -> set:
    """
    Args:
        dataframe_dict (Dict[str, pd.DataFrame]):

    Returns:
        set: All product names that exist in the data
    """
    index_set = set()
    for name, df in dataframe_dict.items():
        index_set = index_set.union(df.index)
    return index_set

def get_all_columns(dataframe_dict:Dict[str, pd.DataFrame]) -> set:
    """
    Args:
        dataframe_dict (Dict[str, pd.DataFrame]):

    Returns:
        set: All product features that exist in the data
    """
    column_set = set()
    for name, df in dataframe_dict.items():
        column_set = column_set.union(df.columns)
    return column_set

def sort_time_strings(time_strings:list) -> list:
    """
    Args:
        time_strings (list):

    Returns:
        list: Sorted list of time strings in m.yy format
    """
    time_tuples = [(int(t.split('.')[1]), int(t.split('.')[0])) for t in time_strings]
    
    sorted_tuples = sorted(time_tuples)
    sorted_strings = [f"{month}.{year:02}" for year, month in sorted_tuples]
    
    return sorted_strings

def read_categories() -> Dict[str, list]:
    """Reads the CONFIG file in the spreadsheet to define related products for aggregation

    Returns:
        Dict[str, list]:
    """
    df = pd.read_excel(os.path.join(BASE_DIR_PATH, DATA_FILENAME), sheet_name=CONFIG_SHEET_NAME)
    categories_dict = {
        column: df[column].dropna().tolist()
        for column in df.columns
    }
    categories_dict["ALL ITEMS"] = []
    return categories_dict
        

def extract_dataframe_dict_from_excel() -> Dict[str, pd.DataFrame]:
    """Reads all sheets in m.yy format from the data file

    Returns:
        Dict[str, pd.DataFrame]:
    """
    sheets_dict = pd.read_excel(
        os.path.join(BASE_DIR_PATH, DATA_FILENAME),
        header=0,
        skiprows=[1],
        sheet_name=None,
        index_col=0
    )
    pubhouse_monthly_sales_dict = {}
    for name, df in sheets_dict.items():
        if sheet_is_valid(name, df):
            pubhouse_monthly_sales_dict[name] = df
    return pubhouse_monthly_sales_dict

def sheet_is_valid(name:str, df:pd.DataFrame) -> bool:
    regex = r'^([1-9]|1[0-2])\.\d{2}$'
    return bool(re.search(regex, name, re.IGNORECASE)) and len(df.columns) >= 2

def initialize_streamlit_styling() -> None:
    st.set_page_config(layout="wide", page_title="Sales Dashboard", page_icon="📊")
    st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            text-overflow: ellipsis;
            white-space: nowrap;
            overflow: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

def display_data_with_pipeline(dataframe_dict:Dict[str, pd.DataFrame], selected_data:str, pipeline:callable, pipeline_name:str, filter:BaseFilter) -> None:
    st.title(f"{selected_data} {pipeline_name}")
    all_time_rows = sort_time_strings(list(get_all_rows(dataframe_dict)))
    all_time_columns = list(get_all_columns(dataframe_dict))
    all_time_names = sorted([n for n in dataframe_dict.keys()])

    col1, col2 = st.columns([2, 8]) 

    with col1:
        selected_name = filter.get_selected_dataframe(all_time_names, f"{pipeline_name}_radio")

    with col2:
        filter.display_quick_select_columns(selected_data, f"{pipeline_name}_multi")
        selected_columns = filter.get_selected_columns(all_time_columns, f"{pipeline_name}_multi")
        selected_rows = filter.get_selected_rows(all_time_rows, f"{pipeline_name}_slider")
        filtered_dataframe = filter.filter_dataframe(dataframe_dict, selected_columns, selected_rows, selected_name)
        pipeline(filtered_dataframe)