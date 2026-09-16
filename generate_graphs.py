"""
generate_graphs.py - Generates all 7 required presentation graphs from experiment data.
Run: python generate_graphs.py
Requires: pip install matplotlib
Output: 7 PNG files ready to paste into your slides.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'lines.linewidth': 2,
    'lines.markersize': 6,
})

# ============================================================
# RAW DATA
# ============================================================

n_values = list(range(1_000_000, 31_000_000, 1_000_000))

serial_times = [
    0.102636, 0.269660, 0.478435, 0.710361, 0.979611,
    1.263734, 1.579146, 1.912144, 2.228596, 2.630511,
    2.960195, 3.347243, 3.749838, 4.161630, 4.594271,
    5.028043, 5.478487, 5.943717, 6.417095, 6.904277,
    7.400371, 7.902706, 8.423128, 8.951760, 9.546637,
    10.031483, 10.644161, 11.147629, 11.699289, 12.294294,
]

mpi4_times = [
    0.076701, 0.167625, 0.271371, 0.383018, 0.536242,
    0.675289, 0.848347, 1.007304, 1.198743, 1.353555,
    1.535287, 1.733577, 2.377963, 2.493425, 2.458809,
    2.589815, 2.817773, 3.053069, 3.631677, 3.671295,
    3.842217, 4.323842, 4.632731, 4.844413, 4.847622,
    5.436640, 5.564915, 6.002762, 6.295243, 6.549268,
]

openmp4_times = [
    0.030103, 0.076467, 0.132485, 0.195153, 0.264302,
    0.340498, 0.418858, 0.505354, 0.595388, 0.689674,
    0.786291, 0.886975, 0.992977, 1.105724, 1.212271,
    1.325448, 1.442315, 1.561672, 1.686252, 1.812821,
    1.938662, 2.069472, 2.200666, 2.338031, 2.472516,
    2.633065, 2.756162, 2.902387, 3.046093, 3.209926,
]

# Experiment B: varying MPI processes, N=20M
serial_20m = 7.079914
mpi_procs =    [1,       2,       4,       8,       12,      16,      24,      32     ]
mpi_times_b =  [7.028286,9.131119,4.191475,1.992068,1.982993,0.982471,1.008448,0.805180]

# Experiment E: varying OpenMP threads, N=20M
omp_threads =  [1,       2,       4,       8,       12,      16     ]
omp_times_e =  [6.966146,3.556355,1.811547,0.942908,0.659627,0.518172]

# Experiment C: Hybrid configs, N=20M (total_units, time)
hybrid_data = {
    4:  {'configs': ['2P×2T','4P×1T','1P×4T'], 'times': [3.798102, 3.661510, 1.913556]},
    8:  {'configs': ['4P×2T','2P×4T','8P×1T'], 'times': [1.975805, 1.961485, 1.907972]},
    16: {'configs': ['4P×4T','8P×2T','16P×1T'],'times': [1.042985, 1.068663, 1.036060]},
    32: {'configs': ['8P×4T','16P×2T'],         'times': [0.632807, 0.662305]},
}

# Amdahl parameters from 1-process MPI run
S = 0.0081
P = 0.9919

def amdahl(n, S, P):
    return 1.0 / (S + P / n)

# ============================================================
# GRAPH 1: Runtime comparison (Serial vs OpenMP vs MPI), increasing N
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
n_labels = [f"{v//1_000_000}M" for v in n_values]
ax.plot(n_labels, serial_times,   'o-', color='#e74c3c', label='Serial')
ax.plot(n_labels, mpi4_times,     's-', color='#3498db', label='Open MPI (4 processes)')
ax.plot(n_labels, openmp4_times,  '^-', color='#2ecc71', label='OpenMP (4 threads)')
ax.set_title('Graph 1: Runtime Comparison — Serial vs OpenMP vs Open MPI\n(Fixed 4 processes/threads, increasing N)')
ax.set_xlabel('Problem Size (N)')
ax.set_ylabel('Wall-clock Time (seconds)')
ax.set_xticks(range(0, 30, 3))
ax.set_xticklabels([f"{v//1_000_000}M" for v in n_values[::3]])
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph1_runtime.png')
plt.close()
print("Saved graph1_runtime.png")

# ============================================================
# GRAPH 2: Empirical speedup (OpenMP vs MPI), increasing N
# ============================================================
mpi_speedup_n   = [s/m for s,m in zip(serial_times, mpi4_times)]
openmp_speedup_n = [s/o for s,o in zip(serial_times, openmp4_times)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(n_labels, openmp_speedup_n, '^-', color='#2ecc71', label='OpenMP (4 threads)')
ax.plot(n_labels, mpi_speedup_n,    's-', color='#3498db', label='Open MPI (4 processes)')
ax.axhline(y=4.0, color='gray', linestyle='--', alpha=0.5, label='Linear ideal (4x)')
ax.set_title('Graph 2: Empirical Speedup — OpenMP vs Open MPI\n(Fixed 4 processes/threads, increasing N)')
ax.set_xlabel('Problem Size (N)')
ax.set_ylabel('Speedup (vs Serial)')
ax.set_xticks(range(0, 30, 3))
ax.set_xticklabels([f"{v//1_000_000}M" for v in n_values[::3]])
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph2_speedup_n.png')
plt.close()
print("Saved graph2_speedup_n.png")

# ============================================================
# GRAPH 3: Empirical speedup (MPI vs OpenMP), increasing parallelism, N=20M
# ============================================================
mpi_speedup_b  = [serial_20m / t for t in mpi_times_b]
omp_speedup_e  = [serial_20m / t for t in omp_times_e]

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(omp_threads, omp_speedup_e,  '^-', color='#2ecc71', label='OpenMP (N=20M)')
ax.plot(mpi_procs[:len(omp_threads)], mpi_speedup_b[:len(omp_threads)], 's-', color='#3498db', label='Open MPI (N=20M)')
ideal_x = [1,2,4,8,12,16]
ax.plot(ideal_x, ideal_x, 'k--', alpha=0.3, label='Linear ideal')
ax.set_title('Graph 3: Empirical Speedup — MPI vs OpenMP\n(Increasing processes/threads, N=20M)')
ax.set_xlabel('Number of Processes / Threads')
ax.set_ylabel('Speedup (vs Serial)')
ax.set_xticks(omp_threads)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph3_speedup_procs.png')
plt.close()
print("Saved graph3_speedup_procs.png")

# ============================================================
# GRAPH 4: Hybrid vs Pure MPI speedup, increasing total units, N=20M
# ============================================================
# Best hybrid time per total unit count
hybrid_units  = [4,    8,    16,   32  ]
hybrid_best   = [min(hybrid_data[u]['times']) for u in hybrid_units]
hybrid_sp     = [serial_20m / t for t in hybrid_best]

# MPI at matching process counts
mpi_match_units = [4, 8, 16, 32]
mpi_match_times = [4.191475, 1.992068, 0.982471, 0.805180]
mpi_match_sp    = [serial_20m / t for t in mpi_match_times]

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(hybrid_units, hybrid_sp,    'D-', color='#9b59b6', label='Hybrid MPI+OpenMP (best config)')
ax.plot(mpi_match_units, mpi_match_sp, 's-', color='#3498db', label='Pure Open MPI')
ax.set_title('Graph 4: Empirical Speedup — Hybrid vs Pure MPI\n(Increasing total parallel units, N=20M)')
ax.set_xlabel('Total Parallel Units (Processes × Threads)')
ax.set_ylabel('Speedup (vs Serial)')
ax.set_xticks(hybrid_units)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph4_hybrid_vs_mpi.png')
plt.close()
print("Saved graph4_hybrid_vs_mpi.png")

# ============================================================
# GRAPH 5: Hybrid vs OpenMP speedup, matching total units, N=20M
# ============================================================
match_units    = [4,       8,       16     ]
omp_match_sp   = [serial_20m/1.811287, serial_20m/0.943129, serial_20m/0.527245]
hybrid_match_best = [
    min(hybrid_data[4]['times']),
    min(hybrid_data[8]['times']),
    min(hybrid_data[16]['times']),
]
hybrid_match_sp = [serial_20m / t for t in hybrid_match_best]

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(match_units, omp_match_sp,    '^-', color='#2ecc71', label='OpenMP')
ax.plot(match_units, hybrid_match_sp, 'D-', color='#9b59b6', label='Hybrid MPI+OpenMP (best config)')
ax.set_title('Graph 5: Empirical Speedup — Hybrid vs OpenMP\n(Matching total thread count, N=20M)')
ax.set_xlabel('Total Parallel Units (matching thread count)')
ax.set_ylabel('Speedup (vs Serial)')
ax.set_xticks(match_units)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph5_hybrid_vs_openmp.png')
plt.close()
print("Saved graph5_hybrid_vs_openmp.png")

# ============================================================
# GRAPH 6: MPI — Empirical vs Theoretical speedup, N=20M
# ============================================================
mpi_emp_sp   = [serial_20m / t for t in mpi_times_b]
mpi_theo_sp  = [amdahl(p, S, P) for p in mpi_procs]

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(mpi_procs, mpi_emp_sp,  's-', color='#3498db', label="Empirical Speedup")
ax.plot(mpi_procs, mpi_theo_sp, 's--', color='#e74c3c', label="Theoretical Speedup (Amdahl's Law)")
ax.set_title("Graph 6: Open MPI — Empirical vs Theoretical Speedup\n(Increasing processes, N=20M)")
ax.set_xlabel('Number of MPI Processes')
ax.set_ylabel('Speedup (vs Serial)')
ax.set_xticks(mpi_procs)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph6_mpi_amdahl.png')
plt.close()
print("Saved graph6_mpi_amdahl.png")

# ============================================================
# GRAPH 7: Hybrid — Empirical vs Theoretical speedup, N=20M
# ============================================================
all_hybrid_units = []
all_hybrid_emp   = []
all_hybrid_theo  = []
for u in [4, 8, 16, 32]:
    for t in hybrid_data[u]['times']:
        all_hybrid_units.append(u)
        all_hybrid_emp.append(serial_20m / t)
        all_hybrid_theo.append(amdahl(u, S, P))

unique_units = [4, 8, 16, 32]
best_emp     = [max([serial_20m/t for t in hybrid_data[u]['times']]) for u in unique_units]
theo         = [amdahl(u, S, P) for u in unique_units]

fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(all_hybrid_units, all_hybrid_emp, color='#9b59b6', alpha=0.6, zorder=3, label='Empirical (all configs)')
ax.plot(unique_units, best_emp,  'D-', color='#9b59b6', label='Empirical (best config)', linewidth=2)
ax.plot(unique_units, theo,      's--', color='#e74c3c', label="Theoretical (Amdahl's Law)", linewidth=2)
ax.set_title("Graph 7: Hybrid MPI+OpenMP — Empirical vs Theoretical Speedup\n(Increasing total units, N=20M)")
ax.set_xlabel('Total Parallel Units (Processes × Threads)')
ax.set_ylabel('Speedup (vs Serial)')
ax.set_xticks(unique_units)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph7_hybrid_amdahl.png')
plt.close()
print("Saved graph7_hybrid_amdahl.png")

print("\nAll 7 graphs generated successfully!")
