import pytest
import pandas as pd
import numpy as np
from excel_to_pandas import ExcelToPandasPipeline

@pytest.fixture
def pipeline():
    return ExcelToPandasPipeline()

@pytest.fixture
def mock_data():
    return {
        "first": pd.DataFrame({
            'col2': [1.1, 2.2, 3.3],
            'col3': [1.11, 2.22, 3.33],
            'col1': [1, 2, 3],
        }, index=['row1', 'row2', 'row3']),
        "second": pd.DataFrame({
            'col1': [1, 2, 3],
            'col4': [1.1, 2.2, 3.3],
            'col5': [1.11, 2.22, 3.33]
        }, index=['row1', 'row4', 'row5']),
        "third": pd.DataFrame({
            'col3': [1, 2, 3, np.nan],
            'unnamed1': [np.nan, np.nan, np.nan, np.nan],
            'col5': [1.1, 2.2, 3.3, np.nan],
            'col6': [1.11, 2.22, 3.33, np.nan]
        }, index=['row3', 'row5', 'row6', 'nullrow']),
    }

@pytest.fixture
def expected_solutions():
    first_solution = pd.DataFrame({
        'col1': [1, 2, 3, np.nan, np.nan, np.nan],
        'col2': [1.1, 2.2, 3.3, np.nan, np.nan, np.nan],
        'col3': [1.11, 2.22, 3.33, np.nan, np.nan, np.nan],
        'col4': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        'col5': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        'col6': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    }, index=['row1', 'row2', 'row3', 'row4', 'row5', 'row6'])

    second_solution = pd.DataFrame({
        'col1': [1, np.nan, np.nan, 2, 3, np.nan],
        'col2': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        'col3': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        'col4': [1.1, np.nan, np.nan, 2.2, 3.3, np.nan],
        'col5': [1.11, np.nan, np.nan, 2.22, 3.33, np.nan],
        'col6': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    }, index=['row1', 'row2', 'row3', 'row4', 'row5', 'row6'])

    return {"first": first_solution, "second": second_solution}

@pytest.fixture
def mock_data_2():
    mock_df_dict = {
        "1.24": pd.DataFrame({
            'unnamed_col1': [np.nan, np.nan, np.nan],
            'unnamed_col2': [np.nan, np.nan, np.nan],
            'unnamed_col3': [np.nan, np.nan, np.nan],
        }),
        "11.25":pd.DataFrame({
            'valid2': [np.nan, np.nan, 1],
            'valid1': [1,2,3],
            'invalidtext': ['text1', 2, np.nan]
        }, index=['FIRSTPRODUCT', 'SECONDPRODUCT', 'THIRDPRODUCT']),
        "1.26":pd.DataFrame({
            'valid1': [2,3,4],
            'valid2': [np.nan, np.nan, 3],
            'unnamed_invalid': [np.nan, np.nan, np.nan]
        }, index=['FIRSTPRODUCT', 'SECONDPRODUCT', 'THIRDPRODUCT']),

    }

    return mock_df_dict

@pytest.fixture
def expected_solutions_2():

    expected_valid_1 = pd.DataFrame({
        'valid1': [np.nan, np.nan, np.nan],
        'valid2': [np.nan, np.nan, np.nan]
    }, index=["FIRSTPRODUCT", "SECONDPRODUCT", "THIRDPRODUCT"])

    expected_valid_2 = pd.DataFrame({
        'valid1': [1.0,2.0,3.0],
        'valid2': [np.nan, np.nan, 1.0]
    }, index=["FIRSTPRODUCT", "SECONDPRODUCT", "THIRDPRODUCT"])

    expected_valid_3 = pd.DataFrame({
        'valid1': [2.0,3.0,4.0],
        'valid2': [np.nan, np.nan, 3.0], 
    }, index=["FIRSTPRODUCT", "SECONDPRODUCT", "THIRDPRODUCT"])

    return {
        '1.24': expected_valid_1,
        '11.25': expected_valid_2,
        '1.26': expected_valid_3
    }

def test_transform(pipeline, mock_data, mock_data_2, expected_solutions, expected_solutions_2):
    res = pipeline.transform(mock_data, inplace=False)

    pd.testing.assert_frame_equal(res['first'], expected_solutions['first'])
    pd.testing.assert_frame_equal(res['second'], expected_solutions['second'])

    res2 = pipeline.transform(mock_data_2, inplace=False)
    pd.testing.assert_frame_equal(res2['1.24'], expected_solutions_2['1.24'])
    pd.testing.assert_frame_equal(res2['11.25'], expected_solutions_2['11.25'])
    pd.testing.assert_frame_equal(res2['1.26'], expected_solutions_2['1.26'])

def test_remove_invalid_rows(pipeline, mock_data):
    testcase1 = mock_data["first"].copy()
    pipeline._remove_invalid_rows(testcase1)
    pd.testing.assert_index_equal(
        testcase1.index,
        mock_data["first"].index,
        obj="DataFrame Index"
    )

    testcase3 = mock_data["third"].copy()
    pipeline._remove_invalid_rows(testcase3)
    expected_index = mock_data["third"].index.difference(['nullrow'])
    pd.testing.assert_index_equal(
        testcase3.index,
        expected_index,
        obj="DataFrame Index"
    )

def test_remove_invalid_columns(pipeline, mock_data):
    testcase1 = mock_data["first"].copy()
    pipeline._remove_invalid_columns(testcase1)
    pd.testing.assert_index_equal(
        testcase1.columns,
        mock_data["first"].columns,
        obj="DataFrame Index"
    )

    testcase3 = mock_data["third"].copy()
    pipeline._remove_invalid_columns(testcase3)
    expected_columns = mock_data["third"].columns.difference(['unnamed1'])
    pd.testing.assert_index_equal(
        testcase3.columns,
        expected_columns,
        obj="DataFrame Index"
    )

# Placeholder tests for future implementation
@pytest.mark.skip(reason="Not implemented yet")
def test_insert_missing_rows():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_insert_missing_columns():
    pass