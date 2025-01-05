import pandas as pd
import os 
from app.utils import read_categories_dataframe

class TimeSeriesCumulativePipeline:

    mean_columns = ['*menu Price $', 'FC%', '*cm category', '*CM $', '*FC $']
    columns_to_ignore = ['*categories']

    def transform(self, dataframe_dict):
        cumulative_dataframe_dict = {}
        for name, df in dataframe_dict.items():
            if name not in TimeSeriesCumulativePipeline.columns_to_ignore:
                cumulative_dataframe_dict[name] = self._create_cumulative_dataframe(df, name)
        
        return cumulative_dataframe_dict
            
    def _create_cumulative_dataframe(self, df, name) -> pd.DataFrame:
        categories_df = read_categories_dataframe()
        cumulative_df = pd.DataFrame()
        for c in categories_df.columns:
            categories = categories_df[c].dropna().tolist()
            categories = [c for c in categories if c in df.columns]
            cumulative_df[c] = df[categories].aggregate('mean' if name in TimeSeriesCumulativePipeline.mean_columns else 'sum', axis=1)
        
        return cumulative_df
