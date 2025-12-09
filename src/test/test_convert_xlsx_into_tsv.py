import pandas as pd
import pytest

import convert_xlsx_into_tsv as convert

def test_that_error_raised_if_not_found_file():
    """
    Test that a SystemError is raised if an input file is not found
    """
    input_file = "input/not_existing_file.xlsx"
    with pytest.raises(SystemError):
        convert.read_xlsx_to_dataframe(input_file)


def test_that_error_raised_if_not_correct_gene_number():
    """
    Test that a ValueError is raised if the number of gene is different from 1385
    """
    gene_list_pancan = pd.DataFrame({"Gene":["BCC3","ABI1","ABL1","ABL2","ABLIM1","ACACA","ACE"]})
    output_filename = "input/formatted_gene_list_trusight_pan_cancer.tsv"
    with pytest.raises(ValueError):
        convert.save_df_into_tsv(gene_list_pancan, output_filename)



#run as: 
#cd src 
#pytest test