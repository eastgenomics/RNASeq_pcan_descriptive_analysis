#!/usr/bin/python3

#Rationale: download all "*PCAN*.star.bam.gene_tpm.gct" files from several projects
import dxpy
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

file_list_path="./input/PCAN_tpm_project_file_ID"

# Folder where files will be saved
DOWNLOAD_DIR = "./input/TPM_files"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Number of threads for parallel processing
MAX_WORKERS = 32

# Read the file list
files_to_process = []
with open(file_list_path, "r") as f:
    for line in f:
        line = line.strip()
        if not line or ":" not in line:
            continue
        project_id, file_id = line.split(":", 1)
        files_to_process.append((project_id, file_id))

archived_file=[]

#Save file for the archived project-file:
def append_project_file(filename, project_file):
    """
    Appends a single project:file entry to a file, one per line.

    Args:
        filename (str): Path of the file to append to.
        project_file (str): String in the format 'project:file'.
    """
    with open(filename, "a") as f:
        f.write(f"{project_file}\n")


# Function to process a single file
def process_file(project_file):
    original_project, file_id = project_file
    try:
        file_obj = dxpy.DXFile(file_id)
        desc = file_obj.describe()
        state = desc.get("archivalState")
        print(state)

        if state == "live":
            dxpy.bindings.dxfile_functions.download_dxfile(
            file_id,
            os.path.join(DOWNLOAD_DIR, dxpy.describe(file_id).get('name')),
            project=original_project)
            return f"{original_project}:{file_id} -> Copied live locally to {DOWNLOAD_DIR}"
            
        elif state == "archived":
            append_project_file("./input/PCAN_tpm_project_file_ID_archived",f"{original_project}:{file_id}")
            return f"{original_project}:{file_id} -> Archived - saved to a file"

        else:
            return f"{original_project}:{file_id} -> Unexpected state: {state}"

    except dxpy.exceptions.DXError as e:
        return f"{original_project}:{file_id} -> Error: {str(e)}"



# Process files in parallel
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(process_file, f): f for f in files_to_process}

    for future in as_completed(futures):
        print(future.result())