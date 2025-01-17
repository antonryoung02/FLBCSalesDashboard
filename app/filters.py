import streamlit as st
from datetime import datetime
from app.config import DATE_FILE_MONTH_FORMAT

class BaseFilter:
    def __init__(self, categories_dataframe):
        self.categories_dataframe = categories_dataframe

    def filter_dataframe(self, dataframe_dict:dict, columns:list, index:list, names:list):
        filtered_dict = dataframe_dict.copy()   
        if names:
            filtered_dict = {name:df for name, df in dataframe_dict.items() if name in names}
        if columns:
            filtered_dict = {name:df[columns] for name, df in filtered_dict.items()}
        if index:
            filtered_dict = {name:df[df.index.isin(index)] for name, df in filtered_dict.items()}
        return filtered_dict

    def display_quick_select_columns(self, selected_data:str, key:str):
        if selected_data == "Per-Product Data":
            st.write("Quick-select products")
            cols = st.columns(len(self.categories_dataframe.df.columns)) 

        if key not in st.session_state:
            st.session_state[key] = [] 

        if selected_data == "Per-Product Data":
            for col, column_name in zip(cols, self.categories_dataframe.df.columns):
                with col:
                    if st.button(column_name, key=f"{key}_{column_name}"):
                        st.session_state[key] = self.categories_dataframe.get_values_for_column(column_name)

    def get_selected_dataframe(self, all_dataframe_names:list, key:str) -> list:
        selected_name = st.radio(
            "Categories",
            options=all_dataframe_names,
            index=all_dataframe_names.index(st.session_state[key] if key in st.session_state else all_dataframe_names[0]), 
            key=key
        ) 
        return [selected_name]

    def get_selected_columns(self, all_columns:list, key:str) -> list:
        if set(st.session_state[key]) <= set(all_columns):
            default=st.session_state[key]
        else:
            default=[]

        selected_columns = st.multiselect(
            "Products",
            options=all_columns, 
            default=default,
            key=key,
        )
        return selected_columns
        
    def get_selected_rows(self, all_rows:list, key:str) -> list:

        all_time_rows_dt = [
        datetime.strptime(row, "%m.%y") for row in all_rows
        ]
        start_time_str, end_time_str = st.select_slider(
            "Time Range",
            options=[row.strftime(f"{DATE_FILE_MONTH_FORMAT}/%y") for row in all_time_rows_dt], 
            value=(all_time_rows_dt[0].strftime(f"{DATE_FILE_MONTH_FORMAT}/%y"), all_time_rows_dt[-1].strftime(f"{DATE_FILE_MONTH_FORMAT}/%y")),
            key=key
        )

        start_time = datetime.strptime(start_time_str, "%m/%y")
        end_time = datetime.strptime(end_time_str, "%m/%y")

        selected_rows = [
            row.strftime(f"{DATE_FILE_MONTH_FORMAT}.%y") for row in all_time_rows_dt if start_time <= row <= end_time
        ]
        return selected_rows

