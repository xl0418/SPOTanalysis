#!/bin/bash
## now loop through the above array

#SBATCH --time=10:10:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=50G   # memory per CPU core
#SBATCH -J "ColGREst"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

python 05-Collect_GREst_SPOT.py
