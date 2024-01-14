#!/bin/bash
## now loop through the above array

#SBATCH --time=6-20:10:00   # walltime
#SBATCH --ntasks=32   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "ProkkaSPOT"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

module load parallel/20180222
module load singularity/3.3.0

sh 03-prokka_SPOT_genomes.sh 32 SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv


