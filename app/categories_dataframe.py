import pandas as pd
from app.config import CONFIG_SHEET_NAME, DATA_FILENAME, BASE_DIR_PATH
import os
import numpy as np

class CategoriesDataframe:
    def __init__(self):
        self.df = pd.read_excel(os.path.join(BASE_DIR_PATH, DATA_FILENAME), sheet_name=CONFIG_SHEET_NAME)
        self.df['ALL ITEMS'] = np.nan
        self.df = self.df.reindex(sorted(self.df.columns), axis=1)

    def get_values_for_column(self, column_name):
        return self.df[column_name].dropna().tolist()

    def get_columns(self):
        return self.df.columns
    

categories_dataframe = CategoriesDataframe()
    # What are the operations I do on this dataframe. What ordering does it expect or need.
    # Upon read, I set ALL ITEMS to NAN/empty list
    # It doesn't make sense to keep it in a dataframe, it should be a dictionary
    # Would no longer need non_nan_values




