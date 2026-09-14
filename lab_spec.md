# FIT3143 Lab Assessment: Message Passing Interface (MPI)

## Objectives
- Introduce Open MPI
- Design and analyse distributed parallel algorithms with the Message Passing Interface (MPI)

## Marks
- The lab session is worth 8 marks of the unit's final mark.

## Lab Instructions
1. **Preparation**: Preparation is required for this Lab session. Please DO NOT plan to complete the Lab without any preparation/understanding.
2. **Timeline**: Students should start working on the Lab tasks at least 1 week prior to the assessed session.
3. **Submission**: Students must submit their answers and codes via Moodle in the required format before the start of the allocated class. A late penalty (5% per day) will apply if you do not submit the required materials on time!
4. **Assessment Format**: In addition to regular offline/off-class marking, students’ (or Team’s) slides, answers, and/or source code will also be reviewed and assessed through in-class presentations, peer reviews, and/or question-and-answer sessions.
5. **Presentation Marking**: For team/group presentations, marks in general will be allocated for:
    - The correctness of the codes or results
    - The quality and clarity of the presentation
    - The correctness of the explanation during the presentation
    - *Note: The presentation content should include slides that are clear, easy to understand, and readable in a professional working environment. Hard to read/digest presentations will lose marks.*
6. **Q&A Marking**: For individual/group interviews and Q&A sessions, marks will be allocated for:
    - The correctness of the verbal answer
    - The quality of the verbal answer
    - *Note: Focus on the most important idea. Concise, focused and accurate explanations with reference to submitted code/documents will be awarded. Inaccurate/lengthy explanations, lack of understanding, or unfiltered AI-generated answers will lose marks.*
7. **Rubric**: Always make sure you read and follow the marking rubric well in advance of the deadline.
8. **Participation**: Marks will not be awarded if you skip the class, do not make any submissions, do not contribute to the team, or make an empty submission.
9. **Generative-AI**: You are allowed to use Generative-AI to search for information during preparation. However, you must declare it in your report and upload all prompt records (in PDF files).
10. **No AI during assessment**: AI tools are not allowed during the presentation period or any oral/coding interview sessions.
11. **Identification**: All submitted files should ideally include students’ names, ID and Monash email addresses.

## Lab In-Class Assessment Activities
Students are required to form teams of 2. *(Exceptions must be arranged by Week 7)*.

- **Team Preparation Period (before deadline)**: Divide workload, complete tasks, submit required files before the deadline.
- **Team Presentation Period (max 7 min)**: Present and demonstrate code, results, and observations. All members must be present.
- **Q&A Period (approx. 2 min)**: Each member will be asked roughly two questions based on the submitted/presented work.

*Note: Missing submissions or absent members result in 0 marks.*

---

