import streamlit as st
from datetime import datetime
from app.config import DATE_FILE_MONTH_FORMAT

class BaseFilter:
    def __init__(self, categories:dict):
        self.categories = categories

    def filter_dataframe(self, dataframe_dict:dict, columns:list, index:list, names:list) -> dict:
        filtered_dict = dataframe_dict
        if names:
            filtered_dict = {name:df for name, df in dataframe_dict.items() if name in names}
        if columns:
            filtered_dict = {name:df[columns] for name, df in filtered_dict.items()}
        if index:
            filtered_dict = {name:df[df.index.isin(index)] for name, df in filtered_dict.items()}
        return filtered_dict

    def display_quick_select_columns(self, selected_data:str, key:str) -> None:
        if selected_data == "Per-Product Data":
            st.write("Quick-select products")
            cols = st.columns(len(self.categories.keys())) 

        if key not in st.session_state:
            st.session_state[key] = [] 

        if selected_data == "Per-Product Data":
            for col, column_name in zip(cols, sorted(self.categories.keys())):
                with col:
                    if st.button(column_name, key=f"{key}_{column_name}"):
                        st.session_state[key] = self.categories[column_name]

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

        self._handle_undefined_keys(all_columns, key)

        selected_columns = st.multiselect(
            "Products",
            options=all_columns, 
            default=default,
            key=key,
        )
        return selected_columns

    def _handle_undefined_keys(self, all_columns:list, key:str) -> None:
        undefined_keys = set(st.session_state[key]).difference(set(all_columns))
        if len(undefined_keys) > 0:
            st.error(f"There are typos in the CONFIG excel spreadsheet. The products {undefined_keys} are not being displayed because they do not exist in the sales data.")
        st.session_state[key] = list(set(st.session_state[key]).difference(undefined_keys))
        
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

