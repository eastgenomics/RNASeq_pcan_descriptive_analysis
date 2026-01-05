#Rationale: clean sample data from epic and create a new column for test result (failed, passed_yes_fusion, passed_no_fusion)

# system
import argparse
import re

#library from 3rd parties:
import numpy as np
import pandas as pd

#local packages - if any:


def parse_args() -> argparse.Namespace:
    """
    Parse the inputs given on the command line
    
    Returns
    ----------
    args : Namespace
        Namespace object of passed command line argument inputs
    """
    parser = argparse.ArgumentParser(
        description="Required input file to convert xlsx file to tsv"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        required=True,
        help="The csv file name with cohort features to perform descriptive analysis"
    )
    
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=True,
        help="The folder name in which to save the plots"
    )
    
    args = parser.parse_args()
    return args


def read_csv_to_dataframe(input_file) -> pd.DataFrame:
    """
    Read a csv file to a Pandas dataframe.

    Parameters
    ----------
    input_file : str
        Name of input file

    Returns
    ----------
    pd.DataFrame
        csv file contents as Pandas dataframe
    
    Raises
    ----------
    SystemExit
        If file not found
    """
    try:
        dataframe = pd.read_csv(input_file, encoding="utf-8", header=0)
    except FileNotFoundError as exc:
        raise SystemError(f"File not found -> {input_file}.") from exc
    
    return dataframe


def validate_df_columns_number(input_df: pd.DataFrame) ->  pd.DataFrame:
    """
    Read Pandas dataframe and validate columns number

    Parameters
    ----------
    input_file : pd.DataFrame
        Pandas dataframe

    Returns
    ----------
    pd.DataFrame
        Pandas dataframe
    
    Raises
    ----------
    ValueError
        If columns number is not the expected one
    """
    if (len(input_df.columns) != 9):
        raise ValueError('Dataframe does not contain the correct number of columns (different from 9)') 

    print(f'Dataframe has the correct number of columns: {len(input_df.columns)} \n--------')
    return input_df


def validate_df_columns_name(input_df: pd.DataFrame) ->  pd.DataFrame:
    """
    Read Pandas dataframe and validate columns names

    Parameters
    ----------
    input_file : pd.DataFrame
        Pandas dataframe

    Returns
    ----------
    pd.DataFrame
        Pandas dataframe
    
    Raises
    ----------
    SyntaxError
        If columns names are not the expected ones
    """
    #using a set requirement, we can check that colname exist and that they appear in any order:
    required_colnames={'Specimen Identifier','Year of Birth','Patient Stated Ethnicity','Patient Stated Gender','Patient Age at Activity','Beaker Procedure Name','Received Specimen Source','Test Directory Test Code','Test Result'}
    column_names = input_df.columns.tolist()
    column_names_set = set(column_names)
    
    if (required_colnames.issubset(column_names_set) != True):
        raise SyntaxError('Dataframe does not contain the required colnames')
    
    print('Dataframe has the correct name columns \n--------\nStarting to clean the dataframe and create new columns based on "Test Result" column value \n--------')
    return input_df


def clean_dataframe(input_df: pd.DataFrame) ->  pd.DataFrame:
    """
    Read Pandas dataframe and clean it to have machine-readable columns and row contents

    Parameters
    ----------
    input_file : pd.DataFrame
        Pandas dataframe

    Returns
    ----------
    pd.DataFrame
        Pandas dataframe cleaned
    
    Raises
    ----------
    ValueError
        If col number different from eight, as one column has been dropped
    Value Error
        If columns are still presenting special characters as [' ', ', ','"','.     ']
    """
    #Clean column names:
    input_df.columns = (input_df.columns
                  .str.replace(" ", "_")
                  .str.lower()
                  .str.replace(r"[^\w]", "", regex = True)) # remove all special characters using regex
    
    #Drop 'beaker_procedure_name' not really needed:
    input_df = input_df.drop(columns = "beaker_procedure_name")

    #Clean specific column value: ', ', delete ", delete any special characters:
    input_df["received_specimen_source"] = input_df["received_specimen_source"].str.replace(", ", "_").str.lower()
    input_df["received_specimen_source"] = input_df["received_specimen_source"].str.replace(" ", "_").str.lower()
    
    input_df["test_result"] = input_df["test_result"].str.lower().str.replace(r"[^\w]", "_", regex = True) #clunky way but ok for this time
    input_df["test_result"] = input_df["test_result"].str.replace("_+", "_", regex = True).str.rstrip('_')
    input_df["test_result"] = input_df["test_result"].str.lstrip('_')
    
    #Clean all other object column columns:
    input_df_obj = input_df.select_dtypes('object')
    input_df[input_df_obj.columns] = input_df_obj.apply(lambda x: x.str.strip())

    #Drop duplicates in case there are:
    input_df = input_df.drop_duplicates()
    

    if (len(input_df.columns) !=8):
        raise ValueError('Dataframe does not have eight columns as expected as "beaker_procedure_name" as been dropped')
    
    matches = [' ', ', ','"','.     ']

    special_chars_df = input_df[input_df['test_result'].str.contains('|'.join(matches))]
    if (len(special_chars_df) > 0):
        raise ValueError('Special characters are still present in the dataframe')
    
    return input_df


