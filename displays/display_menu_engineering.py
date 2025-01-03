import plotly.graph_objects as go
import streamlit as st
from utils import get_all_rows, sort_time_strings, read_categories_dataframe
from filters import BaseFilter

def display_menu_engineering(dataframe_dict):
    
    st.title("Menu Engineering Matrix")
    col1, col2 = st.columns([2, 8]) 

    with col2:
        category_df = read_categories_dataframe()

        category_df = category_df.reindex(sorted(category_df.columns), axis=1)

        selected_indices = st.multiselect(
            "Products",
            options=category_df.columns, 
            key="menu_series_multi",
        )

        selected_products = []
        for i in selected_indices:
            non_nan_values = category_df[i].dropna().tolist()
            selected_products += [val for val in non_nan_values]

        all_time_rows = sort_time_strings(list(dataframe_dict.keys()))
        selected_row = st.select_slider(
        "Month",
        options=all_time_rows,  
        value=all_time_rows[-1],
        )


        medp = MenuEngineeringDisplayPipeline()
        medp.compute_averages(dataframe_dict[selected_row])
        menu_filter = BaseFilter(medp)
        menu_filter.filter(dataframe_dict, columns=[], index=selected_products, names=[selected_row])



class MenuEngineeringDisplayPipeline:
    
    def __init__(self):
        self.transformed_data = None
        self.y = 'mm%' 
        self.x = '*cm category'

    def __call__(self, data):
        self.transformed_data = self.transform(data)
        self.display(self.transformed_data)

    def compute_averages(self, df):
        self.x_mean = df[self.x].mean()
        self.y_mean = df[self.y].mean()
        self.x_min = df[self.x].min()
        self.x_max = df[self.x].max() 
        self.y_min = df[self.y].min()
        self.y_max = df[self.y].max()

    def transform(self, data):
        for name, df in data.items():
            data[name] = df[[self.x, self.y]]
        return data
    
    def display(self, dataframe_dict):
 
        category_df = read_categories_dataframe()
        category_df = category_df.reindex(sorted(category_df.columns), axis=1)

        for name, df in dataframe_dict.items():
            fig = go.Figure()

            for category in category_df.columns:
                category_items = category_df[category].dropna().values
                category_indices = [index for index in df.index if index in category_items]

                filtered_df = df.loc[category_indices]

                fig.add_trace(go.Scatter(
                    y=filtered_df[self.y], 
                    x=filtered_df[self.x], 
                    mode='markers', 
                    name=category, 
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
