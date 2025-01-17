import plotly.graph_objects as go
import streamlit as st


def display_time_series(data):
    transformed_data = _transform(data)
    _display(transformed_data)
    

def _transform(data):
    return data

def _extract_unit(name):
    symbols = ["#", "$", "%"]
    for s in symbols:
        if s in name:
            return "(" + s + ")"
    
    return ""

def _display(data):
    for name, df in data.items():
        fig = go.Figure()
        for column in df.columns: 
            fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

        fig.update_layout(
            title=dict(text=name, font=dict(size=20)),
            xaxis_title='Date',
            yaxis_title=f'Amount {_extract_unit(name)}',
            template='plotly_dark',
        )
        
        st.plotly_chart(fig, use_container_width=True)