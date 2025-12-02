#!/bin/usr/sh

#Rationale: compare gene fusions detectable from PANCAN and RES with the gene fusion reported in the NHS Test Directory
mkdir input

#NHS Test Directory gene fusion (from DNA Nexus):
#file ID: file-GpGVQZj4JJKy6vGyZz2GQ2p2
cd input/
dx download file-GpGVQZj4JJKy6vGyZz2GQ2p2

#TruSight gene fusion list:
wget -P input/ https://emea.illumina.com/content/dam/illumina-marketing/documents/products/gene_lists/gene_list_trusight_pan_cancer.xlsx


#How many gene fusions in NHS Test Directory can be detected by the TruSight gene fusion kit ?
#Script in python to compare - need to read the xlsx file.