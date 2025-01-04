from standardize import StandardizePipeline 
from time_series import TimeSeriesPipeline
from time_series_cumulative import TimeSeriesCumulativePipeline
import re
import pandas as pd
import streamlit as st
from displays.display_menu_engineering import display_menu_engineering
from displays.display_cumulative import display_cumulative
from displays.display_time_series import display_time_series
from displays.display_trends import display_trends
import os
from config import BASE_DIR_PATH, DATA_FILENAME
import warnings

def extract(sheets_dict):
    pubhouse_dict = {}
    for name, df in sheets_dict.items():
        if sheet_is_valid(name, df):
            pubhouse_dict[name] = df
    return pubhouse_dict

def sheet_is_valid(name, df):
    regex = r'^\d+\.\d+$' # filename must be <number>.<number>
    return re.search(regex, name, re.IGNORECASE) and len(df.columns) >= 2

def apply_streamlit_override_styles():
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
                
def main():
    st.set_page_config(layout="wide", page_title="Sales Dashboard", page_icon="📊")
    apply_streamlit_override_styles()
    warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

    dataframes = pd.read_excel(
        os.path.join(BASE_DIR_PATH, DATA_FILENAME),
        header=0,
        skiprows=[1],
        sheet_name=None,
        index_col=0
    )
    dataframe_dict = extract(dataframes)

    sp = StandardizePipeline()
    sp.transform(dataframe_dict, inplace=True)

    tsp = TimeSeriesPipeline()
    time_dataframe_dict = tsp.transform(dataframe_dict)

    tscp = TimeSeriesCumulativePipeline()
    cumulative_time_dataframe_dict = tscp.transform(time_dataframe_dict)

    selected_data = st.radio(
        "Select Data Type",
        ["Per-Product Data", "Per-Group Data"],
        index=["Per-Product Data", "Per-Group Data"].index(st.session_state.get("selected_data", "Per-Product Data")),
        horizontal=True
    )

    if selected_data == "Per-Product Data":
        selected_dataframe_dict = time_dataframe_dict
    else:
        selected_dataframe_dict = cumulative_time_dataframe_dict
        
    display_time_series(selected_dataframe_dict, selected_data = selected_data)
    display_trends(selected_dataframe_dict, selected_data = selected_data)
    display_cumulative(selected_dataframe_dict, selected_data = selected_data)

    st.divider()

    display_menu_engineering(dataframe_dict)
    




if __name__ == "__main__":
    main()