#!/usr/bin/R
#Rationale: create sparse TPM Matrix for tumour and control

library(data.table)
library(stringr)
library(Matrix) #useful to deal with sparse matrix


# ---------------------------
# Get List Files from command line
# ---------------------------
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("Please provide the list of file as arguments")
}

#List Files
files <- readRDS(args[1])

#Read gene column once
genes <- fread(files[1])$Name

#Check files have same order for genes:
all(sapply(files, function(f) identical(fread(f, skip=2)$Name, genes)))

#read only TPM column from each file
tpm_matrix <- sapply(files, function(f) fread(f, skip=2)$TPM)

# convert numeric matrix to sparse
sparse_mat <- Matrix(tpm_matrix, sparse = TRUE)


# add row/column names
colnames(sparse_mat) <- sub(".*([0-9]{5}[SKQ][0-9]{4}).*", "\\1", basename(files))
rownames(sparse_mat) <- genes

#Split into tumour and control matrix:
tumour_idx <- grepl("[SK]", colnames(sparse_mat))
control_idx <- grepl("Q", colnames(sparse_mat))
sparse_mat_tumour <- sparse_mat[, tumour_idx] #all columns with solid tumour (S) or haem-onc (K)
sparse_mat_control <- sparse_mat[, control_idx] #all columns with control (Q)
##Verify:
dim(sparse_mat)              # original
dim(sparse_mat_tumour)       # tumour samples
dim(sparse_mat_control)      # control samples

table(tumour_idx)
table(control_idx)


#Check sparsity of the matrix:
#If < 50% non-zero → use sparse
#If > 50% non-zero → dense TSV is fine
print("Sparsity check for tumour matrix:")
nnzero(sparse_mat_tumour) / length(sparse_mat_tumour)
print("Sparsity check for control matrix:")
nnzero(sparse_mat_control) / length(sparse_mat_control)


#Save Tumour Matrix as a sparse matrix:
saveRDS(sparse_mat_tumour, file = "./output/TPM_sparse_tumour.rds")
saveRDS(sparse_mat_control, file = "./output/TPM_sparse_control.rds")