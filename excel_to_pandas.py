import pandas as pd
import numpy as np
from utils import get_all_columns, get_all_rows

class ExcelToPandasPipeline:
    """The parent transformation. Cleans empty rows/cols and inserts all col/rows with null values to standardize output shape amongst dataframe dicts. 
    """

    def transform(self, dataframe_dict:dict, inplace:bool=True) -> dict | None:
        if not inplace:
            dataframe_dict = {name: df.copy() for name, df in dataframe_dict.items()}
        
        for name, df in dataframe_dict.items():
            self._remove_invalid_rows(df)
            self._remove_invalid_columns(df)

        all_rows = get_all_rows(dataframe_dict)
        all_columns = get_all_columns(dataframe_dict)
        for name, df in dataframe_dict.items():
            df = self._insert_missing_rows(df, all_rows)
            dataframe_dict[name] = df
            self._insert_missing_columns(df, all_columns)
            self._convert_cols_to_float64(df)

            df.sort_index(axis=0, inplace=True)
            df.sort_index(axis=1, inplace=True)

        if not inplace:
            return dataframe_dict
        
    def _convert_cols_to_float64(self, df):
        int_cols = df.select_dtypes(include=['int','object']).columns
        df[int_cols] = df[int_cols].astype('float64')

    def _remove_invalid_rows(self, df:pd.DataFrame) -> None:
        """Removes the first row (second header) and all null rows

        Args:
            df (pd.DataFrame):
        """
        threshold = (len(df.columns) / 2) - 1
        df.drop(index=df[df.notna().sum(axis=1) <= threshold].index, inplace=True)

    def _remove_invalid_columns(self, df:pd.DataFrame) -> None:
        """Removes all null columns (contains 'unnamed' from read_excel)

        Args:
            df (pd.DataFrame):
        """
        def get_null_columns(df:pd.DataFrame) -> list:
            return [col for col in df.columns if 'unnamed' in col.lower()]
        
        unnamed_cols = get_null_columns(df) 
        df.drop(columns=unnamed_cols, inplace=True)
        df.drop(columns=[col for col in df.columns if df[col].apply(lambda x: isinstance(x, str)).any()], inplace=True)


    def _insert_missing_rows(self, df:pd.DataFrame, all_rows:set) -> pd.DataFrame:
        """Adds null rows for products that aren't reference in the dataframe

        Args:
            df (pd.DataFrame):
            all_rows (set):

        Returns:
            pd.DataFrame:
        """
        def get_missing_rows(df, all_rows) -> set:
            diff = all_rows.difference(set(df.index))
            return diff
        missing_rows = get_missing_rows(df, all_rows)

        missing_df = pd.DataFrame([[np.nan for _ in df.columns] for _ in missing_rows], index=list(missing_rows), columns=df.columns)
        full_df = pd.concat([df, missing_df], axis=0)
        return full_df

    def _insert_missing_columns(self, df:pd.DataFrame, all_columns:set) -> None:
        """Adds null columns for product features that aren't referenced in the dataframe

        Args:
            df (pd.DataFrame):
            all_columns (set):

        Returns:
            pd.DataFrame:
        """

        def get_missing_columns(df_columns, all_columns) -> set:
            diff = all_columns.difference(set(df_columns))
            return diff
        
        missing_columns = get_missing_columns(df.columns, all_columns)
        for c in missing_columns:
            df[c] = np.nan



