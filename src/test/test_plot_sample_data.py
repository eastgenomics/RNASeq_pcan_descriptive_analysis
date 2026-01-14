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


def test_that_error_raised_if_colnames_not_found():
    """
    Test that a ValueError is raised if column name is not found in the dataframe
    """
    df_missing_colname = pd.DataFrame(columns=['test_result'])
    new_col_name_test = 'test_passed_fusion'
    output_filename_test = './output/samples_plot'
    with pytest.raises(ValueError):
        psd.piechart_plot(df_missing_colname, new_col_name_test, output_filename_test)
    with pytest.raises(ValueError):
        psd.count_plot(df_missing_colname, new_col_name_test, output_filename_test)
    with pytest.raises(ValueError):
        psd.box_plot(df_missing_colname, new_col_name_test, output_filename_test)