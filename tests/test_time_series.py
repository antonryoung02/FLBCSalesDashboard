import pytest
import pandas as pd
import numpy as np
from app.transform_data.time_series_transform import time_series_transform

def test_transform(mock_df_dict):
    res = time_series_transform(mock_df_dict["input"], features_to_ignore=['ignorecol']) 
    for key in mock_df_dict["solution"]:
        pd.testing.assert_frame_equal(res[key], mock_df_dict["solution"][key])

def test_transform_ignores_cols(mock_df_dict_with_ignorecol):
    res = time_series_transform(mock_df_dict_with_ignorecol, features_to_ignore=['ignorecol']) 
    assert 'f1' in res
    assert 'f2' in res
    assert 'ignorecol' not in res

@pytest.fixture
def mock_df_dict_with_ignorecol():
    return {
        "1.24": pd.DataFrame({
            "f1":[np.nan,np.nan],
            "ignorecol":[1,2],
            "f2": [1,2]
        }, index=['p1', 'p2'])
    }

@pytest.fixture
def mock_df_dict():
    return {
        "input":{
            "1.24":pd.DataFrame({
                "f1":[1,2,3],
                "f2":[np.nan, np.nan, np.nan],
                "f3": [2,2,2]
            }, index=["product1", "product2", "product3"]),
            "2.24":pd.DataFrame({
                "f1":[1,2,3],
                "f2":[np.nan, np.nan, np.nan],
                "f3": [2,2,2]
            }, index=["product1", "product2", "product3"]),
            "3.24":pd.DataFrame({
                "f1":[1,2,3],
                "f2":[9,8,7],
                "f3": [2,2,2]
            }, index=["product1", "product2", "product3"]),
        },
        "solution":{
            "f1":pd.DataFrame({
                "product1":[1.0,1.0,1.0],
                "product2":[2.0,2.0,2.0],
                "product3":[3.0,3.0,3.0]
            }, index=['1.24', '2.24', '3.24']),
            "f2":pd.DataFrame({
                "product1":[np.nan,np.nan,9.0],
                "product2":[np.nan,np.nan,8.0],
                "product3":[np.nan,np.nan,7.0]
            }, index=['1.24', '2.24', '3.24']),
            "f3":pd.DataFrame({
                "product1":[2.0,2.0,2.0],
                "product2":[2.0,2.0,2.0],
                "product3":[2.0,2.0,2.0]
            }, index=['1.24', '2.24', '3.24']),
        }
    }