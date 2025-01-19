import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np

def display_trends(data:dict) -> None:
    transformed_data = _transform(data)
    for name, df in transformed_data.items():
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
    
def _transform(data:dict) -> dict:
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
