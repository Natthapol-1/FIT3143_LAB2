import re

def parse_results():
    with open('experiment_results.txt', 'r') as f:
        lines = f.readlines()

    exp_a = []
    exp_b = []
    exp_c = []
    
    current_exp = None
    current_n = None
    current_serial = None
    current_p = None
    current_t = None
    
    for i, line in enumerate(lines):
        if "=== EXPERIMENT A:" in line:
            current_exp = 'A'
        elif "=== EXPERIMENT B:" in line:
            current_exp = 'B'
        elif "=== EXPERIMENT C:" in line:
            current_exp = 'C'
            
        if current_exp == 'A':
            m = re.search(r'Testing N = (\d+)', line)
            if m:
                current_n = int(m.group(1))
            m = re.search(r'\[SERIAL\] Time taken: ([\d\.]+) seconds', line)
            if m:
                current_serial = float(m.group(1))
            m = re.search(r'\[TASK1_MPI\] Total Time: ([\d\.]+) s', line)
            if m:
                exp_a.append({'N': current_n, 'Serial_Time': current_serial, 'MPI_Time': float(m.group(1))})
                
        elif current_exp == 'B':
            m = re.search(r'\[SERIAL\] Time taken: ([\d\.]+) seconds', line)
            if m:
                current_serial = float(m.group(1))
            m = re.search(r'\[MPI \((\d+) processes\)\]', line)
            if m:
                current_p = int(m.group(1))
            m = re.search(r'\[TASK1_MPI\] Total Time: ([\d\.]+) s \| Parallel Loop Time: ([\d\.]+) s \| Serial Overhead: ([\d\.]+) s', line)
            if m:
                exp_b.append({
                    'Procs': current_p, 
                    'Total_Time': float(m.group(1)),
                    'Parallel_Time': float(m.group(2)),
                    'Serial_Overhead': float(m.group(3))
                })
                
        elif current_exp == 'C':
            m = re.search(r'\[Hybrid \((\d+) processes, (\d+) threads\)\]', line)
            if m:
                current_p = int(m.group(1))
                current_t = int(m.group(2))
            m = re.search(r'\[TASK2_HYBRID\] Total Time: ([\d\.]+) s \| Parallel Loop Time: ([\d\.]+) s \| Serial Overhead: ([\d\.]+) s', line)
            if m:
                exp_c.append({
                    'Procs': current_p,
                    'Threads': current_t,
                    'Total_Units': current_p * current_t,
                    'Total_Time': float(m.group(1)),
                    'Parallel_Time': float(m.group(2)),
                    'Serial_Overhead': float(m.group(3))
                })

    return exp_a, exp_b, exp_c, current_serial

def generate_report():
    exp_a, exp_b, exp_c, serial_baseline_20M = parse_results()
    
    with open('task3_data.md', 'w') as f:
        f.write("# Task 3 Data for Presentation Graphs\n\n")
        
        # Graph 1 & 2
        f.write("## Data for Graphs 1 & 2 (Increasing N with 4 MPI Processes)\n")
        f.write("| N | Serial Time (s) | Open MPI Time (s) | Empirical Speedup |\n")
        f.write("|---|---|---|---|\n")
        for row in exp_a:
            speedup = row['Serial_Time'] / row['MPI_Time']
            f.write(f"| {row['N']} | {row['Serial_Time']:.3f} | {row['MPI_Time']:.3f} | {speedup:.2f}x |\n")
        f.write("\n")
        
        # Graph 3 & 6
        f.write("## Data for Graphs 3 & 6 (Increasing MPI Processes, N = 20M)\n")
        f.write(f"**Baseline Serial Time:** {serial_baseline_20M:.3f} s\n\n")
        
        # Calculate Amdahl's fractions from 1 process
        p1 = next((r for r in exp_b if r['Procs'] == 1), None)
        frac_s = p1['Serial_Overhead'] / p1['Total_Time']
        frac_p = p1['Parallel_Time'] / p1['Total_Time']
        
        f.write(f"**Amdahl's Fractions (from 1 MPI process):**\n")
        f.write(f"- Serial Fraction (S): {frac_s:.4f}\n")
        f.write(f"- Parallel Fraction (P): {frac_p:.4f}\n\n")
        
        f.write("| Processes | MPI Time (s) | Empirical Speedup | Theoretical Speedup (Amdahl) |\n")
        f.write("|---|---|---|---|\n")
        for row in exp_b:
            emp_speedup = serial_baseline_20M / row['Total_Time']
            theo_speedup = 1.0 / (frac_s + (frac_p / row['Procs']))
            f.write(f"| {row['Procs']} | {row['Total_Time']:.3f} | {emp_speedup:.2f}x | {theo_speedup:.2f}x |\n")
        f.write("\n")
        
        # Graph 4, 5, 7
        f.write("## Data for Graphs 4, 5, & 7 (Hybrid MPI + OpenMP, N = 20M)\n")
        f.write("| MPI Processes | OpenMP Threads | Total Units | Hybrid Time (s) | Empirical Speedup | Theoretical Speedup (Amdahl) |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        exp_c_sorted = sorted(exp_c, key=lambda x: x['Total_Units'])
        for row in exp_c_sorted:
            emp_speedup = serial_baseline_20M / row['Total_Time']
            theo_speedup = 1.0 / (frac_s + (frac_p / row['Total_Units']))
            f.write(f"| {row['Procs']} | {row['Threads']} | {row['Total_Units']} | {row['Total_Time']:.3f} | {emp_speedup:.2f}x | {theo_speedup:.2f}x |\n")
            
if __name__ == '__main__':
    generate_report()
    print("task3_data.md has been generated.")
