import pytest
import pandas as pd
from app.base_filter import BaseFilter

def test_filter_rows(base_filter, mock_dataframe_dict):
    included_rows = ['1.24', '2.24']
    res = base_filter.filter_dataframe(mock_dataframe_dict, columns=[], index=included_rows, names=[])
    for df in res.values():
        pd.testing.assert_index_equal(df.index, pd.Index(included_rows))    

def test_filter_columns(base_filter, mock_dataframe_dict):
    included_cols = ['p1']
    res = base_filter.filter_dataframe(mock_dataframe_dict, columns=included_cols, index=[], names=[])
    for df in res.values():
        pd.testing.assert_index_equal(df.columns, pd.Index(included_cols))     

def test_filter_dataframes(base_filter, mock_dataframe_dict):
    included_dataframes = ['feature2', 'feature3']
    res = base_filter.filter_dataframe(mock_dataframe_dict, columns=[], index=[], names=included_dataframes)
    assert list(res) == included_dataframes 

@pytest.fixture
def mock_dataframe_dict():
    return {
        "feature1": pd.DataFrame({
            "p1": [1.0,2.0,3.0],
            "p2": [1.0,1.0,1.0]
        }, index=['1.24', '2.24', '3.24']),
        "feature2": pd.DataFrame({
            "p1": [1.0,2.0,3.0],
            "p2": [1.0,1.0,1.0]
        }, index=['1.24','2.24', '3.24']),
        "feature3": pd.DataFrame({
            "p1": [1.0,2.0,3.0],
            "p2": [1.0,1.0,1.0]
        }, index=['1.24', '2.24', '3.24']),
    }

@pytest.fixture
def base_filter():
    return BaseFilter(categories={})