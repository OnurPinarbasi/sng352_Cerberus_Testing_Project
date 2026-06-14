# Cerberus Software Testing Project

This project is a software testing project developed to test the security and accuracy of the Python data validation library **Cerberus**. 

In the project, the **MUMCUT** analysis method and **DNF Error Classes** were used from formal test design methods.

| Fault Class | Description |
|------------|-------------|
| **ENF** (Expression Negation Fault) | Entire expression is mistakenly negated. |
| **TNF** (Term Negation Fault) | A whole term is mistakenly negated. |
| **TOF** (Term Omission Fault) | A term is accidentally removed. |
| **LNF** (Literal Negation Fault) | A literal is mistakenly negated. |
| **LRF** (Literal Reference Fault) | A literal is replaced by another literal. |
| **LOF** (Literal Omission Fault) | A literal is accidentally removed from a term. |
| **LIF** (Literal Insertion Fault) | An extra literal is added to a term. |
| **ORF+** (Operator Reference Fault) | An OR operator is incorrectly changed to AND. |
| **ORF*** (Operator Reference Fault) | An AND operator is incorrectly changed to OR. |

---

## 1. General Information About the Project

* **Target System:** 20 critical functions in the `validator.py` file of the Cerberus validation library were tested.
* **Teamwork:** 4 team members selected 5 completely unique functions from the system (20 functions in total) and created detailed $\LaTeX$ analyses and accuracy tables.
* **Test Suite:** Each member wrote at least 20 unit tests, creating a robust test suite with **105 tests in total**.
* **Error Emulation (Mutation Testing):** Add the Table 8.1 error classes (LIF, LNF, TOF, etc.) to the code base.) simulating **45 logical mutations** (artificial error) have been placed. In this way, the ability of the tests to catch (kill) errors was measured.

---

## 2. Execution Commands

While in the project's root directory in the terminal, you can use the following commands:

### 2.1. To Run Unit Tests
To run all written clean tests and verify that they pass:
```bash
pytest tests/ -v
```

### 2.2. For Running Mutation (Mutation) Tests
To automatically test whether the written logical errors (mutants) are caught (or killed) by the tests:
```bash
python faults/run_mutants.py
```
*(This command will apply the 45 mutations sequentially to the code, run the tests, and finally display in a table format in the terminal which ones were successfully detected).*

---

## 3. Folder Structure

* **`cerberus/`**: The source code of the target library being tested.
* **`tests/`**: Unit tests written by group members. (`Ahmet Kerem Ince (member1)`, `Berrak Yildirim (member2)`, `Onur Pinarbasi (member3)`, `Zeynep Orman (member4)`).
* **`faults/`**: Manually created logical error files (mutants) and an autorunner script. (`run_mutants.py`).
* **`report/`**: Project delivery report including mathematical derivations, truth tables and analyses. (`report.md`).