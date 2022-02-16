import pytest
import pandas as pd


@pytest.fixture
def constructor_frame(data):
    return pd.DataFrame(data)
