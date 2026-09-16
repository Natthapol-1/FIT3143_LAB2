# Presentation Q&A Cheat Sheet

This document contains the exact answers to all the "Questions to Consider" listed in your lab specification for Tasks 1, 2, 3, and 4. You can use these to build your presentation slides and answer the TA's questions during the live Q&A.

## Task 1: Open MPI
**Q: What is the speed-up? Is it reasonable?**
*   **Answer:** Yes, the speed-up is highly reasonable. For checking 20,000,000 numbers, the serial code took ~7.08s, while Open MPI with 16 processes took ~0.98s (a 7.2x speedup). This represents an excellent parallel efficiency considering the communication overhead required by MPI.

**Q: How does speed-up change with the number of processes and n? Why?**
*   **Answer:** As `n` increases, the speedup gets *better* because the ratio of computation (prime checking) to communication overhead (gathering the results) increases. As the number of processes increases, speedup increases up to a point, but eventually plateaus (or drops) due to Amdahl's Law (the serial bottleneck of combining the arrays) and the physical limits of the CPU cores available on the node.

**Q: How to ensure balanced workload distribution?**
*   **Answer:** We used a **Cyclic Workload Distribution** (`i += size`). Checking large numbers (like 9,999,991) takes much longer than small numbers (like 7). If we split the workload statically (e.g., Process 0 gets 0-5M, Process 1 gets 5M-10M), Process 1 would take significantly longer. By using a cyclic approach, every process gets an equal mix of fast small numbers and slow large numbers, perfectly balancing the load.

---

## Task 2: Hybrid Open MPI + OpenMP
**Q: What is the speed-up? Is it reasonable?**
*   **Answer:** The hybrid approach provided the best speedup overall. Using 8 MPI processes with 4 OpenMP threads each (32 total units), the time dropped to 0.63s (an 11.2x speedup over serial). It is highly reasonable and shows the power of combining distributed memory with shared memory.

**Q: How does speed-up change with the number of threads, processes, and n? Why?**
*   **Answer:** Increasing total computing units (threads $\times$ processes) decreases runtime, but we noticed that configurations heavily favoring OpenMP threads (e.g., 1 process $\times$ 4 threads = 1.91s) were faster than configurations favoring MPI processes (e.g., 4 processes $\times$ 1 thread = 3.66s). This is because OpenMP threads share memory and don't require the heavy network communication overhead that MPI processes do.

**Q: How to ensure balanced workload distribution?**
*   **Answer:** In addition to the MPI cyclic distribution, we used **`schedule(guided)`** for the OpenMP threads. Guided scheduling hands out large chunks of iterations at the beginning (when numbers are small and fast to check) and progressively smaller chunks towards the end (when numbers are huge and slow to check). This ensures no thread is left sitting idle at the end of the computation.

---

## Task 3: Performance Evaluation
**Q: Empirical vs Theoretical speed-up?**
*   **Answer:** Our theoretical speedup (calculated via Amdahl's Law) was consistently higher than our empirical speedup. For example, at 32 processes, theoretical speedup was 25.5x, but empirical was 8.79x. 
*   **Why?** Amdahl's Law only accounts for the serial vs parallel fractions. It completely ignores hardware realities like cache misses, memory bus contention, network latency during `MPI_Gather`, and the overhead of spawning threads.

**Q: Does increasing MPI processes always increase speed-up?**
*   **Answer:** No. We observed diminishing returns. Moving from 1 to 16 processes dropped the time drastically, but increasing further to 24 or 32 processes yielded very little improvement. At a certain point, the cost of coordinating 32 processes outweighs the benefit of the extra processing power.

**Q: Same speed-up across different machines?**
*   **Answer:** No. Different machines have different physical core counts, clock speeds, and memory bandwidths. Furthermore, cluster machines have different network topologies. Running this on a 4-core laptop would hit a severe bottleneck much earlier than running it on a 32-core university cluster node.

---

## Task 4: Alternative Assessment / Conclusion (If asked)
**Q: Would you recommend Open MPI for prime number searching (against POSIX Thread/Open MP)? Why/Why not?**
*   **Answer:** I would actually recommend OpenMP (or the Hybrid approach) over pure Open MPI for this specific problem. 
*   **Pros of MPI:** It can scale infinitely across multiple physical computers, whereas OpenMP is restricted to a single machine.
*   **Cons of MPI:** Prime number searching requires checking millions of numbers. Returning all those found primes to the root process via `MPI_Gather` creates a massive communication bottleneck. OpenMP avoids this entirely because all threads write directly to shared memory, which is significantly faster.
