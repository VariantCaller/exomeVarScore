import os
import csv

os.environ['PYTHONPATH'] = ''

# Read the paths and settings from the config file
with open('config.txt') as f:
    config = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

samples = config['SAMPLE_NAMES']
assembly = config['GENOME_ASSEMBLY']
snpeffconfig = config['SNPEFF_CONFIG']
dbsnp = config['DBSNP_DB']
dbnsfp = config['DBNSFP_DB']
clinvar = config['CLINVAR_DB']
effdir = config['SNPEFF_DIR']
effx = config['SNPEFF_CONFIG']
sift = config['SNPSIFT_DIR']
clear_dump = config.get('CLEAR_DUMP', False)


# Create the output directories if they don't exist
if not os.path.exists('ANNOTATED/dump'):
    os.makedirs('ANNOTATED/dump')

# Add snpEff.jar to the PATH environment variable
os.environ['PATH'] += os.pathsep + effdir

# Add snpEff.jar to the PYTHONPATH environment variable
os.environ['PYTHONPATH'] += os.pathsep + effx

# Open the CSV file containing the SRA ID numbers
with open(samples, newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    # Loop through each row in the file
    for row in reader:
        # Extract the SRA ID from the "acc" column
        sra_id = row['acc']
        # Iterate over the SRA IDs and perform the analysis
        print("Mapping {} to genome".format(sra_id))
        os.system("java -jar {}/snpEff.jar -c {} -canon {} VCF/{}.vcf > ANNOTATED/dump/{}.mapped.vcf".format(effdir, snpeffconfig, assembly, sra_id, sra_id))
        print("dbSNP annotation for {}".format(sra_id))
        os.system("java -jar {}/SnpSift.jar annotate -id {} ANNOTATED/dump/{}.mapped.vcf > ANNOTATED/dump/{}.dbSNP.mapped.vcf".format(sift, dbsnp, sra_id, sra_id))
        print("dbNSFP annotation for {}".format(sra_id))
        os.system("java -jar {}/SnpSift.jar dbnsfp -db {} ANNOTATED/dump/{}.dbSNP.mapped.vcf > ANNOTATED/dump/{}.dbnsfp.dbSNP.mapped.vcf".format(sift, dbnsfp, sra_id, sra_id))
        print("Clinvar annotation for {}".format(sra_id))
        os.system("java -jar {}/SnpSift.jar annotate {} ANNOTATED/dump/{}.dbnsfp.dbSNP.mapped.vcf > ANNOTATED/{}.FullyAnnotated.vcf".format(sift, clinvar, sra_id, sra_id))

# Clear the dump folder if specified in config
if config.get('CLEAR_DUMP_FOLDER', 'False').lower() == 'true':
    os.system('rm -rf ANNOTATED/dump/*')
