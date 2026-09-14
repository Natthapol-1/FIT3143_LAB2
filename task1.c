#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

// Function to check if a number is prime
bool is_prime(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i <= sqrt(n); i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// Comparison function for qsort
int compare_ints(const void *a, const void *b) {
    int int_a = *((int *)a);
    int int_b = *((int *)b);
    if (int_a == int_b) return 0;
    return (int_a < int_b) ? -1 : 1;
}

int main(int argc, char *argv[]) {
    int rank, size;
    int n = 0;
    double start_time, end_time;

    // Initialize MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Root process reads 'n' from command line
    if (rank == 0) {
        if (argc != 2) {
            fprintf(stderr, "Usage: %s <n>\n", argv[0]);
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        n = atoi(argv[1]);
        if (n <= 2) {
            fprintf(stderr, "Please provide an n > 2\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        start_time = MPI_Wtime(); // Start timer
    }

    // Broadcast 'n' to all processes
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Dynamically allocate array for local primes
    int capacity = 1000;
    int *local_primes = (int *)malloc(capacity * sizeof(int));
    if (local_primes == NULL) {
        fprintf(stderr, "Memory allocation failed on rank %d\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    int local_count = 0;

    // Cyclic workload distribution
    for (int i = 2 + rank; i < n; i += size) {
        if (is_prime(i)) {
            if (local_count >= capacity) {
                capacity *= 2;
                local_primes = (int *)realloc(local_primes, capacity * sizeof(int));
                if (local_primes == NULL) {
                    fprintf(stderr, "Memory reallocation failed on rank %d\n", rank);
                    MPI_Abort(MPI_COMM_WORLD, 1);
                }
            }
            local_primes[local_count++] = i;
        }
    }

    // Root gathers the counts of primes from each process
    int *counts = NULL;
    int *displs = NULL;
    int total_primes = 0;

    if (rank == 0) {
        counts = (int *)malloc(size * sizeof(int));
        displs = (int *)malloc(size * sizeof(int));
    }

    MPI_Gather(&local_count, 1, MPI_INT, counts, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Root calculates total primes and displacements for Gatherv
    int *all_primes = NULL;
    if (rank == 0) {
        for (int i = 0; i < size; i++) {
            displs[i] = total_primes;
            total_primes += counts[i];
        }
        all_primes = (int *)malloc(total_primes * sizeof(int));
    }

    // Gather all prime numbers into the root process
    MPI_Gatherv(local_primes, local_count, MPI_INT, all_primes, counts, displs, MPI_INT, 0, MPI_COMM_WORLD);

    // Root sorts and writes to file
    if (rank == 0) {
        // Sort the collected primes (due to cyclic distribution, they are not globally sorted)
        qsort(all_primes, total_primes, sizeof(int), compare_ints);
        
        end_time = MPI_Wtime(); // Stop timer
        printf("Time taken: %f seconds\n", end_time - start_time);
        printf("Total primes found less than %d: %d\n", n, total_primes);

        // Write to output file
        FILE *fp = fopen("primes_output.txt", "w");
        if (fp == NULL) {
            fprintf(stderr, "Could not open file for writing\n");
        } else {
            for (int i = 0; i < total_primes; i++) {
                fprintf(fp, "%d\n", all_primes[i]);
            }
            fclose(fp);
            printf("Results written to primes_output.txt\n");
        }

        free(counts);
        free(displs);
        free(all_primes);
    }

    // Cleanup
    free(local_primes);
    MPI_Finalize();

    return 0;
}
