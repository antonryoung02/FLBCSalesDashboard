import pytest
import pandas as pd
from app.utils import get_all_columns, get_all_rows, sort_time_strings, sheet_is_valid

def test_get_all_rows(mock_dataframe_dict):
    assert get_all_rows(mock_dataframe_dict) == {"row1", "row4", "row5", "row6", "row7", "row8", "row9"}

def test_get_all_columns(mock_dataframe_dict):
    assert get_all_columns(mock_dataframe_dict) == {"col1", "col2", "col5", "col8"}

def test_sort_time_strings(time_strings_in_expected_format):
    assert sort_time_strings(time_strings_in_expected_format["input"]) == time_strings_in_expected_format["solution"]

def test_sheet_is_valid(valid_dataframe, time_strings):
    for i in range(len(time_strings['input'])):
        assert sheet_is_valid(time_strings["input"][i], valid_dataframe) == time_strings["solution"][i]

@pytest.fixture
def time_strings_in_expected_format():
    return {
        "input": ["11.24", "1.24", "1.25", "12.25", "2.25", "6.24"],
        "solution": ["1.24", "6.24", "11.24", "1.25", "2.25", "12.25"],
    }

@pytest.fixture
def valid_dataframe():
    return pd.DataFrame({
        "col1": [1,1,1],
        "col2": [2,2,2],
    })

@pytest.fixture
def time_strings():
    return {
        "input": ["1.24", "01.24", "11.24", "1.2024"],
        "solution": [True, False, True, False]
        }

@pytest.fixture
def mock_dataframe_dict():
    return {
        "1.24": pd.DataFrame({
            "col1": [1,2,3,4],
            "col2": [3,4,5,6],
            "col5": [5,6,7,8],
        }, index=['row1', 'row4', 'row6', 'row7']),
        "2.24": pd.DataFrame({
            "col1": [1,2,3,4],
            "col8":[6,7,8,9],
            "col2":[1,2,3,4]
        }, index=['row1', 'row5', 'row8', 'row9'])
    }