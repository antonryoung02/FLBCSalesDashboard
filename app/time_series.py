import pandas as pd
from app.utils import get_all_columns, get_all_rows, convert_columns_to_float64
import app.dataframe_operations as dfo
class TimeSeriesPipeline:

    def transform(self, dataframe_dict):
        columns = sorted(list(get_all_columns(dataframe_dict)))
        rows = sorted(list(get_all_rows(dataframe_dict)))
        transformed_data = {}

        for f in columns:
            transformed_data[f] = self._create_dataframe_for_feature(f, rows, dataframe_dict)
        
        return transformed_data

    def _create_dataframe_for_feature(self, f:str, rows:list, dataframe_dict:dict) -> pd.DataFrame:
        feature_df = pd.DataFrame() 
        for df in dataframe_dict.values():
            feature_df = pd.concat([feature_df, df[f]], axis=1)

        feature_df = feature_df.T
        feature_df.index = [name for name in dataframe_dict.keys()]
        feature_df.columns = rows
        dfo.convert_columns_to_float64(feature_df)

        return feature_df
    