# Centralized Fault & Mutation Testing

This directory contains the manually implemented DNF fault-emulating mutations used to evaluate the effectiveness of the test suite developed for the **Cerberus** data validation library.

---

## 1. Purpose of the Directory

The purpose of this folder is to organize all mutation testing artifacts in one centralized place. It contains:
- **45 individual mutants** (organized into subfolders named `F1-1` through `F4-11`), each simulating a specific logic fault class on a chosen target method of the system under test (`cerberus/validator.py`).
- **INDEX.md**: A tabular index of all mutants, mapping each mutant to its fault class, target function, and killing test.
- **VALIDATION.md**: Log file verifying that the test suite compiles and runs successfully on a clean codebase.
- **mutations.md**: Detailed textual descriptions of the mutation rationales, original vs. mutated code snippets, and analysis for each mutant.
- **run_mutants.py**: A unified command-line entry point to execute and verify the killing status of all or individual mutants.

---

## 2. Available Fault Classes and Mutants

The project implements **45 mutants** covering all **10 DNF fault classes** from Table 8.1 of the Software Testing course methodology:

| Fault Class | Description | Implemented Mutants |
|-------------|-------------|---------------------|
| **LIF** | Literal Insertion Fault | F1-1, F1-2, F1-4, F2-2, F2-4, F3-1, F3-3, F4-4 |
| **LRF** | Literal Replacement Fault | F2-5, F1-7, F3-7, F2-7 (in items/regex checks) |
| **LOF / TOF** | Term Omission Fault / Literal Omission | F1-3, F2-3, F3-4, F4-1 |
| **LNF** | Literal Negation Fault | F1-5, F2-1, F3-2, F4-2, F4-3 |
| **ENF** | Expression Negation Fault | F3-5, F1-12, F2-11, F4-11 |
| **LDF** | Literal Deletion Fault | F1-6, F2-6, F3-6, F4-6 |
| **TNF** | Term Negation Fault | F1-8, F2-7, F3-8, F4-7 |
| **TIF** | Term Insertion Fault | F1-9, F2-8, F3-9, F4-8 |
| **ORF+** | Operator Replacement Fault (logical OR/AND) | F1-10, F2-9, F3-10, F4-9 |
| **ORF\*** | Operator Replacement Fault (relational operator) | F1-11, F2-10, F3-11, F4-10 |

---

## 3. How to Execute Mutants

You can run mutants easily using the unified runner script `run_mutants.py` located inside this directory.

### Prerequisite
Make sure you are in the project root directory and your Python environment has `pytest` installed.

### Execute All Mutants at Once
To run all 45 mutants sequentially, apply their changes, run the killing tests, and print a summary table of the mutation score:
```bash
python faults/run_mutants.py
```

### Execute a Single Mutant
To run a specific mutant (e.g., `F1-1`), apply only its mutation, execute its specific killing test, and restore the code:
```bash
python faults/run_mutants.py F1-1
```

---

## 4. Expected Project Structure

```text
proje/
  cerberus/
    validator.py         # System Under Test (SUT)
  tests/
    member1/             # Tests targeting Member 1 functions (27 tests)
    member2/             # Tests targeting Member 2 functions (23 tests)
    member3/             # Tests targeting Member 3 functions (27 tests)
    member4/             # Tests targeting Member 4 functions (28 tests)
  faults/
    INDEX.md             # Mutants inventory mapping mutants to tests
    VALIDATION.md        # Clean run validation output
    mutations.md         # Full descriptions of each mutation
    README.md            # This documentation file
    run_mutants.py       # Unified automated mutation runner script
    F1-1/                # Individual mutant folder
      original.py        # Code block before mutation
      mutated.py         # Code block after mutation
      mutation.patch     # Unified diff patch file
      README.md          # Mutant details and manual instructions
    ...                  # (Folders for F1-2 through F4-11)
```
