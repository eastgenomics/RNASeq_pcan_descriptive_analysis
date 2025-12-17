#!/bin/bash
#Rationale: extract sample IDs for all Eunomia runs from DNANexus

+set -e

dx login
#choose project 003_251118_RNASeq_GeneExpression

dx mkdir input

#For now, work with live files.
#Extract patient IDs from the job summary file and filter for sample IDs by PANCAN Epic-Testcode:

#First option - with CLI, although I get an exception message for the archived files (but faster)
dx find projects --name "002_*PCAN" --brief | \
xargs -P16 -I{} dx find data --name *conductor_job_summary.txt --project {} --brief | \
xargs -P16 -I{} dx cat {} | \
grep "10011\|10012" | awk -F'[ :]+' '{print $3}' | sort -u | \
dx upload - --path input/samples_pcan_live_251125.txt

dx logout