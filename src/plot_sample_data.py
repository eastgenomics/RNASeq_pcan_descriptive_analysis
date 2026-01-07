#Rationale: descriptive analysis of the PCAN samples

# system
import argparse
import re

#library from 3rd parties:
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

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
        help="The txt file name with cohort features to perform descriptive analysis"
    )
    
    parser.add_argument(
        "-o",
        "--output_folder",
        type=str,
        required=True,
        help="The folder name in which to save the plots"
    )

    args = parser.parse_args()
    return args

def read_txt_to_dataframe(input_file: str) -> pd.DataFrame:
    """
    Read a txt file to a Pandas dataframe.

    Parameters
    ----------
    input_file : str
        Name of input file

    Returns
    ----------
    pd.DataFrame
        txt file contents as Pandas dataframe
    
    Raises
    ----------
    SystemExit
        If file not found
    """
    try:
        dataframe = pd.read_csv(input_file, encoding="utf-8", header=0, sep = "\t")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found -> {input_file}.") from exc
    
    #print(dataframe)
    return dataframe

def piechart_plot(input_df: pd.DataFrame, colnames_to_plot: str, output_folder: str):
    """
    Read a dataframe and do a pie chart of the specified column

    Parameters
    ----------
    input_df : pd.DataFrame
        Input dataframe
    
    colnames_to_plot: str
        Name of the column to plot a piechart
    
    output_folder: str
        Output folder where to save the plot
    
    Returns
    ----------
    piechart plot
        plt piechart saved as .png figure
    
    Raises
    ----------
    ValueError
        If column not found in the dataframe
    """
    required_colnames = {colnames_to_plot}
    column_names = input_df.columns.tolist()
    column_names_set = set(column_names)
    if (required_colnames.issubset(column_names_set) != True):
        raise ValueError('Dataframe does not contain the required colname')
    
    #Column of interest as categorical variable: 
    input_df[colnames_to_plot] = input_df[colnames_to_plot].astype("category")
    
    # Create value counts and labels to plot:
    size= input_df[colnames_to_plot].value_counts(dropna=False)
    size_percentage = input_df[colnames_to_plot].value_counts(dropna=False, normalize=True) * 100
    labels = [f"{idx} ({val:.02f}%)" for idx, val in size_percentage.items()]
    
    #Create the folder if not existing:
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    # Do the pie chart:
    sns.set_theme()
    sns.set_style("whitegrid")
    colors = ['#12436D', '#F46A25', '#801650', '#28A197']
    plt.figure(figsize=(6,6))
    plt.pie(size, labels = labels, colors = colors)
    plt.savefig(f"{output_folder}piechart_{colnames_to_plot}.png")
    plt.show()
    plt.close()



def main():
    args = parse_args()
    df_samples = read_txt_to_dataframe(args.input_file)
    piechart_plot(df_samples, 'patient_stated_gender',args.output_folder)
    piechart_plot(df_samples, 'test_passed_failed',args.output_folder)
    piechart_plot(df_samples, 'test_passed_fusion',args.output_folder)
    

if __name__ == "__main__":
    main()