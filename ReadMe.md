# Data

1. The file "**SPOT_Prokaryotic16S_ASV_dna-sequences.fasta**" contains ASV sequences data;

2. Blasting process used GTDB r207 "**GTDB-blastdb/220613_bac-arc-r207_merged.fna**" and produces the output file "**SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv**";

3. The file "**SPOT_Prokaryotic16S_ASV_Domain_identity.csv**" provides taxonomy for each ASV;



# Scripts

All the scripts named after "**sub_XXX**" are to submit jobs to the cluster.

1. "**01-blast-SPOT.sh**" compares the ASVs in the file "**SPOT_Prokaryotic16S_ASV_dna-sequences.fasta**" with GTDB r207 and produces identified genomes, "**SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv**".

2. "**02-SPOT_getgenome_parallel.sh**" downloads full genomes according to the blast output;

3. "**03-prokka_SPOT_genomes.sh**" exploits [Prokka](https://github.com/tseemann/prokka) to annotate genomes according to the taxonomy provided for ASVs; 


# Processes

1. Blastn ASVs against GTDB r207 with a percent identity 95 and a query coverage 100, -- **Script 01**;

2. Download full genomes from [NCBI](https://www.ncbi.nlm.nih.gov/) using [NCBI Datasets](https://www.ncbi.nlm.nih.gov/datasets/) -- **Script 02**;

3. Annotating genomes given the taxonomy of ASVs. -- **Script 03**;