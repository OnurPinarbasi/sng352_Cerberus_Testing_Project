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

## 2. Step-by-Step Setup and Execution Guide

Follow these steps to set up the environment and run the tests from scratch:

### Step 2.1: Prerequisites
Ensure you have the following installed on your machine:
*   **Python**: Version 3.8 or higher.
*   **Git**: To clone the repository.

### Step 2.2: Clone the Repository
Clone the project repository and navigate into the root directory:
```bash
git clone git@github.com:OnurPinarbasi/sng352_Cerberus_Testing_Project.git
cd sng352_Cerberus_Testing_Project
```
*(Alternatively, you can clone via HTTPS: `git clone https://github.com/OnurPinarbasi/sng352_Cerberus_Testing_Project.git`)*

### Step 2.3: Create and Activate a Virtual Environment (Recommended)
Set up a clean virtual environment to avoid package dependency conflicts:
*   **On macOS and Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
*   **On Windows (CMD or PowerShell):**
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```

### Step 2.4: Install Dependencies
Install the required testing framework, `pytest`. No other packages are needed as the `cerberus` module being tested is bundled locally inside the project:
```bash
pip install pytest
```

### Step 2.5: Run Clean Unit Tests
Verify that all 105 clean unit tests written by our team members pass on the original codebase:
```bash
pytest tests/ -v
```

### Step 2.6: Run the Mutation Testing Suite
Execute the automated mutation testing runner to apply the 45 logical mutants sequentially and test whether our suite catches (kills) them:
```bash
python faults/run_mutants.py
```
*Note: This script automatically backs up `cerberus/validator.py`, applies each mutant in isolation, runs the targeted killing test, restores the clean code, and generates a summary table of **KILLED** and **SURVIVED** mutants.*

### Step 2.7: Run a Specific Mutant Individually
To execute and test a single mutant (e.g., `F1-1`) in isolation:
```bash
python faults/run_mutants.py F1-1
```

---

## 3. Folder Structure

* **`cerberus/`**: The source code of the target library being tested.
* **`tests/`**: Unit tests written by group members. (`Ahmet Kerem Ince (member1)`, `Berrak Yildirim (member2)`, `Onur Pinarbasi (member3)`, `Zeynep Orman (member4)`).
* **`faults/`**: Manually created logical error files (mutants) and an autorunner script. (`run_mutants.py`).
* **`report/`**: Project delivery report including mathematical derivations, truth tables and analyses. (`report.md`).