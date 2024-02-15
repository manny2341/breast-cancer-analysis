# Breast Cancer Detection System

A machine learning project that predicts whether a breast tumour is cancerous or not, based on 30 measurements taken from a cell scan. Built and trained on 569 real patients with 97.5% accuracy.

---

## What This Project Does

A doctor takes a small sample of cells from a lump (called a biopsy). A computer measures the shape and size of those cells. This system looks at those measurements and answers one question:

> **Is this tumour Malignant (cancerous) or Benign (not cancerous)?**

---

## Prerequisites

- Python 3.13
- The libraries listed in requirements.txt

---

## Installation

```bash
# Clone the repository
git clone https://github.com/manny2341/breast-cancer-analysis.git
cd breast-cancer-analysis

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### Web App
```bash
streamlit run breast_cancer_app.py
```
Open your browser at `http://localhost:8501`

### Full Analysis Script
```bash
python3 breast_cancer_analysis.py
```

### Presentation Slides
```bash
python3 create_slides.py
```
Opens `Breast_Cancer_Detection_Presentation.pptx`

---

## Project Structure

```
breast-cancer-analysis/
├── breast_cancer_app.py                  # Streamlit web application
├── breast_cancer_analysis.py             # Full analysis script
├── create_slides.py                      # Generates PowerPoint presentation
├── dataset_before_preprocessing.csv      # Original raw dataset
├── dataset_after_preprocessing.csv       # Cleaned and scaled dataset
├── model_results.json                    # Accuracy results for all 6 models
├── cv_results.json                       # Cross validation results
├── CLAUDE_ANALYSIS_PROMPT.md             # Prompt to ask Claude to explain the project
├── chart1_diagnosis_count.png            # Cancer vs no cancer counts
├── chart2_feature_comparison.png         # Measurements comparison chart
├── chart3_top_features.png               # Top 10 cancer indicators
├── chart4_distributions.png              # How cancer cells differ from healthy cells
├── chart5_model_comparison.png           # All 6 model scores side by side
├── chart6_confusion_matrix.png           # What each model got right and wrong
└── chart7_roc_curves.png                 # ROC curves for all models
```

---

## The Dataset

**Breast Cancer Wisconsin (Diagnostic) Dataset**

| Detail | Value |
|---|---|
| Total patients | 569 |
| Benign (no cancer) | 357 |
| Malignant (cancer) | 212 |
| Measurements per patient | 30 |
| Missing values | None |

### The 30 Measurements

Each of these is recorded 3 times — mean, standard error, and worst:

| Measurement | What It Means |
|---|---|
| Radius | How big the cell is |
| Texture | How rough or smooth the surface is |
| Perimeter | Distance around the cell |
| Area | Total size of the cell |
| Smoothness | Variation in the radius |
| Compactness | How round vs irregular the cell is |
| Concavity | Number of dents in the surface |
| Concave Points | Number of concave parts of the border |
| Symmetry | How symmetrical the cell is |
| Fractal Dimension | How complex the cell border is |

---

## Step-by-Step Process

### Step 1 — Explored the Data
- 569 patients, 32 columns, 0 missing values
- 357 benign, 212 malignant

### Step 2 — Cleaned the Data
- Removed the ID column (useless random number)
- No missing values to handle
- Scaled all measurements using StandardScaler so the computer treats them equally

### Step 3 — Visualised the Data
- Cancer cells are bigger, rougher, and more irregular than healthy cells
- `concave_points_worst` is the strongest cancer indicator (correlation 0.79)
- The two groups are clearly different — the computer has strong patterns to learn

### Step 4 — Trained 6 Models

| Model | How It Works |
|---|---|
| Logistic Regression | Draws a straight line between cancer and no cancer |
| Decision Tree | Asks yes/no questions to reach an answer |
| Random Forest | 100 decision trees all voting together |
| Gradient Boosting | Each tree learns from the mistakes of the last |
| SVM | Finds the best possible boundary between groups |
| KNN | Looks at the 5 most similar patients and copies them |

### Step 5 — Evaluated the Models
- Used accuracy, precision, recall, F1 score
- Ran cross validation (tested 5 times each on different data)
- Checked confusion matrix — what did each model get right and wrong
- Plotted ROC curves — how well does each model separate cancer from no cancer

### Step 6 — Built a Web App
- Anyone can enter measurements and get a prediction
- Shows confidence score and most suspicious measurements
- Switch between 3 models from the sidebar

---

## Model Results

### Single Test Results

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | 96.5% | 95.1% | 92.9% | 95.1% |
| Decision Tree | 93.0% | 90.5% | 90.5% | 90.5% |
| Random Forest | 97.4% | 100% | 92.9% | 96.3% |
| Gradient Boosting | 96.5% | 97.6% | 90.5% | 95.0% |
| **SVM** | **97.4%** | **100%** | **92.9%** | **96.3%** |
| KNN | 95.6% | 97.4% | 90.5% | 93.8% |

### Cross Validation (tested 5 times each)

| Model | Average Score | Consistency |
|---|---|---|
| Logistic Regression | 97.4% | ±1.7% |
| Decision Tree | 91.0% | ±2.8% |
| Random Forest | 95.4% | ±1.3% |
| Gradient Boosting | 95.1% | ±2.5% |
| **SVM** | **97.5%** | **±2.0%** |
| KNN | 96.7% | ±1.4% |

---

## The Winner — SVM

| Metric | Score |
|---|---|
| Accuracy | 97.4% |
| Cross Validation | 97.5% |
| AUC | 0.995 |
| Cancer cases missed | 3 out of 114 tested |

SVM scored the highest cross validation score meaning it performs consistently no matter what data it sees. It only missed 3 cancer cases out of 114 patients in testing.

---

## Web App Features

| Tab | What It Does |
|---|---|
| Detection | Enter 30 measurements → get Cancer / No Cancer result with confidence score |
| Model Results | Full table of all 6 model scores, cross validation results, charts |
| About the Data | Explains the dataset, measurements, and all analysis charts |

---

## Key Findings

- Cancer cells are significantly **larger** than healthy cells
- Cancer cells have more **irregular and dented** shapes
- The **worst measurements** (largest values seen) are better predictors than average values
- All 6 models performed well — the data has very clear patterns

---

## Data Source

Breast Cancer Wisconsin (Diagnostic) Dataset
University of Wisconsin — available on UCI Machine Learning Repository

---

## Disclaimer

This project is for **educational purposes only**. It must not be used as a substitute for professional medical diagnosis. Always consult a qualified doctor.

---

## Licence

MIT Licence — free to use, modify, and distribute with attribution.
