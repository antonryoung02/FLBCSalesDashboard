import pandas as pd
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_SHEET = "CONFIG"
FILENAME = "MENU ENGINEERING FLBC PBHS and CELLAR.xlsx"

class TimeSeriesCumulativePipeline:

    mean_columns = ['*menu Price $', 'FC%', '*cm category', '*CM $', '*FC $']
    columns_to_drop = ['*categories']

    def __init__(self):
        pass

    def _get_categories_df(self):
        return pd.read_excel(os.path.join(BASE_DIR, FILENAME), sheet_name=CONFIG_SHEET)



    def transform(self, dataframe_dict):
        cumulative_dataframe_dict = {}
        categories_df = self._get_categories_df()
        for name, df in dataframe_dict.items():
            if name in TimeSeriesCumulativePipeline.columns_to_drop:
                continue
            if df.applymap(lambda x: isinstance(x, str)).any().any(): #contains strings. could warn here?
                continue
            
            cumulative_df = pd.DataFrame()
            for c in categories_df.columns:
                categories = categories_df[c].dropna().tolist()
                categories = [c for c in categories if c in df.columns]
                cumulative_df[c] = df[categories].aggregate('mean' if name in TimeSeriesCumulativePipeline.mean_columns else 'sum', axis=1)
            
            cumulative_dataframe_dict[name] = cumulative_df
        
        return cumulative_dataframe_dict

   
