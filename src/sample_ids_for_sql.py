"""
Reads a text file of sample IDs, adds an 'SP-' prefix, removes duplicates, and generates output suitable for SQL Server queries for descriptive analysis.

"""
input_file = "samples_pcan_live_251125.txt"
sp_output_file = "sample_id_with_sp.txt"
duplicates_file = "sample_id_duplicates.txt"

input_line_count = 0
sp_output_line_count = 0
duplicate_line_count = 0
unique_ids = set()
duplicate_id = set()

#Process input file and generates sample IDs with SP- prefix
with open(input_file, "r", encoding="utf-8-sig") as first_file, open(sp_output_file,"w",  encoding="utf-8-sig") as second_file:
    for line in first_file:
        input_line_count += 1
        line = line.strip()
        
        if line:
            parts = line.split("-")
            if len(parts) < 2:
                print(f"Warning: Skipping malformed line {input_line_count}: '{line}'")
                continue
            new_id = "SP-" + parts[1]
            
            if new_id in unique_ids:
                duplicate_id.add(new_id)
                duplicate_line_count += 1
                
            else:
                second_file.write(new_id + "\n")
                unique_ids.add(new_id)
                sp_output_line_count += 1

#Write duplicates to a file
with open(duplicates_file, "w",encoding="utf-8-sig") as dup_id_file:
    for dup in sorted(duplicate_id):
        dup_id_file.write(dup + "\n")

# Print summary 
print(f"Total lines in input file: {input_line_count}")
print(f"Total lines written to output file: {sp_output_line_count}")
print(f"Total number of duplicate sample IDs: {duplicate_line_count}")

#Generate SQL appropriate list of all the unique IDs
sql_list_format = "(" + ", ".join(f"'{d}'" for d in sorted(unique_ids)) + ")"

print("Unique sample IDs (duplicates removed):")
print(sql_list_format)