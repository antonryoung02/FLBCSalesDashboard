import pandas as pd

class TimeSeriesPipeline:
    def __init__(self):
        pass

    def _get_columns(self, dataframe_dict):
        column_set = set()
        for name, df in dataframe_dict.items():
            column_set = column_set.union(df.columns)
        return sorted(list(column_set))
    
    def _get_all_rows(self, dataframe_dict):
        index_set = set()
        for name, df in dataframe_dict.items():
            index_set = index_set.union(df.index)
        return sorted(list(index_set))
    
    def _convert_cols_to_float64(self, df):
        int_cols = df.select_dtypes(include=['int','object']).columns
        df[int_cols] = df[int_cols].astype('float64')


    def transform(self, dataframe_dict):
        columns = self._get_columns(dataframe_dict)
        rows = self._get_all_rows(dataframe_dict)
        transformed_data = {f:pd.DataFrame() for f in columns}
        for f in columns:
            cumu_df = pd.DataFrame() 
            for name, df in dataframe_dict.items():
                cumu_df = pd.concat([cumu_df, df[f]], axis=1)

            cumu_df = cumu_df.T
            cumu_df.index = [name for name, _ in dataframe_dict.items()]
            cumu_df.columns = rows
            self._convert_cols_to_float64(cumu_df)
            transformed_data[f] = cumu_df

        return transformed_data
   
