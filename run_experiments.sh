#!/bin/bash
#SBATCH --job-name=task3_experiments
#SBATCH --time=01:00:00
#SBATCH --mem=8G
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --partition=defq

module load openmpi/4.1.5-gcc-11.2.0-ux65npg

gcc -O2 serial_primes.c -o serial_primes -lm
mpicc -O2 task1.c -o task1 -lm
mpicc -O2 -fopenmp task2.c -o task2 -lm

OUTPUT_FILE="experiment_results.txt"
echo "=== FIT3143 LAB 2 TASK 3 EXPERIMENTS ===" > $OUTPUT_FILE

# EXPERIMENT A: 30 different values of N (For Graphs 1 & 2)
# We test N from 1,000,000 to 30,000,000 in steps of 1,000,000
echo "=== EXPERIMENT A: Varying N (30 values) ===" | tee -a $OUTPUT_FILE
FIXED_PROCS=4
for i in {1..30}; do
    n=$((i * 1000000))
    echo "Testing N = $n" | tee -a $OUTPUT_FILE
    
    echo "  [Serial]" | tee -a $OUTPUT_FILE
    ./serial_primes $n | grep "Time" | tee -a $OUTPUT_FILE
    
    echo "  [MPI (4 processes)]" | tee -a $OUTPUT_FILE
    export OMP_NUM_THREADS=1
    srun --ntasks=$FIXED_PROCS ./task1 $n | grep "Time" | tee -a $OUTPUT_FILE
done
echo "" | tee -a $OUTPUT_FILE


# EXPERIMENT B: Varying MPI Processes (For Graphs 3 & 6)
# Testing from 1 up to 32 (to see what happens when exceeding physical cores)
echo "=== EXPERIMENT B: Varying MPI Processes ===" | tee -a $OUTPUT_FILE
FIXED_N=20000000
MPI_PROCS=(1 2 4 8 12 16 24 32)
echo "Testing with N = $FIXED_N" | tee -a $OUTPUT_FILE

# Run serial once for baseline
echo "  [Serial Baseline]" | tee -a $OUTPUT_FILE
./serial_primes $FIXED_N | grep "Time" | tee -a $OUTPUT_FILE

for p in "${MPI_PROCS[@]}"; do
    echo "  [MPI ($p processes)]" | tee -a $OUTPUT_FILE
    export OMP_NUM_THREADS=1
    srun --ntasks=$p ./task1 $FIXED_N | grep "Time" | tee -a $OUTPUT_FILE
done
echo "" | tee -a $OUTPUT_FILE


# EXPERIMENT C: Hybrid MPI + OpenMP (For Graphs 4, 5, 7)
# Testing various combinations of processes and threads
echo "=== EXPERIMENT C: Hybrid OpenMPI + OpenMP ===" | tee -a $OUTPUT_FILE
echo "Testing with N = $FIXED_N" | tee -a $OUTPUT_FILE

# We test combinations that result in 4, 8, 16, and 32 total parallel units
# format: "MPI_PROCS OpenMP_THREADS"
HYBRID_CONFIGS=(
    "2 2"  # 4 units
    "4 1"  # 4 units (MPI heavy)
    "1 4"  # 4 units (OpenMP heavy)
    
    "4 2"  # 8 units
    "2 4"  # 8 units
    "8 1"  # 8 units
    
    "4 4"  # 16 units
    "8 2"  # 16 units
    "16 1" # 16 units
    
    "8 4"  # 32 units (oversubscribed if machine has <32 cores)
    "16 2" # 32 units
)

for config in "${HYBRID_CONFIGS[@]}"; do
    read -r p t <<< "$config"
    echo "  [Hybrid ($p processes, $t threads)]" | tee -a $OUTPUT_FILE
    export OMP_NUM_THREADS=$t
    srun --ntasks=$p --cpus-per-task=$t ./task2 $FIXED_N | grep "Time" | tee -a $OUTPUT_FILE
done

echo "Experiments completed successfully!"
