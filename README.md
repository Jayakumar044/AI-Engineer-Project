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

## 4. Phase 1 — Learning in the Notebook

All of the following was done interactively inside `01_python_basics.ipynb`,
one cell at a time, using `Shift+Enter` to run each cell and see its output
immediately. This "learn by doing on real data" approach covers Modules 2–11 of
the syllabus.

### 4.1 Loading the data (Module 2 + 4)

```python
import pandas as pd
df = pd.read_csv('../data/sales_data.csv')
df.head()
```

- `import pandas as pd` loads the Pandas library under the short alias `pd`.
- `pd.read_csv(...)` reads the CSV file into a **DataFrame** — Pandas' table
  structure (rows and columns, like a spreadsheet).
- `'../data/sales_data.csv'` is a **relative path**: `../` means "go up one
  folder from where this notebook lives, then look inside `data/`."
- `df.head()` previews the first 5 rows.

### 4.2 Inspecting the data (Module 4 + 7)

```python
df.shape          # (rows, columns)
df.columns        # list of column names
df.dtypes         # data type of each column
df.info()         # combined summary: types + non-null counts
df.describe()     # statistics: mean, std, min, max, percentiles for numeric columns
```

`df.info()` revealed that out of 505 rows, `CustomerAge` and `PaymentMethod` each
had 18 missing values (487 non-null instead of 505) — this is what later drove the
data-cleaning step. `df.describe()` is where Module 7 (Statistics) came in
directly: mean, median (the 50% row), and standard deviation were read straight
off real data instead of from a textbook example.

### 4.3 Filtering, sorting, and grouping (Module 4)

```python
df.groupby('Region')['TotalSales'].sum().sort_values(ascending=False)
df.groupby('Category')['TotalSales'].sum().sort_values(ascending=False)
electronics_df = df[df['Category'] == 'Electronics']
```

- `groupby('Region')` splits the data into groups, one per region.
- `['TotalSales'].sum()` adds up sales within each group.
- `.sort_values(ascending=False)` orders the result from highest to lowest.
- `df[df['Category'] == 'Electronics']` is **boolean filtering**: the condition
  produces `True`/`False` for every row, and only the `True` rows are kept.

This is how a real, useful insight was found: Toys had the highest **quantity**
sold, but Electronics had by far the highest **revenue** — because Electronics'
per-unit price is much higher. Quantity and revenue rankings can disagree, and a
business decision should usually follow revenue, not unit count.

### 4.4 Visualization (Module 5)

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.bar(category_sales.index, category_sales.values, color='steelblue')
plt.title('Total Sales by Category')
plt.show()
```

Five chart types were built this way: **bar** (category comparison), **line**
(sales trend over time, using `pd.to_datetime()` to convert the date column from
text into a real date type first), **pie** (region share of total sales),
**histogram** (distribution of customer ages), and **scatter** (relationship
between unit price and total sales).

### 4.5 Data Cleaning (Module 6)

```python
df = df.drop_duplicates()

df['CustomerAge'] = df['CustomerAge'].fillna(df['CustomerAge'].median())
df['PaymentMethod'] = df['PaymentMethod'].fillna(df['PaymentMethod'].mode()[0])
```

- `drop_duplicates()` removes rows that are exact copies of an earlier row.
- For the missing `CustomerAge` (a number), each missing value was filled with
  the column's **median** — the middle value when sorted, which is robust to
  outliers.
- For the missing `PaymentMethod` (text/category), each missing value was filled
  with the **mode** — the single most frequently occurring value, since
  mean/median don't apply to text.

### 4.6 Correlation (Module 7)

```python
df[['Quantity', 'UnitPrice', 'DiscountPct', 'TotalSales', 'CustomerAge']].corr()
```

`.corr()` measures, for every pair of numeric columns, how strongly they move
together, on a scale from **−1** (perfect inverse relationship) to **+1**
(perfect direct relationship), with **0** meaning no relationship. The standout
finding: `UnitPrice` and `TotalSales` had a strong correlation of **0.81**, while
`CustomerAge` had almost **0** correlation with `TotalSales` — meaning a
customer's age told us almost nothing about how much they'd spend, but the
product's price told us a lot. This directly informed which columns to feed into
the machine learning model later (**feature selection**).

### 4.7 Machine Learning — Linear Regression (Module 8 + 9)

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

X = df[['Quantity', 'UnitPrice', 'DiscountPct']]   # features (inputs)
y = df['TotalSales']                                # target (what we predict)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
```

- **X** (features) is the input data the model is allowed to look at.
  **y** (target) is the value the model has to learn to predict.
