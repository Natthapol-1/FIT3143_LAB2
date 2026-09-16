# Task 3 Data for Presentation Graphs

Here is all the data cleanly processed from your experiment results. You can copy and paste these tables directly into your presentation or into Excel/Sheets to plot your 7 graphs!

## Data for Graphs 1 & 2 (Increasing N with 4 MPI Processes)
| N | Serial Time (s) | Open MPI Time (s) | Empirical Speedup |
|---|---|---|---|
| 1000000 | 0.103 | 0.077 | 1.34x |
| 2000000 | 0.270 | 0.168 | 1.61x |
| 3000000 | 0.478 | 0.271 | 1.76x |
| 4000000 | 0.710 | 0.383 | 1.85x |
| 5000000 | 0.980 | 0.536 | 1.83x |
| 6000000 | 1.264 | 0.675 | 1.87x |
| 7000000 | 1.579 | 0.848 | 1.86x |
| 8000000 | 1.912 | 1.007 | 1.90x |
| 9000000 | 2.229 | 1.199 | 1.86x |
| 10000000 | 2.631 | 1.354 | 1.94x |
| 11000000 | 2.960 | 1.535 | 1.93x |
| 12000000 | 3.347 | 1.734 | 1.93x |
| 13000000 | 3.750 | 2.378 | 1.58x |
| 14000000 | 4.162 | 2.493 | 1.67x |
| 15000000 | 4.594 | 2.459 | 1.87x |
| 16000000 | 5.028 | 2.590 | 1.94x |
| 17000000 | 5.478 | 2.818 | 1.94x |
| 18000000 | 5.944 | 3.053 | 1.95x |
| 19000000 | 6.417 | 3.632 | 1.77x |
| 20000000 | 6.904 | 3.671 | 1.88x |
| 21000000 | 7.400 | 3.842 | 1.93x |
| 22000000 | 7.903 | 4.324 | 1.83x |
| 23000000 | 8.423 | 4.633 | 1.82x |
| 24000000 | 8.952 | 4.844 | 1.85x |
| 25000000 | 9.547 | 4.848 | 1.97x |
| 26000000 | 10.031 | 5.437 | 1.85x |
| 27000000 | 10.644 | 5.565 | 1.91x |
| 28000000 | 11.148 | 6.003 | 1.86x |
| 29000000 | 11.699 | 6.295 | 1.86x |
| 30000000 | 12.294 | 6.549 | 1.88x |

## Data for Graphs 3 & 6 (Increasing MPI Processes, N = 20M)
**Baseline Serial Time:** 7.080 s

**Amdahl's Fractions (from 1 MPI process):**
- Serial Fraction (S): **0.0081** (0.8% overhead)
- Parallel Fraction (P): **0.9919** (99.2% parallelizable)

| Processes | MPI Time (s) | Empirical Speedup | Theoretical Speedup (Amdahl) |
|---|---|---|---|
| 1 | 7.028 | 1.01x | 1.00x |
| 2 | 9.131 | 0.78x | 1.98x |
| 4 | 4.191 | 1.69x | 3.91x |
| 8 | 1.992 | 3.55x | 7.57x |
| 12 | 1.983 | 3.57x | 11.02x |
| 16 | 0.982 | 7.21x | 14.27x |
| 24 | 1.008 | 7.02x | 20.23x |
| 32 | 0.805 | 8.79x | 25.58x |

## Data for Graphs 4, 5, & 7 (Hybrid MPI + OpenMP, N = 20M)
| MPI Processes | OpenMP Threads | Total Units | Hybrid Time (s) | Empirical Speedup | Theoretical Speedup (Amdahl) |
|---|---|---|---|---|---|
| 2 | 2 | 4 | 3.798 | 1.86x | 3.91x |
| 4 | 1 | 4 | 3.662 | 1.93x | 3.91x |
| 1 | 4 | 4 | 1.914 | 3.70x | 3.91x |
| 4 | 2 | 8 | 1.976 | 3.58x | 7.57x |
| 2 | 4 | 8 | 1.961 | 3.61x | 7.57x |
| 8 | 1 | 8 | 1.908 | 3.71x | 7.57x |
| 4 | 4 | 16 | 1.043 | 6.79x | 14.27x |
| 8 | 2 | 16 | 1.069 | 6.63x | 14.27x |
| 16 | 1 | 16 | 1.036 | 6.83x | 14.27x |
| 8 | 4 | 32 | 0.633 | 11.19x | 25.58x |
| 16 | 2 | 32 | 0.662 | 10.69x | 25.58x |
