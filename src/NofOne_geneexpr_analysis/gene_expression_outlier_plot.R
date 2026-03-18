#!/usr/bin/R

#Rationale: for a gene of interest, plot the expression in log2(TPM +1) and highlight the outlier samples according to gene's Tukey's threshold

library(ggplot2)
library(data.table)
library(Matrix)

# ---------------------------
# Get gene from command line
# ---------------------------
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("Please provide a gene ensemble and gene symbol as arguments")
}

gene_of_interest <- args[1]
#gene_of_interest <- "ENSG00000119508.18"

gene_of_interest_symbol <- args[2]

# ---------------------------
# Load data
# ---------------------------
log2_dense <- readRDS("./output/TPM_filtered_dense_log2transformed.rds")
upper_thresh <- fread("./output/upper_thresh_Tukey_outliers.tsv", header = FALSE)
colnames(upper_thresh) <- c("gene", "threshold")
upper_thresh <- setNames(upper_thresh$threshold, upper_thresh$gene)

# ---------------------------
# Convert expression to long format
# ---------------------------
log2_dense_mat <- as.matrix(log2_dense)  # dgCMatrix → standard matrix
expr_dt <- as.data.table(log2_dense_mat, keep.rownames = "gene")  # rownames become 'gene'
expr_dt <- melt(
  expr_dt,
  id.vars = "gene",
  variable.name = "sample",
  value.name = "log2_TPM"
)


# ---------------------------
# Check gene exists
# ---------------------------
if (!(gene_of_interest %in% expr_dt$gene)) {
  stop(paste("Gene not found:", gene_of_interest))
}

# ---------------------------
# Subset gene and flag outliers
# ---------------------------
plot_dt <- expr_dt[gene == gene_of_interest]
threshold <- upper_thresh[gene_of_interest]
plot_dt[, is_outlier := log2_TPM > threshold]

# ---------------------------
# Plot scatter with outliers
# ---------------------------
# Plot
p <- ggplot(plot_dt, aes(x = sample, y = log2_TPM)) +
  geom_jitter(aes(color = is_outlier), width = 0.2, size = 0.5) +
  geom_hline(yintercept = threshold, linetype = "dashed", color = "blue") +
  geom_text(
    data = plot_dt[is_outlier == TRUE],
    aes(label = sample),
    vjust = -0.5,
    size = 3,
    color = "red"
  ) +
  scale_color_manual(values = c("black", "red")) +
  theme_bw() +
  theme(
    axis.text.x = element_blank(),    # hide x-axis tick labels
    axis.ticks.x = element_blank()    # hide x-axis ticks
  ) +
  labs(
    title = paste("Expression of", gene_of_interest),
    subtitle = "Blue dashed line = Tukey upper threshold",
    x = "Sample",
    y = "log2(TPM + 1)",
    color = "Outlier"
  )

  # ---------------------------
# Save plot
# ---------------------------
ggsave(
  filename = paste0("./output/", gene_of_interest, "_",gene_of_interest_symbol, "_scatter_outliers.png"),
  plot = p,
  width = max(5, 100 * 0.2),
  height = 10,
)