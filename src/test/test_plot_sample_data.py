import pandas as pd
import pytest

import plot_sample_data as psd

def test_that_error_raised_if_not_found_file():
    """
    Test that a FileNotFoundError is raised if an input file is not found
    """
    input_file = "input/not_existing_file.xlsx"
    with pytest.raises(FileNotFoundError):
        psd.read_txt_to_dataframe(input_file)