import numpy as np
import pandas as pd

# read BLAST output
spot_blast = pd.read_csv("data/SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv", sep='\t', header=None)

# the number of unique tags in SPOT dataset
no_tags_blast = spot_blast.iloc[:,0].nunique()
tags_blast = spot_blast.iloc[:,0].unique()

# read domain identity file
spot_data = pd.read_csv("data/SPOT_Prokaryotic16S_ASV_Domain_identity.csv", sep=',')
# remove '>' from the beginning of the tag
spot_data.iloc[:,0] = spot_data.iloc[:,0].str.replace(">", "")

# read fasta file
spot_fasta = pd.read_csv("data/SPOT_Prokaryotic16S_ASV_dna-sequences.fasta", sep='\t', header=None)
# extract the string starting with '>'
tags_fasta = [i[1:] for i in spot_fasta.iloc[:,0] if i.startswith('>')]

# the number of unique tags in SPOT fasta file
no_tags_fasta = len(tags_fasta)

no_tags_domain = spot_data.iloc[:,0].nunique()
tags_domain = spot_data.iloc[:,0].unique()

# the tags in tags_blast but not in tags_domain
tags_in_blast_not_in_domain = set(tags_blast) - set(tags_domain)

tags_in_domain_not_in_blast = set(tags_domain) - set(tags_blast)

print("Number of tags in BLAST output: ", no_tags_blast)

print("Number of tags in domain identity file: ", no_tags_domain)

print("Number of tags in fasta file: ", no_tags_fasta)

print("Number of tags in BLAST output but not in domain identity file: ", len(tags_in_blast_not_in_domain))

print("Number of tags in domain identity file but not in BLAST output: ", len(tags_in_domain_not_in_blast))

# number of genomes in blast output
no_genomes_blast = spot_blast.iloc[:,1].nunique()

file_relative_a_FL = 'data/SPOT_FreeLivingProkaroytes_ASV_2005_2018_5depths.csv'
tag2sample_FL = pd.read_csv(file_relative_a_FL, sep=',')

# number of unique tags in tag2sample
no_tags_relative_a = tag2sample_FL.index.nunique()

file_relative_a_PA = 'data/SPOT_ParticleAssocaitedProkaroytes_ASV_2005_2018_5depths.csv'
tag2sample_PA = pd.read_csv(file_relative_a_PA, sep=',')

# number of unique tags in tag2sample
no_tags_relative_a_PA = tag2sample_PA.index.nunique()

# tags in tag2sample_PA.index but not in tag2sample_FL.index
tags_in_PA_not_in_FL = set(tag2sample_PA.index) - set(tag2sample_FL.index)

# tags in domain identity file but not in tag2sample_FL.index
tags_in_domain_not_in_FL = set(tags_domain) - set(tag2sample_FL.index)

# tags in blast output but not in tag2sample_FL.index
tags_in_blast_not_in_FL = set(tags_blast) - set(tag2sample_FL.index)

# tags in blast output and also in tag2sample_FL.index
tags_in_blast_and_FL = set(tags_blast) & set(tag2sample_FL.index)

spot_blast_FL = spot_blast[spot_blast.iloc[:,0].isin(tags_in_blast_and_FL)]

# number of unique tags in spot_blast_FL
no_tags_blast_FL = spot_blast_FL.iloc[:,0].nunique()
# number of unique genomes in spot_blast_FL
no_genomes_blast_FL = spot_blast_FL.iloc[:,1].nunique()

# read SPOT_fullhits_FL.csv
spot_fullhits_FL = pd.read_csv("data/SPOT_fullhits_FL.csv", sep=',')
# number of unique tags in spot_fullhits_FL
no_tags_fullhits_FL = spot_fullhits_FL['tag'].nunique()
# number of unique genomes in spot_fullhits_FL
no_genomes_fullhits_FL = spot_fullhits_FL['genomeid'].nunique()

# read SPOT_fullhits_PA.csv
spot_fullhits_PA = pd.read_csv("data/SPOT_fullhits_PA.csv", sep=',')
# number of unique tags in spot_fullhits_PA
no_tags_fullhits_PA = spot_fullhits_PA['tag'].nunique()
# number of unique genomes in spot_fullhits_PA
no_genomes_fullhits_PA = spot_fullhits_PA['genomeid'].nunique()

genomes_fullhits_FL = spot_fullhits_FL['genomeid'].unique()
genomes_fullhits_PA = spot_fullhits_PA['genomeid'].unique()

# number of unique genomes in both spot_fullhits_FL and spot_fullhits_PA
no_genomes_fullhits_FL_PA = len(np.unique(np.concatenate((genomes_fullhits_FL, genomes_fullhits_PA))))

# number of unique tags in both spot_fullhits_FL and spot_fullhits_PA
no_tags_fullhits_FL_PA = len(np.unique(np.concatenate((spot_fullhits_FL['tag'].unique(), spot_fullhits_PA['tag'].unique()))))