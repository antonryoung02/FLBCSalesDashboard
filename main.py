from excel_to_pandas import ExcelToPandasPipeline
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

def extract(sheets_dict):
    pubhouse_dict = {}
    regex = r'^\d+\.\d+$' # filename must be <number>.<number>

    for sheet, df in sheets_dict.items():
        if re.search(regex, sheet, re.IGNORECASE) and len(df.columns) > 2:
            pubhouse_dict[sheet] = df
    return pubhouse_dict

def style():
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
    style()
    dataframes = pd.read_excel(
        os.path.join(BASE_DIR_PATH, DATA_FILENAME),
        header=0,
        skiprows=[1],
        sheet_name=None,
        index_col=0
    )
    dataframe_dict = extract(dataframes)


    e2p = ExcelToPandasPipeline()
    e2p.transform(dataframe_dict, inplace=True)

    tsp = TimeSeriesPipeline()
    time_dataframe_dict = tsp.transform(dataframe_dict)


    tscp = TimeSeriesCumulativePipeline()
    cumulative_time_dataframe_dict = tscp.transform(time_dataframe_dict)

    view = st.radio(
        "Select Data Type",
        ["Per-Product Data", "Per-Group Data"],
        index=["Per-Product Data", "Per-Group Data"].index(st.session_state.get("view", "Per-Product Data")),
        horizontal=True
    )

    if view == "Per-Product Data":
        selected_dataframe_dict = time_dataframe_dict
    else:
        selected_dataframe_dict = cumulative_time_dataframe_dict
        
    display_time_series(selected_dataframe_dict, selected_data = view)

    display_trends(selected_dataframe_dict, selected_data = view)

    display_cumulative(selected_dataframe_dict, selected_data = view)

    st.divider()
    display_menu_engineering(dataframe_dict)
    




if __name__ == "__main__":
    main()