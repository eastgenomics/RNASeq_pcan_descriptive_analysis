#!/usr/bin/R

#Rationale:Transform TPM into log2(TPM+1) and calculate the Tukey outlier threshold

library(data.table)
library(tidyverse)
library(Matrix)
#install.packages("matrixStats")
library(matrixStats) #to do calculation with a large-scale dense matrix

# ---------------------------
# Get Input Matrix and Output prefix name from command line
# ---------------------------
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("Please provide a dense and filtered matrix and the prefix for output name-files as arguments")
}

dense_matrix_file <- args[1]
output_prefix <- args[2]

#Read dense matrix:
dense_mat <- readRDS(dense_matrix_file )

#Calculate log2(TMP) - add 1 to avoid log2(0):
log2_dense <- log2(dense_mat + 1)

#Save log2(TMP):
saveRDS(log2_dense, file = (paste0("./output/",output_prefix,"_TPM_filtered_dense_log2transformed.rds")))

#Convert to a data.frame as save like that:
log2_dense_df <- as.data.frame(as.matrix(log2_dense))

#Calculate Tukey threshold for each gene:
##Convert into matrix:
log2_dense_mat <- as.matrix(log2_dense)

##Compute quartiles per gene
Q1 <- rowQuantiles(log2_dense_mat, probs = 0.25)
Q3 <- rowQuantiles(log2_dense_mat, probs = 0.75)
IQR <- Q3 - Q1

##Tukey upper thresholds:
upper_thresh <- Q3 + 1.5 * IQR
names(upper_thresh) <- rownames(log2_dense_mat)

#Save outliers threshold: - need to be edited
write.table(upper_thresh, paste0("./output/",output_prefix,"_upper_thresh_Tukey_outliers.tsv"))

#Find outliers:
outlier_mat <- log2_dense > upper_thresh[rownames(log2_dense)]

#Convert to long format
outlier_dt <- which(outlier_mat, arr.ind = TRUE)  # matrix of row,col indices
outlier_dt <- data.table(
  gene = rownames(log2_dense)[outlier_dt[,1]],
  sample = colnames(log2_dense)[outlier_dt[,2]],
  log2_TPM = log2_dense[outlier_dt]
)

#Save outliers results:
fwrite(outlier_dt, paste0("./output/",output_prefix,"_gene_sample_outliers.tsv"), sep="\t")