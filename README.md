# Patient-Health-Record-Consent-Management-System
# Software Engineering Lab Submissions

This repository contains my Software Engineering lab submissions. Each lab has its own folder.

## Student Details

| SRN | Name |
|---|---|
| PES1UG24AM107 | Nakka Gopya |

## Labs at a Glance

| Lab | Topic | Folder | Main Deliverables |
|---|---|---|---|
| Lab 1 | Lab 1 submission | [`lab1/`](lab1) | `PES1UG24AM107.pdf` |
| Lab 2 | Lab 2 submission | [`lab2/`](lab2) | `PES1UG24AM107.pdf` |
| Lab 3 | UML Component Diagram (Layered Architecture) | [`Lab3/`](Lab3) | Component diagram, justification PDF, README |
| Lab 4 | Separate repository | [`LAB4`](LAB4) | Link: [fruit-ninja-lab4](https://github.com/gopya3106/fruit-ninja-lab4) |
| Lab 5 | Static Code Analysis (Pylint, Flake8, Bandit) | [`lab 5/`](lab%205) | Fixed code, before/after reports, `issues.md`, `reflection.md` |
| Lab 6 | Code and Branch Coverage (coverage + pytest) | [`lab 6/`](lab%206) | Code and branch coverage tests, screenshots |
| Lab 7 | Fuzz Testing (Hypothesis) | [`lab 7/`](lab%207) | Fixed script, Hypothesis tests, PDF report |

## Repository Structure

```text
Patient-Health-Record-Consent-Management-System/
│
├── README.md
│
├── lab1/
│   └── PES1UG24AM107.pdf
│
├── lab2/
│   └── PES1UG24AM107.pdf
│
├── Lab3/
│   ├── README.md
│   ├── Lab3_Component_Diagram.png
│   └── Lab3_Justification.pdf
│
├── LAB4                                   (link to the Lab 4 repository)
│
├── lab 5/
│   ├── library_catalog_system.py          (fixed code)
│   ├── issues.md
│   ├── reflection.md
│   └── reports/
│       ├── before/   (pylint, flake8, bandit reports)
│       └── after/    (pylint, flake8, bandit reports)
│
├── lab 6/
│   ├── laundry_service.py                 (code under test)
│   ├── CodeCoverageTest_laundry_service.py
│   ├── BranchCoverageTest_laundry_service.py
│   └── screenshots/
│
└── lab 7/
    ├── laundry_service.py                 (fixed application)
    ├── test_laundry_service.py            (Hypothesis fuzz tests)
    ├── Lab7_FuzzTesting_Report.pdf
    └── screenshots/
```

## Lab 5: Static Code Analysis

I ran Pylint, Flake8 and Bandit on `library_catalog_system.py` and fixed the issues they reported. The Pylint score went from **5.32 to 10.00**. The reports from before and after the fixes are in `reports/`. The issues are listed in `issues.md`, and my answers are in `reflection.md`.

## Lab 6: Code and Branch Coverage

The code under test is `laundry_service.py`, which works out extra-weight charges, whether an order can be accepted, and the drop-off cutoff status.

| Test file | Tests | Line coverage | Branch coverage |
|---|---|---|---|
| Starter test file | 2 | 38% | 32% |
| `CodeCoverageTest_laundry_service.py` | 12 | **100%** | 98% |
| `BranchCoverageTest_laundry_service.py` | 34 | **100%** | **100%** |

The code coverage tests run every line but still miss one branch: a heavy load on standard speed. The branch coverage tests add that case, plus boundary values and every combination of conditions.

To run (from inside `lab 6`):

```bash
pip install coverage pytest
coverage run --branch -m pytest BranchCoverageTest_laundry_service.py
coverage report -m
```

## Lab 7: Fuzz Testing

I used Hypothesis to fuzz the three functions in `laundry_service.py`: `parse_order`, `weight_average` and `payable_charge`. It found crashes on inputs like `None`, `""`, `":"`, `"|"` and `"1,,3"`. It also found a wrong result: `weight_average` used integer division, so it gave 5 instead of 5.33 for `3,5,8`.

In the fixed script, every function checks its input. Invalid input returns `None` (and the program prints "Invalid input") instead of crashing. Also, numbers must be finite and non-negative, and the average uses true division.

Result: **4 of 6** tests fail on the original code, and **6 of 6** pass on the fixed code.

To run (from inside `lab 7`):

```bash
pip install hypothesis pytest
python laundry_service.py
python -m pytest test_laundry_service.py -v
```

## File Naming Convention

For PDF-only labs, the submission is named with my SRN: `PES1UG24AM107.pdf`. For code labs, the file names follow the lab handout.
