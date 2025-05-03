import os
import csv

# === Settings ===
# Folder where all individual capture CSV files are stored
input_folder = "network_logs"

# Name of the final merged output file
output_file = "merged_network_data.csv"

# CSV header (ensure it matches the headers in each capture file)
fields = ["timestamp", "src_ip", "dst_ip", "protocol", "src_port", "dst_port", "length"]

# === Function to Merge CSVs ===
def merge_csv_files():
    """
    Merges all CSV files in the input folder into a single CSV file.
    Skips the header line for all files except the first one to avoid duplication.
    """
    with open(output_file, mode='w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(fields)  # Write header row only once at the top

        # Loop through each file in the input directory
        for filename in sorted(os.listdir(input_folder)):
            if filename.endswith(".csv"):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, mode='r') as in_file:
                    reader = csv.reader(in_file)
                    next(reader)  # Skip header of each input file
                    for row in reader:
                        writer.writerow(row)  # Write data row to the output file

    print(f"[+] Merged all CSV files into '{output_file}'")

# === Entry Point ===
if __name__ == "__main__":
    merge_csv_files()
