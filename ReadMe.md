# Data

1. The file "**SPOT_Prokaryotic16S_ASV_dna-sequences.fasta**" contains ASV sequences data.

2. Blasting process used GTDB r207 "**GTDB-blastdb/220613_bac-arc-r207_merged.fna**" and produces the output file "**SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv**"



# Scripts

1. "**01-blast-SPOT.sh**" blasts the ASVs in the file "**SPOT_Prokaryotic16S_ASV_dna-sequences.fasta**" and produces identified genomes, "**SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv**". The arguments are **-perc_identity 95 -qcov_hsp_perc 100**;




# Processes