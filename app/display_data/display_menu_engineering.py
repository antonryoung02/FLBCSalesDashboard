import plotly.graph_objects as go
import streamlit as st
from app.utils import sort_time_strings
from app.base_filter import BaseFilter
import pandas as pd
from typing import Dict

def display_menu_engineering(dataframe_dict:Dict[str, pd.DataFrame], categories:Dict[str, list]) -> None:
    
    st.title("Menu Engineering Matrix")
    col1, col2 = st.columns([2, 8]) 

    with col2:

        selected_indices = st.multiselect(
            "Products",
            options=categories.keys(), 
            key="menu_series_multi",
        )

        selected_products = []
        for i in selected_indices:
            non_nan_values = categories[i]
            selected_products += non_nan_values

        all_time_rows = sort_time_strings(list(dataframe_dict))
        selected_row = st.select_slider(
        "Month",
        options=all_time_rows,  
        value=all_time_rows[-1],
        )

        medp = MenuEngineeringDisplayPipeline(categories)
        medp.compute_averages(dataframe_dict[selected_row])
        filter = BaseFilter(categories)
        filtered_dataframe = filter.filter_dataframe(dataframe_dict, columns=[], index=selected_products, names=[selected_row])
        medp(filtered_dataframe)



class MenuEngineeringDisplayPipeline:
    
    def __init__(self, categories:Dict[str, list]):
        self.transformed_data = None
        self.y = 'mm%' 
        self.x = '*cm category'
        self.categories = categories

    def __call__(self, data:dict) -> None:
        self.transformed_data = self.transform(data)
        self.display(self.transformed_data)

    def compute_averages(self, df:pd.DataFrame) -> None:
        self.x_mean = df[self.x].mean()
        self.y_mean = df[self.y].mean()
        self.x_min = df[self.x].min()
        self.x_max = df[self.x].max() 
        self.y_min = df[self.y].min()
        self.y_max = df[self.y].max()

    def transform(self, data:Dict[str, pd.DataFrame]) -> dict:
        for name, df in data.items():
            data[name] = df[[self.x, self.y]]
        return data
    
    def display(self, dataframe_dict:Dict[str, pd.DataFrame]) -> None:

        for name, df in dataframe_dict.items():
            fig = go.Figure()

            for c in self.categories:
                category_items = self.categories[c]
                category_indices = [index for index in df.index if index in category_items]

                filtered_df = df.loc[category_indices]

                fig.add_trace(go.Scatter(
                    y=filtered_df[self.y], 
                    x=filtered_df[self.x], 
                    mode='markers', 
                    name=c, 
                    text=filtered_df.index, 
                    marker=dict(size=10),
                    hovertemplate="<b>Index</b>: %{text}<br><b>Profitability</b>: %{x}<br><b>Popularity</b>: %{y}<extra></extra>"
                ))

            fig.add_shape(
                type="rect",
                x0=self.x_min, x1=self.x_mean,
                y0=self.y_min, y1=self.y_mean,
                fillcolor="rgba(255, 0, 0, 0.125)",
                line=dict(width=0)
            )
            fig.add_shape(
                type="rect",
                x0=self.x_mean, x1=self.x_max,
                y0=self.y_min, y1=self.y_mean,
                fillcolor="rgba(255, 255, 0, 0.125)", 
                line=dict(width=0)
            )
            fig.add_shape(
                type="rect",
                x0=self.x_min, x1=self.x_mean,
                y0=self.y_mean, y1=self.y_max,
                fillcolor="rgba(255, 165, 0, 0.125)",
                line=dict(width=0)
            )
            fig.add_shape(
                type="rect",
                x0=self.x_mean, x1=self.x_max,
                y0=self.y_mean, y1=self.y_max,
                fillcolor="rgba(0, 255, 0, 0.125)", 
                line=dict(width=0)
            )

            fig.update_layout(
                height=800,
                xaxis_title=f'Profitability: ({self.x})',
                yaxis_title=f'Popularity: ({self.y})',
                template='plotly_white',
            )

            st.plotly_chart(fig, use_container_width=True)
