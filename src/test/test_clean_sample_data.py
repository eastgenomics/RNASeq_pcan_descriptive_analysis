import pandas as pd
import pytest

import clean_sample_data as csd

def test_that_error_raised_if_not_found_file():
    """
    Test that a SystemError is raised if an input file is not found
    """
    input_file = "input/not_existing_file.xlsx"
    with pytest.raises(SystemError):
        csd.read_csv_to_dataframe(input_file)

def test_that_error_raised_if_wrong_col_number():
    """
    Test that a ValueError is raised if number of columns is different from nine
    """
    df_with_wrong_col_number = pd.DataFrame(columns=['Specimen Identifier','Year of Birth','Patient Stated Ethnicity'])
    with pytest.raises(ValueError):
        csd.validate_df_columns_number(df_with_wrong_col_number)

def test_that_error_raised_if_colnames_are_not_as_expected():
    """
    Test that a SyntaxError is raised if column names are not as expected
    """
    df_with_wrong_col_number = pd.DataFrame(columns=['Specimen Identifier','Year of Birth','Patient Stated Ethnicity'])
    with pytest.raises(SyntaxError):
        csd.validate_df_columns_name(df_with_wrong_col_number)


#to be checked !
def test_that_error_raised_if_colnames_not_found():
    """
    Test that a KeyError is raised if column name is not found in the dataframe
    """
    df_missing_colname = pd.DataFrame(columns=['test_result'])
    new_col_name_test = 'test_passed_fusion'
    pattern_match_test = {'1':'fusion_has_been_identified|the_fusion_was|^fusion_.*uncertain.*clinical.*significance|^variant*_uncertain_*significance','2':'fusion_.*uncertain.*clinical.*significance|variant*_uncertain_*significance'}
    with pytest.raises(KeyError):
        csd.categorise_passed(df_missing_colname, new_col_name_test, pattern_match_test)