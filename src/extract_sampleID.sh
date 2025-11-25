#!/bin/usr/sh

#Rationale: extract sample IDs for all Eunomia runs from DNANexus

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

#Second option is to use the API method /system/findDataObjects embedding this command into a function.


#Additional - Exploratory analysis:
##Total (002_*PCAN) files:
dx find projects --name "002_*PCAN" --brief | wc -l

##Total conductor_job_summary.txt file for Eunomia (002_*PCAN): [55]
dx find projects --name "002_*PCAN" --brief | \
xargs -P16 -I{} dx find data --name *conductor_job_summary.txt --project {} --brief | \
wc -l


##Some conductor_job_summary.txt files are archived -check how many: [34]
dx find projects --name "002_*PCAN" --brief | \
xargs -P16 -I{} dx find data --name *conductor_job_summary.txt --project {} --brief | \
args -P16 -I{} dx describe {} | \
grep "ID\|archivalState\|archivedAt" | \
grep -w "archived" -c

##Count conductor_job_summary.txt how many files are live: [21]
dx find projects --name "002_*PCAN" --brief | \
xargs -P16 -I{} dx find data --name *conductor_job_summary.txt --project {} --brief | \
xargs -P16 -I{} dx describe {} | \
grep "ID\|archivalState\|archivedAt" | \
grep -w "live" -c


