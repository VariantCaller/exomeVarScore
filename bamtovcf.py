import csv
import os
import subprocess
import concurrent.futures

# Read the paths and settings from the config file
with open('config.txt') as f:
    config = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

samples = config['SAMPLE_NAMES']
threads = config['THREADS']
workers = config['MAX_CORES']
ref_path = config['REF_DIR']
coverage = config['MIN_COVERAGE']
gapLength = config['GAP_LENGTH']
count = config['ALT_ALLELE_COUNT']
qualityscr = config['QUALITY_SCORE']

# Create output directories if they do not exist
os.makedirs('VCF', exist_ok=True)

# Define a function to process each SRA ID
def process_sra(sra_id):

    # Call freebayes on the sorted BAM file
    cmd = f"freebayes -f {ref_path} --min-coverage {coverage} -g {gapLength} -m {count} -q {qualityscr} -n {threads} BAM/{sra_id}.sorted.bam > VCF/{sra_id}.vcf"
    print(cmd)
    subprocess.run(cmd, shell=True)

# Open the CSV file containing the SRA ID numbers
with open(f'{samples}', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)

    # Use ThreadPoolExecutor to process multiple SRA IDs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(workers)) as executor:
        futures = [executor.submit(process_sra, row['acc']) for row in reader]
        for future in concurrent.futures.as_completed(futures):
            future.result()

