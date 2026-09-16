#!/bin/bash
#SBATCH --job-name=task3_experiments
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --partition=defq

# Load the required MPI module
module load openmpi/4.1.5-gcc-11.2.0-ux65npg

# Compile everything
gcc -O2 serial_primes.c -o serial_primes -lm
mpicc -O2 task1.c -o task1 -lm
mpicc -O2 -fopenmp task2.c -o task2 -lm

OUTPUT_FILE="experiment_results.txt"
echo "=== FIT3143 LAB 2 TASK 3 EXPERIMENTS ===" > $OUTPUT_FILE
echo "Starting experiments..."

# Test parameters
N_VALUES=(1000000 5000000 10000000)
MPI_PROCS=(1 2 4 8 16)
HYBRID_PROCS=(2 4)
HYBRID_THREADS=(2 4)

for n in "${N_VALUES[@]}"; do
    echo "===========================================" | tee -a $OUTPUT_FILE
    echo "Testing N = $n" | tee -a $OUTPUT_FILE
    echo "===========================================" | tee -a $OUTPUT_FILE

    # 1. Serial Baseline
    echo "--- SERIAL ---" | tee -a $OUTPUT_FILE
    ./serial_primes $n | tee -a $OUTPUT_FILE
    echo "" | tee -a $OUTPUT_FILE

    # 2. Task 1: Pure MPI
    echo "--- TASK 1 (MPI Only) ---" | tee -a $OUTPUT_FILE
    for p in "${MPI_PROCS[@]}"; do
        echo "Running with $p MPI processes..." | tee -a $OUTPUT_FILE
        # Reset OMP_NUM_THREADS just in case
        export OMP_NUM_THREADS=1
        srun --ntasks=$p ./task1 $n | tee -a $OUTPUT_FILE
    done
    echo "" | tee -a $OUTPUT_FILE

    # 3. Task 2: Hybrid MPI + OpenMP
    echo "--- TASK 2 (Hybrid MPI + OpenMP) ---" | tee -a $OUTPUT_FILE
    for p in "${HYBRID_PROCS[@]}"; do
        for t in "${HYBRID_THREADS[@]}"; do
            echo "Running with $p MPI processes and $t Threads per process..." | tee -a $OUTPUT_FILE
            export OMP_NUM_THREADS=$t
            # We use srun with specific cpus-per-task to allocate the threads
            srun --ntasks=$p --cpus-per-task=$t ./task2 $n | tee -a $OUTPUT_FILE
        done
    done
    echo "" | tee -a $OUTPUT_FILE

done

echo "Experiments completed successfully!"
