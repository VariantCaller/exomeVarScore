import csv
import os
import subprocess

# Read the paths and settings from the config file
with open('config.txt') as f:
    config = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

threads = config['THREADS']
index_path = config['REF_INDEX']

# Create output directories if they do not exist
os.makedirs('BAM', exist_ok=True)

# Define a function to process each SRA ID
def process_sra(sra_id):
    # Run BWA to align the reads to the reference genome
    bwa_cmd = f"bwa mem -t {threads} {index_path} SRA/{sra_id}_1.fastq.gz SRA/{sra_id}_2.fastq.gz"
    samtools_cmd = f"samtools view -bS - | samtools sort -O bam -o BAM/{sra_id}.sorted.bam -@ {threads} -T BAM/temp -"
    #with subprocess.Popen(bwa_cmd, stdout=subprocess.PIPE, shell=True) as proc1, \
        subprocess.Popen(samtools_cmd, stdin=proc1.stdout, shell=True) as proc2:
        # Wait for the command to finish before moving on
        proc2.wait()

    # Run samtools flagstat to generate some alignment statistics
    subprocess.run(f"samtools flagstat BAM/{sra_id}.sorted.bam", shell=True)

# Open the CSV file containing the SRA ID numbers
with open('SraAccList.csv', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    
    # Process each SRA ID sequentially
    for row in reader:
        process_sra(row['acc'])
