import numpy as np
import pandas as pd
import app.dataframe_operations as dfo

def test_remove_invalid_rows():
    input = pd.DataFrame({
        'a':[0.0, 0.0, np.nan, 1.0],
        'b':[np.nan,np.nan,np.nan,0.0],
        'c':[2.0, 2.0, np.nan, 1.0],
        'd':[1,2,3,4]
    }, index=['r1', 'r2', 'r3', 'r4'])

    dfo.remove_invalid_rows(input)

    pd.testing.assert_index_equal(input.index, pd.Index(['r1', 'r2', 'r4']))

def test_remove_invalid_columns():
    input = pd.DataFrame({
        'a':[0.0, 0.0, np.nan, 1.0],
        'b':[np.nan,np.nan,np.nan,0.0],
        'c':[2.0, 2.0, np.nan, 1.0],
        'unnamed d':[1,2,3,4],
        'e unnamed':[np.nan,np.nan,np.nan,np.nan]
    }, index=['r1', 'r2', 'r3', 'r4'])

    dfo.remove_invalid_columns(input)

    pd.testing.assert_index_equal(input.columns, pd.Index(['a', 'b', 'c']))

def test_convert_columns_to_float64():
    input = pd.DataFrame({
        'a':[0.0, 0.0, np.nan, 1.0],
        'b':[np.nan,np.nan,np.nan,0.0],
        'c':[2.0, 2.0, np.nan, 1.0],
        'unnamed d':[1,2,3,4],
        'e unnamed':[np.nan,np.nan,np.nan,np.nan]
    }, index=['r1', 'r2', 'r3', 'r4'])

    dfo.convert_columns_to_float64(input)
    
    assert len(input.select_dtypes(include=['int','object']).columns) == 0

def test_insert_null_rows():
    input = pd.DataFrame({
        'a':[0.0, 0.0, np.nan, 1.0],
        'b':[np.nan,np.nan,np.nan,0.0],
    }, index=['r1', 'r2', 'r3', 'r4'])
    new_rows = ['r5', 'r6']

    output = dfo.insert_null_rows(input, new_rows)

    pd.testing.assert_index_equal(output.index, pd.Index(['r1', 'r2', 'r3', 'r4', 'r5', 'r6']))


def test_insert_null_columns():
    input = pd.DataFrame({
        'a':[0.0, 0.0, np.nan, 1.0],
        'b':[np.nan,np.nan,np.nan,0.0],
    }, index=['r1', 'r2', 'r3', 'r4'])
    new_columns = ['r5', 'r6']

    dfo.insert_null_columns(input, new_columns)

    pd.testing.assert_index_equal(input.columns, pd.Index(['a', 'b', 'r5', 'r6']))

