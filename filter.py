import os
import csv

# Read the paths and settings from the config file
with open('config.txt') as f:
    config = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

samples = config['SAMPLE_NAMES']
freq = config['ALLELE_FREQ']
freqsrc = config['FREQ_SOURCE']
sift = config['SNPSIFT_DIR']
clear_dump = config.get('CLEAR_DUMP', False)


# Create the output directories if they don't exist
if not os.path.exists('FILTERED/dump'):
    os.makedirs('FILTERED/dump')

# Open the CSV file containing the SRA ID numbers
with open(f'{samples}', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    # Loop through each row in the file
    for row in reader:
        # Extract the SRA ID from the "acc" column
        sra_id = row['acc']
        # Iterate over the SRA IDs and perform the analysis

        # Filter by allele frequency
        print(f"Applying {freq} AF filter to {sra_id}")
        # Save output to file
        os.system(f"java -jar {sift}/SnpSift.jar filter '({freqsrc} <= {freq}) | (na {freqsrc})' ANNOTATED/{sra_id}.FullyAnnotated.vcf > FILTERED/dump/{sra_id}.filtered1.vcf")
        # Extract Table
        # Print ANN Fields
        os.system(f"bcftools query -f '[%INFO/CLNSIG\t%CHROM\t%POS\t%ID\t%GT\t%INFO/{freqsrc}\t%INFO/dbNSFP_SIFT_pred\t%INFO/dbNSFP_PROVEAN_pred\t%INFO/dbNSFP_Polyphen2_HDIV_pred\t%INFO/dbNSFP_FATHMM_pred\t%INFO/dbNSFP_MetaSVM_pred\t%INFO/dbNSFP_MutationAssessor_pred\t%INFO/dbNSFP_MutationTaster_pred\t%INFO/dbNSFP_CADD_phred\t%INFO/dbNSFP_GERP___RS\t%ANN\n]' -H FILTERED/dump/{sra_id}.filtered1.vcf | " +

        # Parse to tabs
        "tr '|' '\t' | " +

        # Print columns
        "awk -v FS='\\t' -v OFS='\\t' '{print $19, $2, $3, $4, $5, $20, $24, $25, $26, $17, $18, $1, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15}' | " +
        "sed -E 's/.*, *//g' | " +
        "sed -E 's/0\\.5//g' | " +
        "awk -v FS='\\t' -v OFS='\\t' '$13==\"\"{$13=\"NA\"}1' | " +

        # Add header
        f"awk -v FS='\\t' -v OFS='\\t' -v AF='dbNSFP_1000Gp3_AF' 'BEGIN{{print \"Gene.Name\",\"CHROM\",\"POS\",\"ID\",\"GT\",\"Gene.ID\",\"Transcript\",\"Allele.Change\",\"AA.Change\",\"Effect\",\"IMPACT\",\"Clinvar\",\"{freqsrc}\",\"SIFT_pred\",\"PROVEAN_pred\",\"Polyphen2_HDIV_pred\",\"FATHMM_pred\",\"MetaSVM_pred\",\"MutationAssessor_pred\",\"MutationTaster_pred\",\"CADD_phred\",\"GERP_RS\"}}{{print}}' | " +

        # Remove Clinvar Benign & Likely Benign
        f"awk -v FS='\\t' -v OFS='\\t' '$12!~/Benign/i' > FILTERED/{sra_id}.filtered.txt")

# Clear the dump folder if specified in config
if config.get('CLEAR_DUMP_FOLDER', 'False').lower() == 'true':
    os.system('rm -rf FILTERED/dump/*')

