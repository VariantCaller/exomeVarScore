import csv
import os

# Create a folder called 'SRA' if it doesn't already exist
if not os.path.exists('SRA'):
    os.makedirs('SRA')

# Open the CSV file containing the SRA ID numbers
with open('SraAccList.csv', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    # Loop through each row in the file
    for row in reader:
        # Extract the SRA ID from the "acc" column
        sra_id = row['acc']
        # Print some information about the current ID being processed
        print(f"Processing SRA ID: {sra_id}")
        # Download the FASTQ files for the current ID and save them in the 'SRA' folder
        first = os.path.join('SRA', sra_id + "_1.fastq")
        second = os.path.join('SRA', sra_id + "_2.fastq")
        os.system(f"fasterq-dump {sra_id} -p -e 12 --outdir SRA")
        os.system(f"gzip {first}")
        os.system(f"gzip {second}")
        # Print some information about the saved files
        print(f"Files saved in SRA/{sra_id}")
