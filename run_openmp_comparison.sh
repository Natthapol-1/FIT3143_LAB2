#!/bin/bash
#SBATCH --job-name=openmp_comparison
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --partition=defq

module load openmpi/4.1.5-gcc-11.2.0-ux65npg

# Compile OpenMP baseline
gcc -O2 -fopenmp openmp_primes.c -o openmp_primes -lm

OUTPUT_FILE="openmp_results.txt"
echo "=== OpenMP Comparison Experiments ===" > $OUTPUT_FILE

# --- EXPERIMENT D: Varying N with fixed 4 threads (for Graphs 1 & 2) ---
# This matches Experiment A which used 4 MPI processes, so N values are identical.
echo "=== EXPERIMENT D: OpenMP Varying N (4 threads) ===" | tee -a $OUTPUT_FILE
for i in {1..30}; do
    n=$((i * 1000000))
    echo "Testing N = $n" | tee -a $OUTPUT_FILE
    export OMP_NUM_THREADS=4
    ./openmp_primes $n | grep "\[OPENMP\]" | tee -a $OUTPUT_FILE
done
echo "" | tee -a $OUTPUT_FILE

# --- EXPERIMENT E: OpenMP varying thread count (for Graph 3) ---
# Fixed N=20M, varying thread count to match MPI process counts from Experiment B.
echo "=== EXPERIMENT E: OpenMP Varying Thread Count (N=20M) ===" | tee -a $OUTPUT_FILE
THREAD_COUNTS=(1 2 4 8 12 16)
for t in "${THREAD_COUNTS[@]}"; do
    echo "Testing with $t threads..." | tee -a $OUTPUT_FILE
    export OMP_NUM_THREADS=$t
    ./openmp_primes 20000000 | grep "\[OPENMP\]" | tee -a $OUTPUT_FILE
done
echo "" | tee -a $OUTPUT_FILE

# --- EXPERIMENT F: OpenMP with total thread counts matching Hybrid configs (for Graph 5) ---
# The hybrid configs tested were: 4, 8, 16, 32 total units.
# We run OpenMP with exactly those thread counts so the comparison is fair.
echo "=== EXPERIMENT F: OpenMP matching Hybrid total units (N=20M) ===" | tee -a $OUTPUT_FILE
MATCHING_THREADS=(4 8 16)
for t in "${MATCHING_THREADS[@]}"; do
    echo "Testing with $t threads (matching hybrid total units)..." | tee -a $OUTPUT_FILE
    export OMP_NUM_THREADS=$t
    ./openmp_primes 20000000 | grep "\[OPENMP\]" | tee -a $OUTPUT_FILE
done

echo "OpenMP comparison experiments complete!"
