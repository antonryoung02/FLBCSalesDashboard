import plotly.graph_objects as go
import streamlit as st
from typing import Dict
import pandas as pd

def display_cumulative(data:Dict[str, pd.DataFrame]) -> None:
    """Displays a stacked bar chart of all products in the dataframe

    Args:
        data (dict): 
    """
    for name, df in data.items():
        fig = go.Figure()

        for column in df.columns: 
            fig.add_trace(go.Bar(
                x=df.index, 
                y=df[column],
                name=column 
            ))

        fig.update_layout(
            title=dict(text=name, font=dict(size=20)),
            xaxis_title='Date',
            yaxis_title=f'Amount {_extract_unit(name)}',
            barmode='stack',
            template='plotly_white',
        )
        
        st.plotly_chart(fig, use_container_width=True)

def _extract_unit(name:str) -> str:
    symbols = ["#", "$", "%"]
    for s in symbols:
        if s in name:
            return "(" + s + ")"
    return ""