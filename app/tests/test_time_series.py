import pytest
import pandas as pd
import numpy as np
from app.time_series import TimeSeriesPipeline

def test_transform():
    pass


@pytest.fixture
def pipeline():
    return TimeSeriesPipeline()