- `train_test_split` divides the 500 rows into 400 for **training** (the model
  learns patterns from these) and 100 for **testing** (the model never sees these
  during training — they're used afterward to check if it actually learned
  something real, rather than memorizing).
- `model.fit(X_train, y_train)` is the actual learning step: the model studies the
  relationship between the input columns and the target column.
- `model.predict(X_test)` asks the trained model to guess `TotalSales` for rows it
  has never seen, so its accuracy can be measured honestly.

**Result:** MAE (Mean Absolute Error) = 817.28, R² Score = 0.827 — meaning the
model's predictions were, on average, about ₹817 off, and the model explained
about 83% of the variation in sales. Decent, but not great — partly because
Linear Regression can only learn straight-line relationships, while
`TotalSales = Quantity × UnitPrice × discount factor` is a multiplicative,
curved relationship.

### 4.8 Machine Learning — Random Forest (Module 9, improved model)

```python
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
```

A **Random Forest** builds many (100, here) individual decision trees, each
trained on a random slice of the data, and averages their predictions. This lets
it capture non-straight-line, multiplicative patterns far better than Linear
Regression.

**Result:** MAE = 150.41, R² = 0.987 — a dramatic improvement (about 5× lower
error, and explaining nearly 99% of the variation). This was the key lesson of
Module 9 and 11 combined: **always try more than one algorithm and compare**
using consistent metrics before deciding which one to use.

### 4.9 Feature Importance (Module 9 + 11, model interpretation)

```python
importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)
```

Random Forest can report how much "weight" it gave each input column when making
predictions. Result: `UnitPrice` = 72%, `Quantity` = 27%, `DiscountPct` =
under 1%. This matched the earlier correlation analysis almost exactly — two
independent methods agreeing is a strong signal that the conclusion (price drives
revenue far more than discount does) is trustworthy, not a fluke.

---

## 5. Phase 2 — Building the Web Application

Once the concepts were proven out in the notebook, the same logic was rebuilt
inside a **Streamlit** app so it could be used interactively in a browser instead
of by running notebook cells manually. Three versions were built, each adding
capability:

- **v1 (`dashboard.py`):** First working version — upload, clean, chart,
  train, predict. Hardcoded to the specific sales dataset's column names.
- **v2 (`dashboard_v2.py`):** Made the column logic *generic* — automatically
  detects numeric vs. category vs. date columns from *any* uploaded CSV, added a
  sidebar, interactive filters, and CSV download buttons. Fixed a bug where
  choosing a poor prediction target (e.g. `CustomerAge`, which has no real
  relationship to the other columns) silently gave a bad model; the app now warns
  the user when this happens and defaults to a sensible target column.
- **v3 (`dashboard_v3.py`, final):** Full visual redesign — custom color
  system, professional fonts (Inter + JetBrains Mono), hover animations,
  spacing/typography polish, and a fix making the app work no matter which
  folder it's launched from.

---

## 6. Full Code Walkthrough — `dashboard_v3.py`

This section explains every meaningful block of the final application file, in
the order it runs.

### 6.1 Imports and page config

```python
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
...
st.set_page_config(page_title="Sales Intelligence Platform", page_icon="◆", layout="wide", ...)
```

`st.set_page_config` must be the first Streamlit command in the file — it sets
the browser tab title, icon, and tells the app to use the full browser width
(`layout="wide"`) rather than a narrow centered column.

### 6.2 Design tokens

```python
NAVY = "#0F172A"
INDIGO = "#4F46E5"
EMERALD = "#10B981"
...
```

Rather than scattering colors throughout the code, every color used anywhere in
the app is defined once, here, as a named constant. This is a standard
professional practice: changing the whole app's color scheme later means editing
one block, not hunting through hundreds of lines.

### 6.3 The big CSS block

```python
st.markdown(f"""<style> ... </style>""", unsafe_allow_html=True)
```

Streamlit doesn't expose deep visual customization through its own Python API, so
custom **CSS** (the styling language of web pages) is injected directly using
`st.markdown` with `unsafe_allow_html=True`. This single block controls:
fonts (loaded from Google Fonts), the dark sidebar theme, the hero banner
gradient, metric card shadows and hover lift effects, button styles and hover
states, tab styling, and a responsive `@media` rule that adjusts padding and
font size on small/mobile screens. The `[data-testid="stToolbar"] { display:
none; }` and `.stAppDeployButton { display: none; }` rules specifically hide
Streamlit's own default "Deploy" button, which is unrelated to this project's
functionality and was hidden as requested.

### 6.4 `section_header()` helper function

```python
def section_header(number: str, title: str):
    st.markdown(f"""<div class="section-label">...</div>""", unsafe_allow_html=True)
```

