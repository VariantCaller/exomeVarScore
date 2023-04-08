import os
import re
import pandas as pd
import csv
import numpy as np
import math


# Read the paths and settings from the config file
with open('config.txt') as f:
    config = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

samples = config['SAMPLE_NAMES']
clear_dump = config.get('CLEAR_DUMP', False)

# Create the output directories if they don't exist
if not os.path.exists('SCORED/dump'):
    os.makedirs('SCORED/dump')

# Open the CSV file containing the SRA ID numbers
with open(f'{samples}', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    # Loop through each row in the file
    for row in reader:
        # Extract the SRA ID from the "acc" column
        sra_id = row['acc']
        # Iterate over the SRA IDs and perform the analysis
        
        # Assigning Weights
        with open(f"FILTERED/{sra_id}.filtered.txt", "r") as f:
            lines = f.readlines()

        with open(f"SCORED/dump/{sra_id}.weightAdded.txt", "w") as f:
            for i, line in enumerate(lines):
                if i == 0:
                    f.write(line.strip() + "\tWEIGHT\n")
                else:
                    data = line.strip().split("\t")
                    if any(x in data[9] for x in ["transcript_ablation", "curator_inference", "trinucleotide_repeat_expansion"]):
                        data.append("1")
                    elif any(x in data[9] for x in ["start_lost", "frameshift_variant", "stop_gained", "splice_region_variant", "splice_acceptor_variant", "splice_donor_variant", "coding_sequence_variant"]):
                        data.append(".95")
                    elif any(x in data[9] for x in ["incomplete_terminal_codon_variant", "stop_lost"]):
                        data.append(".9")
                    elif any(x in data[9] for x in ["protein_altering_variant", "missense_variant", "initiator_codon_variant", "inframe_deletion", "inframe_insertion", "disruptive_inframe_insertion", "sequence_feature", "disruptive_inframe_deletion", "protein_protein_contact"]):
                        data.append(".7")
                    elif any(x in data[9] for x in ["non_coding_transcript_exon_variant", "NMD_transcript_variant", "intron_variant", "mature_miRNA_variant", "3_prime_UTR_variant", "5_prime_UTR_variant", "non_coding_transcript_exon_variant", "synonymous_variant", "stop_retained_variant", "structural_interaction_variant", "5_prime_UTR_premature_start_codon_gain_variant"]):
                        data.append(".65")
                    elif any(x in data[9] for x in ["regulatory_region_variant", "upstream_gene_variant", "downstream_gene_variant", "TF_binding_site_variant", "transcript_amplification", "regulatory_region_amplification", "TFBS_amplification", "regulatory_region_ablation", "TFBS_ablation", "feature_truncation", "feature_elongation", "intragenic_variant"]):
                        data.append(".6")
                    elif any(x in data[9] for x in ["Regulatory_nearest_gene_five_prime_end", "Nearest_gene_five_prime_end", "downstream_gene_variant", "sequence_variant", "conservative_inframe_deletion", "conservative_inframe_insertion"]):
                        data.append(".5")
                    else:
                        data.append("0")
                    f.write("\t".join(data) + "\n")
        
        with open(f"SCORED/dump/{sra_id}.weight.txt", "w") as f:
            with open(f"SCORED/dump/{sra_id}.weightAdded.txt", "r") as f1:
                lines = f1.readlines()
            for line in lines:
                if line.split("\t")[-1] != "0\n":
                    f.write(line)

        #Genotype
        with open(f"SCORED/dump/{sra_id}.weight.txt", "r") as infile:
            with open(f"SCORED/dump/{sra_id}.GT.txt", "w") as outfile:
                for i, line in enumerate(infile):
                    fields = line.strip().split("\t")
                    if i == 0:
                        fields.append("GT")
                        outfile.write("\t".join(fields) + "\n")
                    else:
                        gt = ""
                        if fields[4] in ["1/0", "0/1", "0/2", "2/0"]:
                            gt = ".5"
                        elif fields[4] == "1/1" or fields[4] == "1/2" or fields[4] == "2/1":
                            gt = "1"
                        else:
                            gt = "0"
                        fields.append(gt)
                        outfile.write("\t".join(fields) + "\n")


        # define the input and output file paths
        input_file = f"SCORED/dump/{sra_id}.GT.txt"
        output_file = f"SCORED/dump/{sra_id}.NoTOT.txt"

        # open input and output files
        with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
            header = f_in.readline().strip().split("\t")
            # append the additional columns to the header
            header += ["SIFT.FATHMM", "PROVEAN.D", "Polyphen2.MutationTaster", "CADD", "GERP5.5", "ClinVar.Pathogenic", "HighImpact", "AF2percent", "AF.5percent"]
            f_out.write("\t".join(header) + "\n")
    
            for line in f_in:
                fields = line.strip().split("\t")
                # check the conditions and add corresponding points
                points = []
                if "D" in fields[13] or "D" in fields[16]:
                    points.append("1")
                else:
                    points.append("0")
                if "D" in fields[14]:
                    points.append("1")
                else:
                    points.append("0")
                if "D" in fields[15] or "D" in fields[19] or "A" in fields[19]:
                    points.append("1")
                else:
                    points.append("0")
                if fields[20] != '.' and float(fields[20]) >= 40:
                    points.append("3")
                elif fields[20] != '.' and float(fields[20]) >= 30:
                    points.append("2")
                elif fields[20] != '.' and float(fields[20]) >= 20:
                    points.append("1")
                else:
                    points.append("0")
                if fields[21] != '.' and fields[21] != '-' and float(fields[21]) >= 5.5:
                    points.append("1")
                else:
                    points.append("0")
                if re.search(r"Pathogenic|Likely_pathogenic", fields[11]):
                    points.append(2)
                else:
                    points.append(0)
                if re.search(r"HIGH", fields[10]) and not re.search(r"structural_interaction_variant|protein_protein_contact", fields[10]):
                    points.append(1)
                else:
                    points.append(0)
                af = fields[12]
                if af == "NA" or af == "." or math.isnan(float(af)):
                    points.append(0)
                elif float(af) <= 0.02:
                    points.append(1)
                else:
                    points.append(0)

                af = fields[12]
                if af == "NA" or af == "." or math.isnan(float(af)):
                    points.append(0)
                elif float(af) <= 0.005:
                    points.append(1)
                else:
                    points.append(0)

                if any(points):
                    f_out.write("\t".join(fields + [str(p) for p in points]) + "\n")


        # define the input and output file paths
        input_file = f"SCORED/dump/{sra_id}.NoTOT.txt"
        output_file = f"SCORED/{sra_id}.Finalscr.txt"

        # open input and output files
        with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
            header = f_in.readline().strip().split("\t")
            # append the additional columns to the header
            header += ["PointTotal"]
            f_out.write("\t".join(header) + "\n")

            for line in f_in:
                fields = line.strip().split("\t")
                # get the points for the current row
                points = fields[24:]
                # convert the points to integers
                points = [int(p) if p.isdigit() else 0 for p in points]
                # compute the total points for the current row
                tot_point_sum = sum(points)
                # append the total points to the points list
                points = [tot_point_sum]
                # check if the last value in the points list is 0
                if points[-1] == 0:
                    continue
                # write the fields and points to the output file
                f_out.write("\t".join(fields + [str(p) for p in points]) + "\n")


        # define input and output file paths
        input_file = f"SCORED/{sra_id}.Finalscr.txt"
        output_file = f"SCORED/{sra_id}.SnpScores.txt"

        # read input file into pandas dataframe
        df = pd.read_csv(input_file, sep="\t")
        
        # sort dataframe by PointTotal in descending order
        df = df.sort_values(by=["PointTotal"], ascending=False)

        # define header for output file
        header = ["Gene.Name", "ID", "PointTotal", "WEIGHT"]
        header += [f"SNPScr{i}" for i in range(1, 13)]
        header.append("NoFreqSnpScr")

        # define list to hold rows for output file
        output_rows = []

        # iterate over rows in dataframe
        for index, row in df.iterrows():
            # calculate SNP scores for current row
            snp_scores = []
            for i in range(1, 13):
                if row["PointTotal"] >= i and row["AF2percent"] == 1:
                    snp_scores.append(row["WEIGHT"] * row["PointTotal"])
                else:
                    snp_scores.append(0)

            # calculate NoFreqSnpScr for current row
            if row["AF2percent"] == 0:
                no_freq_snp_scr = row["WEIGHT"] * row["PointTotal"]
            else:
                no_freq_snp_scr = 0

            # append row to output list
            output_rows.append([row["Gene.Name"], row["ID"], row["PointTotal"], row["WEIGHT"]] + snp_scores + [no_freq_snp_scr])

        # write output file
        with open(output_file, "w") as f_out:
            f_out.write("\t".join(header) + "\n")
            for row in output_rows:
                f_out.write("\t".join(str(r) for r in row[:-1]) + "\t" + "\t".join(str(r) for r in row[-1:]) + "\n")


        # define input and output file paths
        input_file = f"SCORED/{sra_id}.SnpScores.txt"
        output_file = f"SCORED/{sra_id}.GeneScores.txt"

        # read input file into pandas dataframe
        df = pd.read_csv(input_file, sep="\t")


        # define header for output file
        header = ["Gene.Name"]
        header += [f"GeneScr{i}" for i in range(1, 13)]
        header.append("NoFreqGeneScr")
        
        # define dictionary to hold gene scores
        gene_scores = {}

        # iterate over rows in dataframe
        for index, row in df.iterrows():
            gene = row["Gene.Name"]
            if gene not in gene_scores:
                gene_scores[gene] = [0] * 13
            for i in range(1, 13):
                gene_scores[gene][i-1] += row[f"SNPScr{i}"]
            gene_scores[gene][-1] += row["NoFreqSnpScr"]

        # write output file
        with open(output_file, "w") as f_out:
            f_out.write("\t".join(header) + "\n")
            for gene, scores in gene_scores.items():
                output_row = [gene] + [str(score) for score in scores]
                f_out.write("\t".join(output_row) + "\n")

# Clear the dump folder if specified in config
if config.get('CLEAR_DUMP_FOLDER', 'False').lower() == 'true':
    os.system('rm -rf SCORED/dump/*')
