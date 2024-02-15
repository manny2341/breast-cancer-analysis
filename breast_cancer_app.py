"""
Breast Cancer Detection Web App
Streamlit Application — SVM Model
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="Breast Cancer Detection",
    page_icon="🎗️",
    layout="wide"
)

# ── STYLING ──────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #c0392b 100%);
        padding: 2rem; border-radius: 10px;
        text-align: center; margin-bottom: 2rem;
    }
    .main-header h1 { color: white; font-size: 2.2rem; margin: 0; }
    .main-header p  { color: #ffcccc; font-size: 1rem; margin: 0.5rem 0 0 0; }
    .result-cancer {
        background: #fff0f0; padding: 1.5rem; border-radius: 10px;
        border: 3px solid #c0392b; text-align: center;
        font-size: 1.5rem; font-weight: bold; color: #c0392b;
    }
    .result-safe {
        background: #f0fff0; padding: 1.5rem; border-radius: 10px;
        border: 3px solid #27ae60; text-align: center;
        font-size: 1.5rem; font-weight: bold; color: #27ae60;
    }
    .metric-box {
        background: #1a1a2e; color: white;
        padding: 1rem; border-radius: 8px; text-align: center;
    }
    .metric-box h3 { color: #ffcc00; margin: 0; font-size: 1.8rem; }
    .metric-box p  { color: #aaaaaa; margin: 0.3rem 0 0 0; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎗️ Breast Cancer Detection System</h1>
    <p>SVM Machine Learning Model — Trained on 569 patients — 97.5% Accuracy</p>
</div>
""", unsafe_allow_html=True)

# ── LOAD AND TRAIN MODEL ─────────────────────────────────────
@st.cache_resource
def train_model():
    df      = pd.read_csv("dataset_before_preprocessing.csv").drop("ID", axis=1)
    X       = df.drop("Diagnosis", axis=1)
    y       = df["Diagnosis"]
    scaler  = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    models = {
        "SVM (Best)":            SVC(probability=True, random_state=42),
        "Random Forest":         RandomForestClassifier(n_estimators=100, random_state=42),
        "Logistic Regression":   LogisticRegression(max_iter=1000, random_state=42),
    }
    for m in models.values():
        m.fit(X_scaled, y)

    return models, scaler, list(X.columns)

models, scaler, feature_names = train_model()

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### About")
    st.info("Enter cell measurements from a biopsy scan to check for breast cancer.")

    st.markdown("### Model")
    selected_model = st.selectbox(
        "Choose model",
        list(models.keys()),
        help="SVM is the most accurate — 97.5% cross-validation score"
    )

    st.markdown("### Model Performance")
    perf = {
        "SVM (Best)":          {"Accuracy": "97.4%", "AUC": "0.995"},
        "Random Forest":        {"Accuracy": "97.4%", "AUC": "0.993"},
        "Logistic Regression":  {"Accuracy": "96.5%", "AUC": "0.998"},
    }
    for metric, val in perf[selected_model].items():
        st.success(f"{metric}: {val}")

    st.markdown("### How to Use")
    st.markdown("""
    1. Enter the cell measurements below
    2. Click **Run Detection**
    3. See the result and confidence score

    > All values come from a biopsy cell scan report.
    """)

    st.markdown("### Disclaimer")
    st.warning("This tool is for educational purposes only. Always consult a qualified doctor.")

# ── MAIN TABS ────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Detection", "Model Results", "About the Data"])

