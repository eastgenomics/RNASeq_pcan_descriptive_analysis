#!/bin/usr/sh

#Rationale: extract sample IDs for all Eunomia runs from DNANexus

dx login
#choose project 003_251118_RNASeq_GeneExpression

dx mkdir input

#Total (002_*PCAN) files:
dx find projects --name "002_*PCAN" --brief | wc -l

#Total job summary file for Eunomia (002_*PCAN):
dx find projects --name "002_*PCAN" --brief | \
xargs -n1 -P16 -I{} dx find data --name *conductor_job_summary.txt --project {} --brief | \
wc -l

#Extract patient IDs from the job summary file:
dx find projects --name "002_*PCAN" --brief | \
xargs -n1 -P16 -I{} dx find data --name *conductor_job_summary.txt --project {} --brief | \
xargs -n1 -P16 -I{} dx 

#understand how to filter the content of a file in DNANexus

dx logout