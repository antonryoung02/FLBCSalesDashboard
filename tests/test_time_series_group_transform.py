import pytest
import pandas as pd
from app.transform_data.time_series_group_transform import time_series_group_transform 

def test_transform_removes_ignored_features(pipeline, dataframe_with_ignored_features):
    res = pipeline(dataframe_with_ignored_features)
    assert "ignore" not in res.keys()
    assert len(res.keys()) == 1

def test_transform_averages_mean_columns(pipeline, dataframe_with_mean_and_sum_features):
    res = pipeline(dataframe_with_mean_and_sum_features['input'])
    pd.testing.assert_index_equal(res['mean'].columns, pd.Index(['m', 's']))
    pd.testing.assert_frame_equal(res['mean'], dataframe_with_mean_and_sum_features['solution']['mean'])

def test_transform_sums_non_mean_columns(pipeline, dataframe_with_mean_and_sum_features):
    res = pipeline(dataframe_with_mean_and_sum_features['input'])
    pd.testing.assert_index_equal(res['arbitrary_feature'].columns, pd.Index(['m', 's']))
    pd.testing.assert_frame_equal(res['arbitrary_feature'], dataframe_with_mean_and_sum_features['solution']['arbitrary_feature']) 

@pytest.fixture
def dataframe_with_mean_and_sum_features():
    return {
        "input": {
            "mean": pd.DataFrame({
                "m1":[1.0,1.0],
                "m2":[2.0,2.0],
                "s1":[3.0,3.0],
                "s2":[4.0,4.0]
            }, index=['1.24', '2.24']),
            "arbitrary_feature": pd.DataFrame({
                "m1":[1.0,1.0],
                "m2":[2.0,2.0],
                "s1":[3.0,3.0],
                "s2":[4.0,4.0]
            }, index=['1.24', '2.24']),
        },
        "solution": {
            "mean": pd.DataFrame({
                "m":[1.5,1.5],
                "s":[3.5,3.5],
            }, index=['1.24', '2.24']),
            "arbitrary_feature": pd.DataFrame({
                "m":[3.0,3.0],
                "s":[7.0,7.0],
            }, index=['1.24', '2.24']),
        }
    }

@pytest.fixture
def dataframe_with_ignored_features():
    return {
        "ignore":pd.DataFrame({
            "m1": [1,2,3],
            "m2": [2,3,4],
            "s1": [3,4,5]
        }, index=['1.24', '2.24', '3.24']),
        "non-ignored_feature":pd.DataFrame({
            "m1": [1,2,3],
            "m2": [2,3,4],
            "s1": [3,4,5]
        }, index=['1.24', '2.24', '3.24']),
    }

@pytest.fixture
def pipeline():

    def helper(dataframe_dict):
        categories = { 
            "m":["m1", "m2", "m3"],
            "s":["s1", "s2", "s3"]
        }
        mean_features=["mean"]
        features_to_ignore=["ignore"]
        return time_series_group_transform(dataframe_dict, categories, mean_features, features_to_ignore)

    return helper
