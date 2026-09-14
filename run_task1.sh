#!/bin/bash
#SBATCH --job-name=task1_test
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --partition=defq

# Load the required MPI module as specified in your slide
module load openmpi/4.1.5-gcc-11.2.0-ux65npg

# Run the executable (we use srun instead of mpirun inside SLURM scripts)
# This runs the task1 executable and passes 100 as the value for 'n'
srun ./task1 100
