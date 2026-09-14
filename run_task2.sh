#!/bin/bash
#SBATCH --job-name=task2_hybrid_test
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=4
#SBATCH --partition=defq

# Load the required MPI module
module load openmpi/4.1.5-gcc-11.2.0-ux65npg

# Set the number of OpenMP threads to match the requested cpus-per-task
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Compile the task2 code (including -fopenmp for OpenMP support)
# Note: You can remove this line once compiled if you don't want it to recompile every run
mpicc -fopenmp task2.c -o task2 -lm

# Run the hybrid executable (4 MPI processes, 4 OpenMP threads each = 16 total parallel units)
srun ./task2 10000000
