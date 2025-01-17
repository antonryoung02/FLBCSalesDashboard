import pytest
import pandas as pd
import numpy as np
from app.transformation_pipelines.standardize import StandardizePipeline 

def test_transform_with_different_columns(pipeline, dataframes_with_different_columns):
    input = dataframes_with_different_columns['input']
    solution = dataframes_with_different_columns['solution']

    pipeline.transform(input, inplace=True)

    pd.testing.assert_frame_equal(input['first'], solution['first'])
    pd.testing.assert_frame_equal(input['second'], solution['second'])

def test_transform_with_different_rows(pipeline, dataframes_with_different_rows):
    input = dataframes_with_different_rows['input']
    solution = dataframes_with_different_rows['solution']

    pipeline.transform(input, inplace=True)

    pd.testing.assert_frame_equal(input['first'], solution['first'])
    pd.testing.assert_frame_equal(input['second'], solution['second'])

def test_transform_with_different_columns_and_rows(pipeline, dataframes_with_different_columns_and_rows):
    input = dataframes_with_different_columns_and_rows['input']
    solution = dataframes_with_different_columns_and_rows['solution']

    pipeline.transform(input, inplace=True)

    pd.testing.assert_frame_equal(input['first'], solution['first'])
    pd.testing.assert_frame_equal(input['second'], solution['second'])
    pd.testing.assert_frame_equal(input['third'], solution['third'])

def test_transform_with_int_dtypes(pipeline, dataframes_with_int_dtypes):
    input = dataframes_with_int_dtypes['input']
    solution = dataframes_with_int_dtypes['solution']

    pipeline.transform(input, inplace=True)

    pd.testing.assert_frame_equal(input['first'], solution['first']) 

@pytest.fixture
def dataframes_with_different_columns():
    input = {
        "first":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0],
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.0,3.0,3.0,3.0]
        }, index=['r1', 'r2', 'r3', 'r4']),
        "second":pd.DataFrame({
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.0,3.0,3.0,3.0],
            'd':[4.0,4.0,4.0,4.0]
        }, index=['r1', 'r2', 'r3', 'r4']),
    }

    solution = {
        "first":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0],
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.0,3.0,3.0,3.0],
            'd':[np.nan,np.nan,np.nan,np.nan]
        }, index=['r1', 'r2', 'r3', 'r4']),
        "second":pd.DataFrame({
            'a':[np.nan,np.nan,np.nan,np.nan],
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.0,3.0,3.0,3.0],
            'd':[4.0,4.0,4.0,4.0]
        }, index=['r1', 'r2', 'r3', 'r4']),  
    }

    return {"input":input, "solution":solution}

@pytest.fixture
def dataframes_with_different_rows():
    input = {
        "first":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0],
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.0,3.0,3.0,3.0]
        }, index=['r1', 'r3', 'r4', 'r5']),
        "second":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0],
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.0,3.0,3.0,3.0]
        }, index=['r2', 'r3', 'r4', 'r5']),
    }

    solution = {
        "first":pd.DataFrame({
            'a':[1.0,np.nan,1.0,1.0,1.0],
            'b':[2.0,np.nan,2.0,2.0,2.0],
            'c':[3.0,np.nan,3.0,3.0,3.0]
        }, index=['r1', 'r2', 'r3', 'r4', 'r5']),
        "second":pd.DataFrame({
            'a':[np.nan,1.0,1.0,1.0,1.0],
            'b':[np.nan,2.0,2.0,2.0,2.0],
            'c':[np.nan,3.0,3.0,3.0,3.0]
        }, index=['r1', 'r2', 'r3', 'r4', 'r5']),
    }

    return {"input":input, "solution":solution}

@pytest.fixture
def dataframes_with_different_columns_and_rows():
    input = {
        "first":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0],
            'b':[2.0,2.0,2.0,2.0],
        }, index=['r1', 'r2', 'r3', 'r4']),
        "second":pd.DataFrame({
            'b':[1.0],
            'c':[2.0],
            'd':[3.01]
        }, index=['r5']),
        "third":pd.DataFrame(),
    }

    solution = {
        "first":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0,np.nan],
            'b':[2.0,2.0,2.0,2.0,np.nan],
            'c':np.nan,
            'd':np.nan
        }, index=['r1', 'r2', 'r3', 'r4', 'r5']),
        "second":pd.DataFrame({
            'a':np.nan,
            'b':[np.nan,np.nan,np.nan,np.nan,1.0],
            'c':[np.nan,np.nan,np.nan,np.nan,2.0],
            'd':[np.nan,np.nan,np.nan,np.nan,3.01]
        }, index=['r1', 'r2', 'r3', 'r4', 'r5']),
        "third":pd.DataFrame({
            'a':np.nan,
            'b':np.nan,
            'c':np.nan,
            'd':np.nan
        }, index=['r1', 'r2', 'r3', 'r4', 'r5'])
    }

    return {'input':input, 'solution':solution}


@pytest.fixture
def dataframes_with_int_dtypes():
    input = {
        "first":pd.DataFrame({
            'a':[1,1,1,1],
            'b':[2,2,2,2],
            'c':[3.25,3.5,3.75,4.01]
        }, index=['r1', 'r2', 'r3', 'r4']),
    }

    solution = {
        "first":pd.DataFrame({
            'a':[1.0,1.0,1.0,1.0],
            'b':[2.0,2.0,2.0,2.0],
            'c':[3.25,3.5,3.75,4.01]
        }, index=['r1', 'r2', 'r3', 'r4']),
    }

    return {"input":input, "solution":solution}

@pytest.fixture
def pipeline():
    return StandardizePipeline()
