# exomeVarScore
ExomeVarScore is a powerful pipeline that processes whole exome sequencing (WES) data, transforming Sequence Read Archive (SRA) data to VCF format and adding annotations using SnpEff/SnpSift. The pipeline also includes a variant scoring algorithm that assigns weights to variants based on ten different criteria.

## Getting Started

Note: Before beginning, be sure to check that you have downloaded the necessary programs and databases. This information, along with directions for download are provided in _programs.txt_
  * Once you have the programs/databases downloaded and functioning, update the _config.txt_ file with appropriate paths.  
    * Also include desired settings for variant calling.

### Step 1: Download the SRA Accession List
  * Download the desired SRA accession list from the NIH website. The NIH provides publicly available genomic data for download. You can search through various projects that include human WES files for use with this repository. In this example, we are using the following:
    * National Center for Biotechnology Information. BioProject: PRJNA316441. Exome sequencing study on diffuse cutaneous systemic sclerosis. Available at: https://www.ncbi.nlm.nih.gov/bioproject?LinkName=sra_bioproject&from_uid=2391704. Accessed on 01/25/2023.
  * This BioProject contains WES data from 32 patients with diffuse cutaneous systemic sclerosis (dcSSc) and was submitted on 25/Mar/2016 from the University of California San Francisco  

To download the SRA accession list from the NIH website, follow these steps:
  1. Find the desired BioProject or use the example from the above link
  2. Click __SRA__ in the top right, which will take you to a page with links to each individual SRA from the BioProject.
  3. Click the following: __Send to:__ > __File__ > (under __Format__ select __Accession List__) > __Create File__
     * This will download a .csv file containing all SRA IDs under the header "acc". The file should be named "SraAccList.csv".
  4. Place the SraAccList.csv file in the directory where you will be running the rest of the scripts.

### Step 2: Download the FASTQ Files
To download the FASTQ files, run the following command:

`python sradownload.py`

  * This script will create a folder named __SRA__ containing all the paired FASTQ.gz files. Depending on the number of SRA IDs and dedicated threads (see _config.txt_), this script may take a long time, approximately 0.5 to 1 hour per ID.
  
### Step 3: Convert FASTQ.gz to BAM files

To convert the FASTQ.gz files to VCF format, run the following command:

`python fastqtobam.py`
* This will create a folder named __BAM__ with associated BAM files.  

### Step 4: Convert BAM files to VCF

To convert the BAM files to VCF format, run the following command:

`python bamtovcf.py`
* This will create a folder named __VCF__ with associated BAM files.
  
### Step 5: Annotate VCF Files

To annotate the VCF files with dbSNP, dbNSFP, and ClinVar, run the following command:

`python annotate.py`
* For directions on how to download these databases, see the _programs.txt_ file.

### Step 6: Process the Annotated VCF Files

Use the following commands in this order to process the annotated VCF files:

`python filter.py`  
* This extracts information from the VCF files used in the scoring algorithm.  

`python scoring.py`  

* This applies the scoring algorithm to each variant and creates a .txt file with each variant. It also creates an additional .txt file with summed SNP scores located on the same gene.  

`python matchtodiseases.py`  
* This matches each gene with an associated disease and organ system. For genes related to the same disease, gene scores are summed to result in a final disease score.


