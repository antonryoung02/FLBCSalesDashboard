import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from app.filters import BaseFilter
from app.utils import get_all_columns, get_all_rows, sort_time_strings
from datetime import datetime
import numpy as np
from categories_dataframe import categories_dataframe 
from app.config import DATE_FILE_MONTH_FORMAT

class DisplayTrendsPipeline:
    ignore_names = ['*categories']

    def __init__(self):
        self.transformed_data = None

    def __call__(self, data):
        self.transformed_data = self.transform(data)
        self.display(self.transformed_data)
        

    def transform(self, data):
        trends_data = {}
        for name, df in data.items():
            before = df.iloc[0]
            after = df.iloc[-1]
            
            valid_before = before.replace(0, np.nan) 
            pct_changes = ((after - valid_before) / valid_before) * 100
            
            avg_pct_change = pct_changes.mean()
            pct_changes.fillna(0, inplace=True) 
            
            pct_changes["Average"] = avg_pct_change  
            trend_df = pd.DataFrame([pct_changes.values], columns=pct_changes.index)
            
            sorted_columns = trend_df.iloc[0].sort_values(ascending=False).index
            trend_df = trend_df[sorted_columns]  
            
            trends_data[name] = trend_df  
        return trends_data

    def display(self, data):
        for name, df in data.items():
            fig = go.Figure()

            x = df.columns 
            y = df.iloc[0].values  

            bar_colors = [
                "orange" if col == "Average" else "blue" for col in x
            ]

            fig.add_trace(go.Bar(
                x=x,
                y=y,
                name=f"Percent Changes for {name}",
                marker_color=bar_colors 
            ))

            fig.update_layout(
                title=dict(text=f"Percent Change for {name}", font=dict(size=20)),
                xaxis_title="Items",
                yaxis_title="Percent Change (%)",
                template="plotly_white",
            )

            st.plotly_chart(fig, use_container_width=True)

def display_trends(dataframe_dict, selected_data):
    st.title(f"{selected_data} Trends")
    all_time_rows = sort_time_strings(list(get_all_rows(dataframe_dict)))
    all_time_columns = list(get_all_columns(dataframe_dict))
    all_time_names = sorted([n for n in dataframe_dict.keys() if n not in DisplayTrendsPipeline.ignore_names])


    all_time_rows_dt = [
        datetime.strptime(row, "%m.%y") for row in all_time_rows
    ]

    col1, col2 = st.columns([2, 8]) 

    if "cumulative_selected_name" not in st.session_state or st.session_state.cumulative_selected_name not in dataframe_dict.keys():
        st.session_state.cumulative_selected_name = all_time_names[0] 

    with col1:
        selected_name = st.radio(
            "Categories",
            options=all_time_names,
            index=all_time_names.index(st.session_state.cumulative_selected_name),
            key="cumulative_radio"
    )

    with col2:
        if selected_data == "Per-Product Data":
            st.write("Quick-select products")
            cols = st.columns(len(categories_dataframe.get_columns())) 

        if "cumulative_multi" not in st.session_state:
            st.session_state.cumulative_multi = [] 

        if selected_data == "Per-Product Data":
            for col, column_name in zip(cols, categories_dataframe.get_columns()):
                with col:
                    if st.button(column_name, key=f"cumulative_{column_name}"):
                        st.session_state.cumulative_multi = categories_dataframe.get_values_for_column(column_name)
        
        if set(st.session_state.cumulative_multi) <= set(all_time_columns):
           default=st.session_state.cumulative_multi 
        else:
            default=[]

        selected_columns = st.multiselect(
            "Products",
            options=all_time_columns,
            default=default,    
            key="cumulative_multi",
        )

        start_time_str, end_time_str = st.select_slider(
            "Time Range",
            options=[row.strftime(f"{DATE_FILE_MONTH_FORMAT}/%y") for row in all_time_rows_dt], 
            value=(all_time_rows_dt[0].strftime(f"{DATE_FILE_MONTH_FORMAT}/%y"), all_time_rows_dt[-1].strftime(f"{DATE_FILE_MONTH_FORMAT}/%y")),
            key="cumulative_slider"
        )

        start_time = datetime.strptime(start_time_str, "%m/%y")
        end_time = datetime.strptime(end_time_str, "%m/%y")

        selected_rows = [
            row.strftime(f"{DATE_FILE_MONTH_FORMAT}.%y") for row in all_time_rows_dt if start_time <= row <= end_time
        ]

        dtp = DisplayTrendsPipeline()
        sales_filter = BaseFilter(dtp)
        sales_filter.filter(dataframe_dict, selected_columns, selected_rows, [selected_name])
