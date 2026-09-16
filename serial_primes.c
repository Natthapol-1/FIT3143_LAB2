#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <sys/time.h>

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

// Helper to get time in seconds
double get_time() {
    struct timeval t;
    gettimeofday(&t, NULL);
    return t.tv_sec + t.tv_usec / 1000000.0;
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

    // Start timer
    double start_time = get_time();

    int capacity = 1000;
    int *primes = (int *)malloc(capacity * sizeof(int));
    if (primes == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    int count = 0;

    // Check all numbers up to n
    for (int i = 2; i < n; i++) {
        if (is_prime(i)) {
            if (count >= capacity) {
                capacity *= 2;
                primes = (int *)realloc(primes, capacity * sizeof(int));
                if (primes == NULL) {
                    fprintf(stderr, "Memory reallocation failed\n");
                    return 1;
                }
            }
            primes[count++] = i;
        }
    }

    // End timer
    double end_time = get_time();
    double time_taken = end_time - start_time;

    printf("[SERIAL] Time taken: %f seconds\n", time_taken);
    printf("[SERIAL] Total primes found less than %d: %d\n", n, count);

    // Write to output file
    FILE *fp = fopen("serial_primes_output.txt", "w");
    if (fp == NULL) {
        fprintf(stderr, "Could not open file for writing\n");
    } else {
        for (int i = 0; i < count; i++) {
            fprintf(fp, "%d\n", primes[i]);
        }
        fclose(fp);
    }

    free(primes);
    return 0;
}