A small reusable function that draws the "01 Data Overview & Cleaning"-style
headers consistently everywhere in the app, instead of repeating the same HTML
three separate times.

### 6.5 Matplotlib global theme

```python
mpl.rcParams.update({...})
```

This sets default chart styling (fonts, colors, removed top/right borders, subtle
gridlines) **once**, so every chart drawn later in the app automatically looks
visually consistent with the rest of the page, without repeating style code in
every single chart.

### 6.6 Sidebar — branding and file upload

```python
with st.sidebar:
    st.markdown(...)  # logo + app name
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], ...)
```

Everything inside `with st.sidebar:` renders in the left panel. `st.file_uploader`
creates the upload control; if the user hasn't uploaded anything,
`uploaded_file` is `None` and the app falls back to sample data.

### 6.7 Loading the data (with the path bug fix)

```python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_CSV_PATH = os.path.join(SCRIPT_DIR, "..", "data", "sales_data.csv")

if uploaded_file is not None:
    df_raw = load_data(uploaded_file)
elif os.path.exists(SAMPLE_CSV_PATH):
    df_raw = load_data(SAMPLE_CSV_PATH)
else:
    st.error(...); st.stop()
```

This fixes a real bug encountered during development: the original code used a
hardcoded relative path (`'../data/sales_data.csv'`), which only worked if the
terminal happened to be inside the `app` folder when launching Streamlit. The fix
uses `__file__` (the script's own file path) to calculate the data folder's
location **relative to the script itself**, so it works no matter which folder
the user runs `streamlit run` from. If the file genuinely doesn't exist, the app
shows a clear message and stops cleanly instead of crashing with a raw Python
traceback.

`@st.cache_data` (just above `load_data`) tells Streamlit to remember the result
of loading a given file, so re-running the app doesn't needlessly re-read the
same CSV from disk every time — a performance best practice.

### 6.8 Automatic data cleaning

```python
duplicates_removed = df.duplicated().sum()
df = df.drop_duplicates()

for col in df.columns:
    if df[col].isnull().sum() > 0:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
```

This is the generalized version of the cleaning done in the notebook — instead of
naming specific columns, it loops over **every** column in **any** uploaded file,
checks its data type, and applies median-fill for numbers or mode-fill for text.
This is what allows the app to correctly clean a completely different dataset
(e.g. employee data) without any code changes.

### 6.9 Automatic column type + date detection

```python
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols]

for c in df.columns:
    if "date" in c.lower():
        df[c] = pd.to_datetime(df[c])
        date_col = c
        break
```

The app inspects the uploaded file's actual column types rather than assuming
fixed column names, and looks for any column with "date" in its name to enable
the time-trend chart.

### 6.10 Sidebar filters

```python
filter_candidates = [c for c in categorical_cols if 1 < df[c].nunique() <= 15]
for fc in filter_candidates[:3]:
    options = sorted(df[fc].dropna().unique().tolist())
    selected = st.multiselect(fc, options, default=options)
    if selected:
        filtered_df = filtered_df[filtered_df[fc].isin(selected)]
```

Only category columns with a *manageable* number of unique values (2 to 15) are
turned into filters — a column like `EmployeeID`, where almost every value is
unique, would produce an unusable 300-option filter, so it's deliberately
excluded. Up to 3 such columns become sidebar multi-select filters.

### 6.11 Visual exploration tabs

Four tabs are built conditionally — only shown if the data actually supports
them (e.g. the "Trend Over Time" tab only appears if a date column was found):

```python
avg_signals = ["age", "score", "rating", "price", "pct", "percent", "ratio", "years", "hours"]
use_average = any(k in val_col.lower() for k in avg_signals)
```

This solves a real bug found during testing: summing a column like `Age` across a
group produces a meaningless "Total Age of 2,340" number. The app now checks the
column name for keywords that suggest it's a **per-entity attribute** (age,
score, rating, etc.) rather than an **additive quantity** (sales, revenue,
count), and automatically uses the **average** instead of the **sum** for those
columns — producing a sensible chart regardless of which dataset is uploaded.

### 6.12 The AI Predictor section

```python
likely_targets = [c for c in numeric_cols if any(k in c.lower() for k in ["total", "sales", "amount", "price", "revenue"])]
default_target = likely_targets[0] if likely_targets else numeric_cols[-1]

X = filtered_df[feature_candidates]
y = filtered_df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

This mirrors exactly what was done in the notebook (Random Forest, train/test
split, MAE and R² evaluation), but now: the target column is chosen by the user
through a dropdown (defaulting intelligently to a column that looks like a
sales/revenue/price figure), the model retrains live on whatever filtered data is
currently selected, and a warning appears automatically if R² comes out low,
explaining *why* in plain language rather than just showing a bad number.

### 6.13 Live prediction and feature importance

```python
input_values[feature] = input_cols[i].number_input(feature, ..., value=mean_val)
...
if st.button("Predict", type="primary"):
    prediction = model.predict(pd.DataFrame([input_values]))[0]
