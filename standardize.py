import pandas as pd
import numpy as np
from utils import get_all_columns, get_all_rows, convert_columns_to_float64

class StandardizePipeline:
    """
    The parent transformation. Cleans empty rows/cols and inserts all col/rows with null values to standardize output shape amongst dataframe dicts. 
    """

    def transform(self, dataframe_dict:dict, inplace:bool=False) -> dict | None:
        """Normalizes dataframes in the dict to be of same shape, with same columns and index

        Args:
            dataframe_dict (dict): Raw dataframe dict read from extract
            inplace (bool, optional): Whether to operate on a copy of the input. Defaults to False.

        Returns:
            dict | None:
        """
        if not inplace:
            dataframe_dict = {name: df.copy() for name, df in dataframe_dict.items()}
        
        for name, df in dataframe_dict.items():
            self._remove_invalid_rows(df)
            self._remove_invalid_columns(df)

        all_rows = get_all_rows(dataframe_dict)
        all_columns = get_all_columns(dataframe_dict)
        for name, df in dataframe_dict.items():
            dataframe_dict[name] = self._standardize_dataframe(df, all_rows, all_columns)

        if not inplace:
            return dataframe_dict
    
    def _remove_invalid_rows(self, df:pd.DataFrame) -> None:
        threshold = (len(df.columns) / 2) - 1
        df.drop(index=df[df.notna().sum(axis=1) <= threshold].index, inplace=True)

    def _remove_invalid_columns(self, df:pd.DataFrame) -> None:
        unnamed_cols = [col for col in df.columns if 'unnamed' in col.lower()]
        df.drop(columns=unnamed_cols, inplace=True)
        df.drop(columns=[col for col in df.columns if df[col].apply(lambda x: isinstance(x, str)).any()], inplace=True)

    def _standardize_dataframe(self, df, all_rows, all_columns) -> pd.DataFrame:
        df = self._insert_missing_rows(df, all_rows)
        self._insert_missing_columns(df, all_columns)
        convert_columns_to_float64(df)
        df.sort_index(axis=0, inplace=True)
        df.sort_index(axis=1, inplace=True)

        return df
    
    def _insert_missing_rows(self, df:pd.DataFrame, all_rows:set) -> pd.DataFrame:
        missing_rows = all_rows.difference(set(df.index))
        if not missing_rows:
            return df
        
        missing_df = pd.DataFrame([[np.nan for _ in df.columns] for _ in missing_rows], index=list(missing_rows), columns=df.columns)
        full_df = pd.concat([df, missing_df], axis=0)
        return full_df

    def _insert_missing_columns(self, df:pd.DataFrame, all_columns:set) -> None: 
        missing_columns = all_columns.difference(set(df.columns))
        for c in missing_columns:
            df[c] = np.nan