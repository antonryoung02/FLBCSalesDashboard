import pandas as pd
import numpy as np

def remove_invalid_rows(df:pd.DataFrame) -> None:
    threshold = (len(df.columns) / 2) - 1
    df.drop(index=df[df.notna().sum(axis=1) <= threshold].index, inplace=True)

def remove_invalid_columns(df:pd.DataFrame) -> None:
    unnamed_cols = [col for col in df.columns if 'unnamed' in col.lower()]
    df.drop(columns=unnamed_cols, inplace=True)
    df.drop(columns=[col for col in df.columns if df[col].apply(lambda x: isinstance(x, str)).any()], inplace=True)

def convert_columns_to_float64(df:pd.DataFrame) -> None:
    int_cols = df.select_dtypes(include=['int','object']).columns
    df[int_cols] = df[int_cols].astype('float64')

def insert_null_rows(df:pd.DataFrame, index:list) -> pd.DataFrame:
    if not index:
        return df
    inserted_rows_df = pd.DataFrame([[np.nan for _ in df.columns] for _ in index], index=index, columns=df.columns)
    full_df = pd.concat([df, inserted_rows_df], axis=0)
    return full_df

def insert_null_columns(df:pd.DataFrame, columns:list) -> None:
    for c in columns:
        df[c] = np.nan