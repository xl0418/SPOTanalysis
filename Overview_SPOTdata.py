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
