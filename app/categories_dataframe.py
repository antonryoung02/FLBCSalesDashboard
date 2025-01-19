import numpy as np
import pandas as pd

class CategoriesDataframe:
    def __init__(self, df:pd.DataFrame):
        self.df = df
        self.df['ALL ITEMS'] = np.nan
        self.df = self.df.reindex(sorted(self.df.columns), axis=1)

    def get_values_for_column(self, column_name) -> list:
        return self.df[column_name].dropna().tolist()

    def get_columns(self) -> list:
        return self.df.columns.drop(["ALL ITEMS"]).tolist()


