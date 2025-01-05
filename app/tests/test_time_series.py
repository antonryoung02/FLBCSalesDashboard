import pytest
import pandas as pd
import numpy as np
from app.time_series import TimeSeriesPipeline

@pytest.fixture
def mock_data_1():
    mock_df_dict = {
        "1.24": pd.DataFrame({
            'col1': [np.nan, np.nan, np.nan, np.nan],
            'col2': [np.nan, 3, 3, 3],
            'col3': [np.nan, 2, 3, 4]
        }, index=['p1', 'p2', 'p3', 'p4']),
        "2.24": pd.DataFrame({
            'col1': [np.nan, np.nan, np.nan, np.nan],
            'col2': [np.nan, 3, 3, 3],
            'col3': [np.nan, 2, 3, 4]
        }, index=['p1', 'p2', 'p3', 'p4']),
        "11.24": pd.DataFrame({
            'col1': [np.nan, 2, 2, 2],
            'col2': [np.nan, 3, 3, np.nan],
            'col3': [np.nan, 2, 3, 4]
        }, index=['p1', 'p2', 'p3', 'p4']),
        "1.25": pd.DataFrame({
            'col1': [2, 2, 2, 2],
            'col2': [3, 3, 3, 3],
            'col3': [1.0, 2.0, 3.0, 4.0],
        }, index=['p1', 'p2', 'p3', 'p4']),
    }
    return mock_df_dict

@pytest.fixture
def expected_results_1():
    expected_col_1 = pd.DataFrame({
        "p1": [np.nan, np.nan, np.nan, 2.0],
        "p2": [np.nan, np.nan, 2.0, 2.0],
        "p3": [np.nan, np.nan, 2.0, 2.0],
        "p4": [np.nan, np.nan, 2.0, 2.0],
    }, index=['1.24', '2.24', '11.24', '1.25'])

    expected_col_2 = pd.DataFrame({
        "p1": [np.nan, np.nan, np.nan, 3.0],
        "p2": [3.0, 3.0, 3.0, 3.0],
        "p3": [3.0, 3.0, 3.0, 3.0],
        "p4": [3.0, 3.0, np.nan, 3.0],
    }, index=['1.24', '2.24', '11.24', '1.25'])

    expected_col_3 = pd.DataFrame({
        "p1": [np.nan, np.nan, np.nan, 1],
        "p2": [2.0, 2.0, 2.0, 2.0],
        "p3": [3.0, 3.0, 3.0, 3.0],
        "p4": [4.0, 4.0, 4.0, 4.0],
    }, index=['1.24', '2.24', '11.24', '1.25'])

    return {
        'col1': expected_col_1,
        'col2': expected_col_2,
        'col3': expected_col_3,
    }

@pytest.fixture
def pipeline():
    return TimeSeriesPipeline()

def test_transform(pipeline, mock_data_1, expected_results_1):
    res_df_dict = pipeline.transform(mock_data_1)

    assert list(res_df_dict.keys()) == ['col1', 'col2', 'col3']

    pd.testing.assert_frame_equal(res_df_dict['col1'], expected_results_1['col1'])
    pd.testing.assert_frame_equal(res_df_dict['col2'], expected_results_1['col2'])
    pd.testing.assert_frame_equal(res_df_dict['col3'], expected_results_1['col3'])