```

Each feature gets its own number input box, pre-filled with that column's average
value as a sensible starting point. Clicking **Predict** packages the current
input values into a single-row DataFrame (the same shape the model was trained
on) and asks the model for a prediction, which is then displayed in a styled
result panel.

### 6.14 Downloads

```python
st.download_button("↓  Download cleaned data (CSV)", data=filtered_df.to_csv(index=False).encode("utf-8"), ...)
```

`DataFrame.to_csv(index=False)` converts the table back into CSV text (without
adding an extra row-number column), `.encode("utf-8")` turns that text into bytes
(which is what the download button requires), and `st.download_button` renders a
button that saves those bytes as a file when clicked — no server-side file
writing needed.

---

## 7. Syllabus Coverage Map

| Module | Topic | Where it was applied |
|---|---|---|
| 1 | Introduction to AI | Entire project is a hands-on real-world AI application |
| 2 | Python Fundamentals | Variables, functions, loops, conditionals — used throughout every script |
| 3 | NumPy | Used internally by Pandas/scikit-learn; used directly to generate sample datasets |
| 4 | Pandas | DataFrames, `read_csv`, filtering, sorting, `groupby` — Section 4.1–4.3 |
| 5 | Data Visualization | Bar, line, pie, histogram, scatter charts — Section 4.4 |
| 6 | Data Preprocessing | Duplicate removal, missing value imputation — Section 4.5, 6.8 |
| 7 | Statistics for AI | Mean, median, std, correlation — Section 4.2, 4.6 |
| 8 | ML Fundamentals | Train/test split workflow — Section 4.7 |
| 9 | Supervised Learning | Linear Regression, Random Forest — Section 4.7, 4.8 |
| 10 | Unsupervised Learning | Not yet covered — natural next step (e.g. customer segmentation with K-Means) |
| 11 | Model Evaluation | MAE, R², model comparison, feature importance — Section 4.8, 4.9 |
| 12 | Deep Learning | Not yet covered |
| 13 | Computer Vision | Not yet covered |
| 14 | NLP | Not yet covered |
| 15 | Generative AI & LLMs | Claude used throughout as a learning/coding assistant |
| 16 | AI Tools | Hands-on use of Claude; awareness of ChatGPT, Gemini, Copilot, etc. |

---

## 8. How to Run This Project

1. Open the project folder in VS Code: `D:\AI-Engineer-Project`.
2. Open a terminal and activate the virtual environment:
   ```
   venv\Scripts\Activate.ps1
   ```
3. Navigate into the app folder and run the app:
   ```
   cd app
   streamlit run dashboard.py
   ```
4. The app opens automatically in the browser at `http://localhost:8501`.
   Upload any CSV, or do nothing to use the bundled sample sales data.
5. To stop the app, go back to the terminal and press `Ctrl+C`.

---

## 9. Key Concepts Glossary

**DataFrame** — Pandas' table structure: rows and columns, like a spreadsheet,
but manipulated with code.

**Feature** — An input column given to a machine learning model.

**Target** — The column a machine learning model is trying to predict.

**Train/test split** — Dividing data so a model learns from one portion and is
honestly evaluated on a separate portion it never saw during training.

**Median** — The middle value of a sorted list; robust to extreme outliers,
which is why it's preferred over the mean when filling missing numeric data.

**Mode** — The most frequently occurring value in a column; used to fill missing
category/text data.

**Correlation** — A number from −1 to +1 describing how strongly two numeric
columns move together.

**R² Score** — A model evaluation metric from roughly 0 to 1 describing what
fraction of the variation in the target the model successfully explains. Closer
to 1 is better.

**MAE (Mean Absolute Error)** — The average size of the model's prediction
errors, in the same units as the target column. Lower is better.

**Random Forest** — A machine learning algorithm that builds many decision trees
on random subsets of the data and averages their predictions, generally more
accurate than a single straight-line model for complex, non-linear
relationships.

**Feature Importance** — A score, produced by certain models like Random Forest,
indicating how much each input column contributed to the model's predictions.

**Virtual environment (venv)** — An isolated copy of Python and its libraries for
one specific project, so different projects' dependencies don't conflict.

**CSV (Comma-Separated Values)** — A plain-text file format for tabular data,
where each line is a row and commas separate column values.