def create_column_passedfail(clean_digest_df: pd.DataFrame, new_col_name: str, pattern_match: str, value_of_column: str ) ->  pd.DataFrame:
    """
    Read clean and digested Pandas dataframe and create a categorical new column (0: failed / 1:passed) based on test result column.
    Parameters
    ----------
    clean_df : pd.DataFrame
        Pandas dataframe that has been cleaned
    
    new_col_name: str
        name for the new column
    
    pattern_match: str
        list with multiple possible patterns to make a mask
    
    value_of_column: str
        value of the column: possible values: 0 or 1

    Returns
    ----------
    pd.DataFrame
        Pandas dataframe with new column(s)
    
    Raises
    ----------
    ???Error # still to be done
        If ??? still to be done
    """
    #Initialise the new column:
    clean_digest_df[new_col_name] = ""
    
    # Define the conditions and corresponding categories:
    mask = clean_digest_df['test_result'].map(lambda x: bool(re.search(pattern_match,x)))
    clean_digest_df[new_col_name][mask] = value_of_column

    # Assign 0 to failed test:
    clean_digest_df[new_col_name] = clean_digest_df[new_col_name].replace('','0')

    #Assign type of variable - catgorical:
    clean_digest_df[new_col_name] = clean_digest_df[new_col_name].astype("category")

    print(clean_digest_df[new_col_name].value_counts())
    print(clean_digest_df[clean_digest_df[new_col_name] == '0'])

    return clean_digest_df


#to be finished !
def categorise_passed(clean_digest_passed_df: pd.DataFrame, new_col_name: str, pattern_match: dict) ->  pd.DataFrame:
    """
    Categorise the passed test column into four categories: 99: failed test / 0:no clinical fusion / 1:clinical fusion / 2:uncertain significant fusion.
    Parameters
    ----------
    clean_df : pd.DataFrame
        Pandas dataframe with 'test_passed_failed' columns
    
    new_col_name: str
        name for the new column for fusion category
    
    pattern_match: dict
        dictionare with the three possible patterns to make masks: key is the category name and the values are the pattern.
    
    Returns
    ----------
    pd.DataFrame
        Pandas dataframe with new column 'test_passed_fusion'
    
    Raises
    ----------
    Error
        If the column 'test_passed_failed' is not present
    """
    # Define the conditions and corresponding categories
    if (clean_digest_passed_df['test_passed_failed'] is True):
        raise KeyError('Dataframe does not have the required column: "test_passed_failed"')
    
    

    #Initialise the new column:
    clean_digest_passed_df[new_col_name] = ""
    
    # Define the conditions and corresponding categories (clinical fusion / vus fusion):
    # The pattern for clinical fusion includes vus as well - they will then be categorised into vus with the appropriate mask
    value_fusion_clinical = list(pattern_match)[0]
    pattern_fusion_clinical = str(list(pattern_match.items())[0][1])
    mask_clinical = clean_digest_passed_df['test_result'].map(lambda x: bool(re.search(pattern_fusion_clinical,x)))
    clean_digest_passed_df[new_col_name][mask_clinical] = value_fusion_clinical

    value_fusion_vus = list(pattern_match)[1]
    pattern_fusion_vus = str(list(pattern_match.items())[1][1])
    mask_vus = clean_digest_passed_df['test_result'].map(lambda x: bool(re.search(pattern_fusion_vus,x)))
    clean_digest_passed_df[new_col_name][mask_vus] = value_fusion_vus

    # Assign 0 to non clinically significant fusion test:
    clean_digest_passed_df[new_col_name] = clean_digest_passed_df[new_col_name].replace('','0')
    
    
    #Assign '99' if test failed:
    mask_failed = (clean_digest_passed_df['test_passed_failed'] == '0')
    clean_digest_passed_df[new_col_name][mask_failed] = '99'

    #Assign type of variable - catgorical:
    clean_digest_passed_df[new_col_name] = clean_digest_passed_df[new_col_name].astype("category")

    print(clean_digest_passed_df[new_col_name].value_counts())
    print(clean_digest_passed_df[clean_digest_passed_df[new_col_name] == '0'])

    return clean_digest_passed_df



colname_title_pasfail = 'test_passed_failed'
pattern_to_match_passed = 'fusion_detected|fusion_has_been_detected|fusion_has_been_identified|the_fusion_was|no.*clinically*gene_fusion.*detect|no.*gene_fusion.*detect|fusion_did_not_detect|trusight_rna_pan_cancer.*did_not_detect|fusion_.*uncertain.*clinical.*significance|variant*_uncertain_*significance'
colname_value_passed = '1'

colname_title_fusion = 'test_passed_fusion'
pattern_to_match_fusion = {'1':'a_.*_has_been_identified|fusion_has_been_identified|the_fusion_was|uncertain','2':'uncertain'}


def main():
    args = parse_args()
    df_samples = read_csv_to_dataframe(args.input_file)
    df_samples_validated_colnumber = validate_df_columns_number(df_samples)
    df_samples_validated_colnumber_colnames = validate_df_columns_name(df_samples_validated_colnumber)
    df_samples_clean = clean_dataframe(df_samples_validated_colnumber_colnames)
    df_samples_clean_passed_col = create_column_passedfail(df_samples_clean, colname_title_pasfail, pattern_to_match_passed, colname_value_passed)
    df_samples_clean_passed_fusion_col = categorise_passed(df_samples_clean_passed_col, colname_title_fusion, pattern_to_match_fusion)

if __name__ == "__main__":
    main()