# ── TAB 1: DETECTION ─────────────────────────────────────────
with tab1:
    st.markdown("## Enter Cell Measurements")
    st.caption("Enter the values from the biopsy scan report. All fields are required.")

    # Group features into 3 sections
    mean_features  = [f for f in feature_names if f.endswith("_mean")]
    se_features    = [f for f in feature_names if f.endswith("_se")]
    worst_features = [f for f in feature_names if f.endswith("_worst")]

    # Default sample values (malignant example from dataset)
    defaults = {
        "radius_mean": 17.99, "texture_mean": 10.38, "perimeter_mean": 122.8,
        "area_mean": 1001.0,  "smoothness_mean": 0.1184, "compactness_mean": 0.2776,
        "concavity_mean": 0.3001, "concave_points_mean": 0.1471,
        "symmetry_mean": 0.2419, "fractal_dimension_mean": 0.07871,
        "radius_se": 1.095, "texture_se": 0.9053, "perimeter_se": 8.589,
        "area_se": 153.4, "smoothness_se": 0.006399, "compactness_se": 0.04904,
        "concavity_se": 0.05373, "concave_points_se": 0.01587,
        "symmetry_se": 0.03003, "fractal_dimension_se": 0.006193,
        "radius_worst": 25.38, "texture_worst": 17.33, "perimeter_worst": 184.6,
        "area_worst": 2019.0, "smoothness_worst": 0.1622, "compactness_worst": 0.6656,
        "concavity_worst": 0.7119, "concave_points_worst": 0.2654,
        "symmetry_worst": 0.4601, "fractal_dimension_worst": 0.1189,
    }

    input_vals = {}

    st.markdown("#### Mean Measurements (average cell values)")
    cols = st.columns(2)
    for i, feat in enumerate(mean_features):
        with cols[i % 2]:
            input_vals[feat] = st.number_input(
                feat.replace("_mean","").replace("_"," ").title() + " (mean)",
                value=float(defaults.get(feat, 0.0)),
                format="%.4f", key=feat
            )

    st.markdown("#### Standard Error Measurements")
    cols = st.columns(2)
    for i, feat in enumerate(se_features):
        with cols[i % 2]:
            input_vals[feat] = st.number_input(
                feat.replace("_se","").replace("_"," ").title() + " (SE)",
                value=float(defaults.get(feat, 0.0)),
                format="%.4f", key=feat
            )

    st.markdown("#### Worst Measurements (largest values seen)")
    cols = st.columns(2)
    for i, feat in enumerate(worst_features):
        with cols[i % 2]:
            input_vals[feat] = st.number_input(
                feat.replace("_worst","").replace("_"," ").title() + " (worst)",
                value=float(defaults.get(feat, 0.0)),
                format="%.4f", key=feat
            )

    st.markdown("---")

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        run = st.button("🔬 Run Detection", type="primary", use_container_width=True)
    with col_btn2:
        st.caption("Pre-filled with a sample malignant case for demonstration.")

    if run:
        # Build input array in correct order
        input_array = np.array([[input_vals[f] for f in feature_names]])
        input_scaled = scaler.transform(input_array)

        model = models[selected_model]
        prediction   = model.predict(input_scaled)[0]
        probability  = model.predict_proba(input_scaled)[0]

        benign_prob    = probability[0] * 100
        malignant_prob = probability[1] * 100

        st.markdown("---")
        st.markdown("## Result")

        if prediction == 1:
            st.markdown(f"""
            <div class="result-cancer">
                ⚠️ MALIGNANT — Cancerous tumour detected<br>
                <span style="font-size:1rem; font-weight:normal">
                Confidence: {malignant_prob:.1f}%
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                ✅ BENIGN — No cancer detected<br>
                <span style="font-size:1rem; font-weight:normal">
                Confidence: {benign_prob:.1f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # Confidence bar chart
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Confidence Breakdown")
            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_facecolor("#1a1a2e")
            ax.set_facecolor("#1a1a2e")
            bars = ax.bar(
                ["Benign\n(No Cancer)", "Malignant\n(Cancer)"],
                [benign_prob, malignant_prob],
                color=["#27ae60", "#c0392b"],
                edgecolor="white", linewidth=0.8
            )
            for bar, val in zip(bars, [benign_prob, malignant_prob]):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f"{val:.1f}%", ha="center", color="white",
                        fontsize=12, fontweight="bold")
            ax.set_ylim(0, 115)
            ax.set_ylabel("Confidence (%)", color="white")
            ax.tick_params(colors="white")
            for spine in ax.spines.values():
                spine.set_edgecolor("#444")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown("### Most Important Measurements")
            # Show top 5 features ranked by how far they are from benign average
            df_ref = pd.read_csv("dataset_before_preprocessing.csv").drop("ID", axis=1)
            benign_avg = df_ref[df_ref["Diagnosis"] == 0][feature_names].mean()

            diffs = {}
            for feat in feature_names:
                diffs[feat] = abs(input_vals[feat] - benign_avg[feat])

            top5 = sorted(diffs.items(), key=lambda x: x[1], reverse=True)[:5]
            top5_names  = [t[0].replace("_", " ") for t in top5]
            top5_vals   = [t[1] for t in top5]

            fig2, ax2 = plt.subplots(figsize=(5, 3))
            fig2.patch.set_facecolor("#1a1a2e")
            ax2.set_facecolor("#1a1a2e")
            ax2.barh(top5_names[::-1], top5_vals[::-1],
                     color="#e74c3c", edgecolor="white", linewidth=0.8)
            ax2.set_xlabel("How far from normal", color="white", fontsize=10)
            ax2.set_title("Top 5 Suspicious Measurements",
                          color="white", fontsize=11, fontweight="bold")
            ax2.tick_params(colors="white", labelsize=9)
            for spine in ax2.spines.values():
                spine.set_edgecolor("#444")
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

        st.warning("This result is from a machine learning model and must not replace professional medical diagnosis.")

# ── TAB 2: MODEL RESULTS ─────────────────────────────────────
with tab2:
    st.markdown("## How Well Do the Models Perform?")

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Best Accuracy",  "97.4%", "SVM & Random Forest"),
        ("Best AUC",       "0.998", "Logistic Regression"),
        ("Cross Val Score","97.5%", "SVM"),
        ("Patients Trained","569",  "Wisconsin Dataset"),
    ]
    for col, (label, val, note) in zip([col1,col2,col3,col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <h3>{val}</h3>
                <p>{label}</p>
                <p style="font-size:0.75rem">{note}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("### Model Comparison")

    import json
    try:
        with open("model_results.json") as f:
            results = json.load(f)
        df_results = pd.DataFrame(results).T.round(1)
        df_results.columns = ["Accuracy (%)", "Precision (%)", "Recall (%)", "F1 Score (%)"]
        st.dataframe(df_results, use_container_width=True)
    except:
        st.info("Run the analysis notebook first to generate model results.")

    st.markdown("### Cross Validation Results")
    try:
        with open("cv_results.json") as f:
            cv = json.load(f)
        cv_data = {k: {"Average (%)": round(v["mean"],1), "Consistency ±": round(v["std"],1)}
                   for k, v in cv.items()}
        st.dataframe(pd.DataFrame(cv_data).T, use_container_width=True)
    except:
        st.info("Run the analysis notebook first to generate CV results.")

    st.markdown("### Training Charts")
    chart_cols = st.columns(2)
    charts = ["chart5_model_comparison.png", "chart7_roc_curves.png"]
    for col, chart in zip(chart_cols, charts):
        try:
            with col:
                st.image(chart, use_container_width=True)
        except:
            pass

# ── TAB 3: ABOUT THE DATA ────────────────────────────────────
with tab3:
    st.markdown("## About the Dataset")
    st.markdown("""
    ### Breast Cancer Wisconsin (Diagnostic) Dataset

    This dataset was collected by the University of Wisconsin and is one of the most
    well-known medical datasets in machine learning.

    | Detail | Value |
    |---|---|
    | Total patients | 569 |
    | Benign (no cancer) | 357 |
    | Malignant (cancer) | 212 |
    | Measurements per patient | 30 |
    | Missing values | None |

    ### What Are the Measurements?

    Each measurement comes from a **digitised image of a biopsy** — a small sample
    of tissue taken from the lump. A computer analyses the cell shapes and records:

    - **Radius** — how big the cell is
    - **Texture** — how rough or smooth the surface is
    - **Perimeter** — the distance around the cell
    - **Area** — total size of the cell
    - **Smoothness** — variation in the radius
    - **Compactness** — how round vs irregular the cell is
    - **Concavity** — number of dents in the cell surface
    - **Symmetry** — how symmetrical the cell is
    - **Fractal Dimension** — how complex the cell border is

    Each is measured **3 times** — mean, standard error, and worst — giving 30 total features.

    ### Key Finding

    Cancer cells tend to be **larger, rougher, and more irregular** than healthy cells.
    These differences are strong enough for the model to detect cancer with **97.5% accuracy**.
    """)

    st.markdown("### Data Charts")
    chart_cols = st.columns(2)
    for col, chart in zip(chart_cols*2,
                          ["chart1_diagnosis_count.png", "chart2_feature_comparison.png",
                           "chart3_top_features.png",    "chart4_distributions.png"]):
        try:
            with col:
                st.image(chart, use_container_width=True)
        except:
            pass
