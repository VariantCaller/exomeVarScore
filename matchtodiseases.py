import pandas as pd
import csv
import os
import subprocess

# Read the paths and settings from the config file
with open('config.txt') as f:
    config = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

samples = config['SAMPLE_NAMES']
disgenet_path = config['KEGG_DisGenet']
kegg_hpo_path = config['KEGG_HPO_DisGenet']


# Create the output directories if they don't exist
if not os.path.exists('DISEASES'):
    os.makedirs('DISEASES')


# Open the CSV file containing the SRA ID numbers
with open(f'{samples}', newline='') as csvfile:
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    # Loop through each row in the file
    for row in reader:
        # Extract the SRA ID from the "acc" column
        sra_id = row['acc']

        # define file paths and names
        text = "example"
        gene_scores_path = f"SCORED/{sra_id}.GeneScores.txt"
        disgenet_output_path = f"DISEASES/{sra_id}.MatchedDisGenetOnly.txt"
        kegg_hpo_output_path = f"DISEASES/{sra_id}.MatchedHPODisGenet.txt"

        # load gene scores into pandas dataframe
        gene_scores_df = pd.read_csv(gene_scores_path, sep="\t")


        # load DisGeNET database into pandas dataframe and merge with sorted gene scores
        disgenet_df = pd.read_csv(disgenet_path, sep="\t")
        matched_disgenet_df = pd.merge(disgenet_df, gene_scores_df, left_on=["gene_symbol"], right_on=["Gene.Name"])

        # change headers to DiseaseScr
        matched_disgenet_df = matched_disgenet_df.rename(columns={"GeneScr" + str(i): "DiseaseScr" + str(i) for i in range(1, 13)})
        
        # write matched DisGeNET output to file
        matched_disgenet_df.to_csv(disgenet_output_path, sep="\t", index=False)

        # load KEGG and HPO databases into pandas dataframes and merge with sorted gene scores
        kegg_hpo_df = pd.read_csv(kegg_hpo_path, sep="\t")
        matched_kegg_hpo_df = pd.merge(kegg_hpo_df, gene_scores_df, left_on=["gene_symbol"], right_on=["Gene.Name"])

        # change headers to DiseaseScr
        matched_kegg_hpo_df = matched_kegg_hpo_df.rename(columns={"GeneScr" + str(i): "DiseaseScr" + str(i) for i in range(1, 13)})

        # write matched KEGG and HPO output to file
        matched_kegg_hpo_df.to_csv(kegg_hpo_output_path, sep="\t", index=False)

