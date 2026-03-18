#!/usr/bin/R
#Rationale: if samples have more than one file, keep the most recent

library(data.table)
library(stringr)

#List Files
files <- list.files("./input/TPM_files", pattern="*.gct", full.names=TRUE)

#De-duplicate the list files:
choose_file <- function(f) {
  # Remove files containing "Val"
  f <- f[!grepl("Val", f, ignore.case = TRUE)]
  if (length(f) == 0) return(NULL)
  
  # Prefer PCAN25*rpt* files
  idx_rpt <- grepl("-25PCAN.*rpt-", f)
  if (any(idx_rpt)) return(f[idx_rpt][1])
  
  # If both 26PCAN and 25PCAN exist → keep 26PCAN
  idx_26 <- grepl("-26PCAN-", f)
  idx_25 <- grepl("-25PCAN-", f)
  if (any(idx_26) && any(idx_25)) return(f[idx_26][1])
  
  # If multiple 25PCAN → pick the one with "-10012-"
  if (sum(idx_25) > 1) {
    idx_25_10012 <- grepl("-25PCAN.*-10012-", f)
    if (any(idx_25_10012)) return(f[idx_25_10012][1])
    else return(f[idx_25][1])
  }
  
  # If multiple 26PCAN → pick the one with "-10012-"
  if (sum(idx_26) > 1) {
    idx_26_10012 <- grepl("-26PCAN.*-10012-", f)
    if (any(idx_26_10012)) return(f[idx_26_10012][1])
    else return(f[idx_26][1])
  }
  
  # Default: keep first remaining file
  return(f[1])
}

# Extract sample IDs
sample_id <- str_extract(basename(files), "[0-9]{5}[SKQ][0-9]{4}")

# Split by sample
files_split <- split(files, sample_id)

# Apply function
files_filtered <- sapply(files_split, choose_file)

# Clean vector
files_filtered <- unname(files_filtered)
files_dedup <- unlist(files_filtered)

#Save De-dup list of files:
saveRDS(files_dedup, "./input/sample_files_dedup.rds")