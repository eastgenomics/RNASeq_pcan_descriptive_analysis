#!/bin/bash

#Rationale: compare gene fusions detectable from PANCAN and RES with the gene fusion reported in the NHS Test Directory

#NHS Test Directory gene fusion (from DNA Nexus):
#file ID: file-GpGVQZj4JJKy6vGyZz2GQ2p2

#TruSight gene fusion list:
wget -P input/ -N https://emea.illumina.com/content/dam/illumina-marketing/documents/products/gene_lists/gene_list_trusight_pan_cancer.xlsx

##Convert xlsx into a text file in python:
python3 ./src/convert_xlsx_into_tsv.py \
    -i ./input/gene_list_trusight_pan_cancer.xlsx \
    -o ./input/formatted_gene_list_trusight_pan_cancer.tsv


#How many gene fusions in NHS Test Directory can be detected by the TruSight gene fusion kit ?
LEN_TEST_DIRECTORY_FUSION=$(dx cat file-GpGVQZj4JJKy6vGyZz2GQ2p2 | wc -l)
echo "Test Directory contains ${LEN_TEST_DIRECTORY_FUSION} gene fusions to test"

LEN_TEST_DIRECTORY_IN_TRUSIGHT=$(dx cat file-GpGVQZj4JJKy6vGyZz2GQ2p2 | \
    grep -F -f input/formatted_gene_list_trusight_pan_cancer.tsv -w -i | \
    wc -l)
echo "TruSight recognises ${LEN_TEST_DIRECTORY_IN_TRUSIGHT} gene fusion of the NHS Test Directory"
echo "Saving the recognised gene funsions into DNANexus project 003_RNA_251118_RNASeq_GeneExpression"
dx cat file-GpGVQZj4JJKy6vGyZz2GQ2p2 | \
    grep -F -f input/formatted_gene_list_trusight_pan_cancer.tsv -w -i --color=always | \
    dx upload - --path input/trusight_in_testdirectory.tsv

LEN_TEST_DIRECTORY_NOTIN_TRUSIGHT=$(dx cat file-GpGVQZj4JJKy6vGyZz2GQ2p2 | \
    grep -F -f input/formatted_gene_list_trusight_pan_cancer.tsv -w -i -v | \
    wc -l)
echo "TruSight does not recognise ${LEN_TEST_DIRECTORY_NOTIN_TRUSIGHT} gene fusion of the NHS Test Directory"
echo "Saving the NON recognised gene fusions into DNANexus project 003_RNA_251118_RNASeq_GeneExpression"
dx cat file-GpGVQZj4JJKy6vGyZz2GQ2p2 | \
    grep -F -f input/formatted_gene_list_trusight_pan_cancer.tsv -w -i -v | \
    dx upload - --path input/trusight_notin_testdirectory.tsv