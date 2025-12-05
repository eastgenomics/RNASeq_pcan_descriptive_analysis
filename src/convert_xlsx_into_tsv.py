#!/usr/bin/env python3

#Rationale: convert xlsx file into tsv file

import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="TruSight gene panel list")
parser.add_argument("output_file", help="Formatted TruSight gene panel list")
args = parser.parse_args()


def convert_xlsx_into_tsv(infile_name, outfile_name):
    gene_list_pancan = pd.read_excel(infile_name, skiprows=2,header=None)
    gene_list_pancan.columns = ["Gene", "Excess"]
    print(gene_list_pancan.head())
    gene_list_pancan = gene_list_pancan['Gene'].dropna()
    #1385 cancer gene - check if right number
    print(gene_list_pancan.head())
    if (len(gene_list_pancan) == 1385):
        print(f"There are {len(gene_list_pancan)} as expected - writing formatting version into {outfile_name}")
        gene_list_pancan.to_csv(outfile_name, index=False, sep='\t')
    else:
        print("Gene list is not as expected (less or more than 1385 genes)")

convert_xlsx_into_tsv(args.input_file, args.output_file)