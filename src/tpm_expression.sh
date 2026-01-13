#!/bin/bash

#Select Project
dx select #project

#Find all gene TPM files and save all the file IDs to a text file
dx find data --name "*.gene_tpm.gct" --brief > gene_tpm.txt

#Download each file listed in the gene_tpm.txt
while read file; do
    dx download "$file"
done < gene_tpm.txt 

#Header for combined tpm matrix
header="GeneID\tGeneName"

##Loop over each TPM file to extract sample names and add that as header
for f in *.gene_tpm.gct; do
    sample=$(basename "$f" .gene_tpm.gct | cut -d'-' -f2)
    header="$header\t$sample"
done

#Write the header line in the output file
echo -e "$header" > combined_gene_expression_matrix.tsv

#Extract GeneID and Gene name from the first GCT file
awk 'NR>3 {print $1"\t"$2}' $(ls *.gene_tpm.gct | head -n1) >  genes.txt

"""
For every sample .gct file, extract the TPM, and build it the combined tpm matrix.
Any empty TPM, set it to 0. 
"""

while read -r geneid genename; do
    line="$geneid\t$genename"
    for f in *.gene_tpm.gct; do
        tpm=$(awk -v g="$geneid" 'NR>2 && $1==g {print $3}' "$f")
        tpm=${tpm:-0}
        line="$line\t$tpm"
    done
    echo -e "$line" >> combined_gene_expression_matrix.tsv
done < genes.txt


