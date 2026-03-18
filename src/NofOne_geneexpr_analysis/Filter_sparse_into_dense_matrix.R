#!/usr/bin/R
#Rationale: Filter a Sparse TPM Matrix into Dense TPM Matrix

library(data.table)
library(Matrix) #useful to deal with sparse matrix

# ---------------------------
# Get Matrix from command line
# ---------------------------
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("Please provide a sparse matrix and an output file-name as arguments")
}

#Output dense matrix file name:
out_dense_mat_name <- args[2]

#Read sparse matrix:
sparse_mat_file <- args[1]
sparse_mat <- readRDS(sparse_mat_file)

#Remove genes never expressed
keep1 <- Matrix::rowSums(sparse_mat) > 0

#Minimum expression threshold: TPM > 1 in at least k samples
k=1
keep2 <- Matrix::rowSums(sparse_mat > 1) >= k

#Presence filter - expression filter
#Keep genes expressed in a minimum number of samples: gene must be expressed in ≥K% of samples.
k_perc=0.2
keep3 <- Matrix::rowMeans(sparse_mat > 1) >= k_perc

#Combine filters:
sparse_mat_filtered <- sparse_mat[keep1 & keep2 & keep3, ]

#To check for sparsity:
nnzero(sparse_mat_filtered) / length(sparse_mat_filtered)

#Save filtered as data.frame (.tsv) for visualisation: 
dense_mat <- as.matrix(sparse_mat_filtered)
write.table(dense_mat, file=paste0(out_dense_mat_name,".tsv"), sep="\t", quote=FALSE)

#Save filtered as dgCMatrix for downstream numerical computation:
saveRDS(sparse_mat_filtered, file = paste0(out_dense_mat_name,".rds"))