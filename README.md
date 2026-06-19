# Sales Intelligence Platform — Complete Project Documentation

This document explains, from absolute zero, everything that was done to go from
"no Python installed" to a working, professional AI-powered web application.
It follows the official AI Engineer syllabus and explains every concept and every
line of code in plain language.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Environment Setup (Installation Guide)](#2-environment-setup-installation-guide)
3. [Project Folder Structure](#3-project-folder-structure)
4. [Phase 1 — Learning in the Notebook](#4-phase-1--learning-in-the-notebook)
5. [Phase 2 — Building the Web Application](#5-phase-2--building-the-web-application)
6. [Full Code Walkthrough — `dashboard_v3.py`](#6-full-code-walkthrough--dashboard_v3py)
7. [Syllabus Coverage Map](#7-syllabus-coverage-map)
8. [How to Run This Project](#8-how-to-run-this-project)
9. [Key Concepts Glossary](#9-key-concepts-glossary)

---

## 1. Project Overview

**What was built:** A web application called the **Sales Intelligence Platform**.
It lets a user upload *any* CSV file (sales data, employee data, or anything with
numeric and category columns), and the app automatically:

- Cleans the data (removes duplicates, fills missing values)
- Lets the user filter the data interactively
- Draws charts (bar charts, line charts, correlation heatmaps, histograms)
- Trains a real Machine Learning model live, in the browser
- Predicts an outcome (e.g. predicted sales amount) based on user-entered numbers
- Explains *why* the model made that prediction
- Lets the user download the cleaned data and the predictions as CSV files

**Tech used:** Python, Pandas, NumPy, Matplotlib, Seaborn, scikit-learn, Streamlit.

**Why this project:** It touches almost every module in the AI Engineer syllabus —
Python basics, NumPy, Pandas, visualization, data cleaning, statistics, and
supervised machine learning — inside one connected, realistic project instead of
disconnected exercises.

---

## 2. Environment Setup (Installation Guide)

This section documents every installation step taken, in order, for a Windows
machine that had nothing installed beforehand.

### 2.1 Installing Python

Python is the programming language everything else is built on.

1. Downloaded the standalone installer from python.org
   (`python-3.14.6-amd64.exe`).
2. Ran the installer and **checked both boxes**:
   - "Use admin privileges when installing py.exe" — installs Python for all users
     on the machine.
   - "Add python.exe to PATH" — this is the critical one. It lets Windows find the
     `python` command from *any* folder in the terminal. Without this, the terminal
     would say `'python' is not recognized`.
3. Clicked **Install Now** and allowed the Windows permission popup.
4. Verified the install by opening Command Prompt and running:
   ```
   python --version
   ```
   This printed `Python 3.14.6`, confirming success.

### 2.2 Installing VS Code

VS Code is the code editor used to write and run all the code.

1. Downloaded and installed VS Code from code.visualstudio.com.
2. Inside VS Code, installed two extensions (via the Extensions panel,
   `Ctrl+Shift+X`):
   - **Python** (by Microsoft) — lets VS Code understand and run Python files.
   - **Jupyter** (by Microsoft) — lets VS Code run interactive notebooks
     (`.ipynb` files), where code can be run in small chunks ("cells") with
     output shown immediately below each cell. This is much easier for learning
     than running a whole script at once.

### 2.3 Creating the Project and a Virtual Environment

1. Created a folder `D:\AI-Engineer-Project` and opened it in VS Code
   (File → Open Folder).
2. Opened a terminal inside VS Code (Terminal → New Terminal). This terminal
   turned out to be **PowerShell** (prompt prefix `PS`).
3. Created a **virtual environment**:
   ```
   python -m venv venv
   ```
   **What this does and why it matters:** A virtual environment is an isolated,
   self-contained copy of Python just for this project. Any libraries installed
   inside it do not affect the rest of the computer, and other projects' libraries
   don't interfere with this one. This is standard practice in real software
   development.
4. Activated the virtual environment:
   ```
   venv\Scripts\Activate.ps1
   ```
   (PowerShell required this exact script name; Command Prompt would have used
   `venv\Scripts\activate` instead.) Once active, the terminal prompt changed to
   show `(venv)` at the start — confirming the isolated environment was in use.

   *Troubleshooting hit during setup:* PowerShell initially blocked the activation
   script for security reasons. This was fixed once, permanently, with:
   ```
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

### 2.4 Installing the Core Libraries

With `(venv)` active, all required libraries were installed in one command:

```
pip install numpy pandas matplotlib seaborn scikit-learn jupyter notebook openpyxl
```

| Library | What it's for |
|---|---|
| `numpy` | Fast numerical operations on arrays of numbers |
| `pandas` | Loading, exploring, cleaning, and analyzing tabular data (like Excel, but in code) |
| `matplotlib` | Drawing charts and graphs |
| `seaborn` | Prettier, higher-level charts built on top of matplotlib (used for the heatmap) |
| `scikit-learn` | Machine learning — training and evaluating models |
| `jupyter` / `notebook` | Running interactive notebooks |
| `openpyxl` | Reading/writing Excel files |

Later, one more library was added for the web app itself:
```
pip install streamlit
```
**Streamlit** turns a plain Python script into an interactive web application,
without needing to know HTML, CSS, or JavaScript separately — although custom
HTML/CSS was later added for visual polish.

---

## 3. Project Folder Structure

```
AI-Engineer-Project/
│
├── venv/                        # The isolated Python environment (created by venv)
├── data/
│   └── sales_data.csv           # The dataset used for learning and as the app's default data
├── notebooks/
│   └── 01_python_basics.ipynb   # Where all the learning/experimentation happened
└── app/
    └── dashboard_v3.py          # The final, polished web application
```

Keeping data, notebooks, and application code in separate folders is standard
practice — it keeps the project organized as it grows, and mirrors how real
data/AI projects are structured.

---

## 4. Project work

The project has two main parts:

- Notebook analysis (`notebooks/01_python_basics.ipynb`) for data exploration, cleaning, visualization, and model evaluation.
- Streamlit app development (`app/dashboard.py`) to make the workflow interactive: upload CSV, clean data, show charts, train a model, make predictions, and download results.

The app is built with Python, Pandas, Matplotlib, Seaborn, scikit-learn, and Streamlit.

---

## 5. How to Run This Project

1. Open the project folder in VS Code: `D:\AI-Engineer-Project`.
2. Activate the virtual environment:
   ```powershell
   venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the app:
   ```powershell
   streamlit run app/dashboard.py
   ```
5. Open the browser at `http://localhost:8501`.

---

## 6. Notes

- `requirements.txt` contains the deployment dependencies.
- `.gitignore` excludes `venv/`, caches, and temporary files.
- Streamlit Cloud should use the repo `Jayakumar044/AI-Engineer-Project` with the main file path `app/dashboard.py`.

