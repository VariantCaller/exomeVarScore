# Required programs to run each script with links and commands to download them.


# sradownload.py

fasterq-dump - This is part of the SRA Toolkit, which can be downloaded from the NCBI website (https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software).

# sratovcf.py

bwa - A software package for mapping low-divergent sequences against a large reference genome. You can download it from the official website: http://bio-bwa.sourceforge.net/ or https://github.com/lh3/bwa

samtools - A suite of programs for interacting with high-throughput sequencing data in the SAM/BAM format. You can download it from the official website: http://www.htslib.org/
	or with command:
	Linux: sudo apt-get install samtools
	macOS: brew install samtools

freebayes - A Bayesian genetic variant detector designed to find small polymorphisms, specifically SNPs (single-nucleotide polymorphisms), indels (insertions and deletions), MNPs (multi-nucleotide polymorphisms), and complex events (composite insertion and substitution events) smaller than the length of a short-read sequencing alignment. You can download it from the official GitHub repository: https://github.com/ekg/freebayes


# annotate.py

snpEff - This is a program for annotating and predicting the effects of genetic variants. You can download it from the official website (http://snpeff.sourceforge.net/) and install it on your system.
	or with commands:
	wget https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip
	unzip snpEff_latest_core.zip

SnpSift - This is a program for filtering and manipulating annotated variants. It is part of the SnpEff software package, so you don't need to download it separately.

# To download databases required for annotation see below!


# filter.py

SnpSift - see above in annotate.py.

bcftools - This is a package for manipulating VCF and BCF files. It can be downloaded from the bcftools website: https://samtools.github.io/bcftools/. To install it, follow the instructions provided on the website.

awk - This is a command-line tool for manipulating text files. It is typically included in Unix-based operating systems, such as Linux and macOS. If you are using Windows, you can install it using a tool like Cygwin or the Windows Subsystem for Linux.

sed - This is a command-line tool for manipulating text files. It is typically included in Unix-based operating systems, such as Linux and macOS. If you are using Windows, you can install it using a tool like Cygwin or the Windows Subsystem for Linux.


# matchtodiseases.py

pandas - Pandas is a Python library for data manipulation and analysis that provides data structures and functions for working with structured data, such as spreadsheets and relational databases. Pandas can be installed using pip, a Python package installer.
	Use command
	pip install pandas


# scoring.py
pandas - see above in matchtodiseases.py



# Databases to download for vcf annotation. Must create tabix index after download.

dbSNP
wget --timeout=5 -c https://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/All_20180423.vcf.gz
tabix -p vcf All_20180423.vcf.gz

dbNSFP
wget --timeout=5 -c https://snpeff.blob.core.windows.net/databases/dbs/GRCh37/dbNSFP_4.1a/dbNSFP4.1a.txt.gz.tbi

wget --timeout=5 -c https://snpeff.blob.core.windows.net/databases/dbs/GRCh37/dbNSFP_4.1a/dbNSFP4.1a.txt.gz

ClinVar
wget --timeout=5 -c https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar_20230318.vcf.gz
tabix -p vcf clinvar_20230318.vcf.gz
