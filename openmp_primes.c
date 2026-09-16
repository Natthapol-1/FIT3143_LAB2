/*
 * openmp_primes.c - Parallel prime search using OpenMP (shared memory)
 * This serves as the Week 4 Task 3 comparison baseline for the MPI and Hybrid implementations.
 *
 * Compilation: gcc -O2 -fopenmp openmp_primes.c -o openmp_primes -lm
 * Usage:       OMP_NUM_THREADS=4 ./openmp_primes <n>
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <omp.h>

// Check if a number is prime using trial division up to sqrt(n)
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
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <n>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    if (n <= 2) {
        fprintf(stderr, "Please provide an n > 2\n");
        return 1;
    }

    int num_threads = omp_get_max_threads();

    // Start timing (exclude IO)
    double start_time = omp_get_wtime();

    // Each thread gets its own private dynamic array to avoid critical sections.
    // This is faster than a shared array with omp critical.
    int **thread_primes = (int **)malloc(num_threads * sizeof(int *));
    int *thread_counts = (int *)calloc(num_threads, sizeof(int));
    int *thread_capacity = (int *)malloc(num_threads * sizeof(int));

    if (!thread_primes || !thread_counts || !thread_capacity) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    for (int t = 0; t < num_threads; t++) {
        thread_capacity[t] = 1000;
        thread_primes[t] = (int *)malloc(thread_capacity[t] * sizeof(int));
        if (!thread_primes[t]) {
            fprintf(stderr, "Memory allocation failed for thread %d\n", t);
            return 1;
        }
    }

    // Parallel prime search using OpenMP with guided scheduling.
    // Each thread writes to its OWN private array - no locking needed.
    // schedule(guided) balances the varying workload of checking large vs small numbers.
    #pragma omp parallel for schedule(guided)
    for (int i = 2; i < n; i++) {
        if (is_prime(i)) {
            int tid = omp_get_thread_num();
            // Resize this thread's private array if needed
            if (thread_counts[tid] >= thread_capacity[tid]) {
                thread_capacity[tid] *= 2;
                thread_primes[tid] = (int *)realloc(thread_primes[tid], thread_capacity[tid] * sizeof(int));
                if (!thread_primes[tid]) {
                    fprintf(stderr, "Memory reallocation failed for thread %d\n", tid);
                    exit(1);
                }
            }
            thread_primes[tid][thread_counts[tid]++] = i;
        }
    }

    // Merge all thread-local arrays into a single global array
    int total_primes = 0;
    for (int t = 0; t < num_threads; t++) {
        total_primes += thread_counts[t];
    }

    int *all_primes = (int *)malloc(total_primes * sizeof(int));
    if (!all_primes) {
        fprintf(stderr, "Memory allocation failed for final array\n");
        return 1;
    }

    int offset = 0;
    for (int t = 0; t < num_threads; t++) {
        for (int j = 0; j < thread_counts[t]; j++) {
            all_primes[offset++] = thread_primes[t][j];
        }
        free(thread_primes[t]);
    }

    // Sort the merged array (cyclic iteration means results are unordered)
    qsort(all_primes, total_primes, sizeof(int), compare_ints);

    double end_time = omp_get_wtime();
    printf("[OPENMP] Threads: %d | Time: %f s\n", num_threads, end_time - start_time);
    printf("Total primes found less than %d: %d\n", n, total_primes);

    // Write output to file
    FILE *fp = fopen("openmp_primes_output.txt", "w");
    if (fp == NULL) {
        fprintf(stderr, "Could not open file for writing\n");
    } else {
        for (int i = 0; i < total_primes; i++) {
            fprintf(fp, "%d\n", all_primes[i]);
        }
        fclose(fp);
    }

    // Cleanup
    free(all_primes);
    free(thread_primes);
    free(thread_counts);
    free(thread_capacity);

    return 0;
}
