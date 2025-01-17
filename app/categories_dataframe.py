import numpy as np

class CategoriesDataframe:
    def __init__(self, df):
        self.df = df
        self.df['ALL ITEMS'] = np.nan
        self.df = self.df.reindex(sorted(self.df.columns), axis=1)

    def get_values_for_column(self, column_name):
        return self.df[column_name].dropna().tolist()

    def get_columns(self):
        return self.df.columns.drop(["ALL ITEMS"])


