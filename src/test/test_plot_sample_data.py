import pandas as pd
import pytest

import pcan_samples_descriptive as psd

def test_that_error_raised_if_not_found_file():
    """
    Test that a SystemError is raised if an input file is not found
    """
    input_file = "input/not_existing_file.xlsx"
    with pytest.raises(SystemError):
        psd.read_txt_to_dataframe(input_file)