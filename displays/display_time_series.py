import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from filters import BaseFilter
from utils import get_all_columns, get_all_rows, sort_time_strings, read_categories_dataframe
from datetime import datetime
import numpy as np

class SalesHistoryDisplayPipeline:
    ignore_names = ['*categories']
    
    def __init__(self):
        self.transformed_data = None

    def __call__(self, data):
        self.transformed_data = self.transform(data)
        self.display(self.transformed_data)
        

    def transform(self, data):
        return data
    
    def _extract_unit(self, name):
        symbols = ["#", "$", "%"]
        for s in symbols:
            if s in name:
                return "(" + s + ")"
        
        return ""
    
    def display(self, data):
        for name, df in data.items():
            fig = go.Figure()
            for column in df.columns: 
                fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

            fig.update_layout(
                title=dict(text=name, font=dict(size=20)),
                xaxis_title='Date',
                yaxis_title=f'Amount {self._extract_unit(name)}',
                template='plotly_dark',
            )
            
            st.plotly_chart(fig, use_container_width=True)

def display_time_series(dataframe_dict, selected_data):
        st.title(f"{selected_data} Time Series")
        all_time_rows = sort_time_strings(list(get_all_rows(dataframe_dict)))
        all_time_columns = list(get_all_columns(dataframe_dict))
        all_time_names = sorted([n for n in dataframe_dict.keys() if n not in SalesHistoryDisplayPipeline.ignore_names])


        all_time_rows_dt = [
            datetime.strptime(row, "%m.%y") for row in all_time_rows
        ]


        col1, col2 = st.columns([2, 8]) 

        if "time_series_selected_name" not in st.session_state or st.session_state.time_series_selected_name not in dataframe_dict.keys():
            st.session_state.time_series_selected_name = all_time_names[0] 

        with col1:
            selected_name = st.radio(
                "Categories",
                options=all_time_names,
                index=all_time_names.index(st.session_state.time_series_selected_name), 
                key="time_series_radio"
        )

        with col2:
            # Buttons for each column
            category_df = read_categories_dataframe()
            category_df["ALL ITEMS"] = np.nan
            category_df = category_df.reindex(sorted(category_df.columns), axis=1)
            
            if selected_data == "Per-Product Data":
                st.write("Quick-select products")
                cols = st.columns(len(category_df.columns)) 

            if "time_series_multi" not in st.session_state:
                st.session_state.time_series_multi = [] 

            if selected_data == "Per-Product Data":
                for col, column_name in zip(cols, category_df.columns):
                    with col:
                        if st.button(column_name, key=f"time_series_multi_{column_name}"):
                            non_nan_values = category_df[column_name].dropna().tolist()
                            st.session_state.time_series_multi = [val for val in non_nan_values]


            if set(st.session_state.time_series_multi) <= set(all_time_columns):
                default=st.session_state.time_series_multi
            else:
                default=[]

            selected_columns = st.multiselect(
                "Products",
                options=all_time_columns, 
                default=default,
                key="time_series_multi",
            )

            start_time_str, end_time_str = st.select_slider(
                "Time Range",
                options=[row.strftime("%-m/%y") for row in all_time_rows_dt], 
                value=(all_time_rows_dt[0].strftime("%-m/%y"), all_time_rows_dt[-1].strftime("%-m/%y")),
                key="time_series_slider"
            )

            start_time = datetime.strptime(start_time_str, "%m/%y")
            end_time = datetime.strptime(end_time_str, "%m/%y")

            selected_rows = [
                row.strftime("%-m.%y") for row in all_time_rows_dt if start_time <= row <= end_time
            ]

            shp = SalesHistoryDisplayPipeline()
            sales_filter = BaseFilter(shp)
            sales_filter.filter(dataframe_dict, selected_columns, selected_rows, [selected_name])