## Task 0 - Getting used to Open MPI manual pages
Make sure you are familiar with the [Open MPI manual pages](https://docs.open-mpi.org/en/v5.0.x/man-openmpi/index.html). Refer to CAAS documentation or set up a local cluster prior to completing the following tasks for performance analysis.

## Task 1 – Prime Search using Message Passing Interface (Open MPI)
Revisiting the prime search problem from Week 4. Implement a parallel version of your serial C code using MPI with Open MPI.

**Coding requirements:**
- **Input**: Root process reads integer `n` as a command-line argument.
- **Dissemination**: The value `n` is disseminated to all other MPI processes.
- **Workload Distribution**: Each process (including root) computes a share of the prime numbers. Design an efficient and balanced workload distribution algorithm. Explore different options.
- **Output**: After computation, the root process prints the final result to a text file in **sorted order**.

*Notes:*
- Run on a single computer and across multiple computers.
- Code must be clean and bug-free to compare against serial, POSIX Thread, and OpenMP versions.
- Test with different numbers of MPI processes and workload distributions.

**Questions to consider:**
- What is the speed-up? Is it reasonable?
- How does speed-up change with number of processes and `n`? Why?
- How to ensure balanced workload distribution?

## Task 2 – Prime Search using hybrid OpenMP and Message Passing Interface (Open MPI)
Implement a hybrid version combining shared memory parallelism (OpenMP) and distributed memory parallelism (OpenMPI).

**Coding requirements:**
- **Input**: Root process reads integer `n` as a command-line argument.
- **Dissemination**: Value `n` is disseminated to all MPI processes and accessible by all threads within a process.
- **Workload Distribution**: Each MPI process creates a set of threads. Design an efficient and balanced workload distribution using a different number of threads and processes.
- **Output**: The main thread of the root process prints the sorted results to a text file.

*Notes:*
- Test with different numbers of threads, MPI processes, and workload distributions.
- Run on a single computer and across multiple computers.
- Code must be clean and bug-free to compare against other versions.

**Questions to consider:**
- What is the speed-up? Is it reasonable?
- How does speed-up change with number of threads, processes, and `n`? Why?
- How to ensure balanced workload distribution?

## Task 3 – Performance evaluation with Amdahl’s Law
Perform empirical evaluations and theoretical analysis (Amdahl’s Law) for Task 1 and 2.

**Empirical Evaluations:**
Measure wall-clock time and derive empirical speed-up against the serial code (Week 4 Task 1) with:
- Increasing problem size `n`
- Increasing number of MPI processes
- Increasing number of threads (Task 2)

**Theoretical Analysis:**
Measure the wall-clock time of serial part(s) and parallel part(s). Utilize Amdahl’s Law or Gustafson’s Law to compute theoretical speed-up with:
- Increasing problem size `n`
- Increasing number of MPI processes
- Increasing number of threads (Task 2)

*Notes:*
- Consider the number of available cores.
- Design measurement experiments to compute serial/parallel fractions correctly (Amdahl vs Gustafson).

**Questions to consider:**
- Empirical vs Theoretical speed-up?
- Does increasing MPI processes always increase speed-up?
- Impact of workload distribution?
- Same speed-up across different machines?

## Task 4 – Presentation slides and documentations
Prepare presentation slides/documentation. 7 min presentation + 2 min Q&A.

**a) (Task 1) Open MPI code [~3 min]**
- Discuss parallel partitioning scheme.
- Graph 1: Runtime of Open MPI vs POSIX/OpenMP (increasing `n`).
- Graph 2: Empirical speed up of Open MPI vs POSIX/OpenMP (increasing `n`).
- Graph 3: Empirical speed up of Open MPI vs POSIX/OpenMP (increasing Open MPI processes).

**b) (Task 2) Open MPI + Open MP code [~2 min]**
- Discuss parallel partitioning scheme.
- Graph 4: Empirical speed up of Hybrid vs Open MPI (increasing threads).
- Graph 5: Empirical speed up of Hybrid vs POSIX/OpenMP (matching total thread count, increasing processes/threads).

**c) (Task 3) Performance evaluation [~2 min]**
- Discuss experimental design for measuring serial/parallel parts.
- Show derivation of Amdahl/Gustafson parameters.
- Graph 6: Empirical vs Theoretical speed-up of Open MPI (increasing processes).
- Graph 7: Empirical vs Theoretical speed-up of Hybrid (increasing processes and threads).

*Notes:*
- Test at least 30 different `n` values. Avoid tiny runtimes (<1s).
- Test threads/processes from 1 up to available CPU cores, and also explore testing beyond the core count.

**d) Q&A [~1 to 2 min]**
- TA/markers will ask questions related to presentation and submitted files.

## Submission Checklist
- `task1.c` and `task2.c`
- Presentation slides (or documentation) - max 7-min presentation content.
- Task 3 (Optional) – Additional notes/documents for calculations.
- AI declaration files (PDF), if applicable.

---

## Alternative Assessment Instructions (Special Consideration Only)
If approved for a special consideration extension:
1. Replaces in-class presentation with a pre-recorded video presentation (< 9 minutes).
2. Markers will only grade the first 9 minutes at regular speed.
3. Instead of live Q&A, answer the following in the recording:
    - *Would you recommend Open MPI for prime number searching (against POSIX Thread/Open MP)? Why/Why not? What are the pros and cons?*
    - *Is there a difference between the empirical speed-up and the theoretical speed-up? Why/Why not? Explain.*
4. Submit video (.mp4), slides, code, and AI declarations before the extended due date.
5. AI tools not allowed during recording. Show face and student ID at the start.
