# Cyber Attack Prediction — Comprehensive Project Guide (Updated 2026)

Welcome to the Cyber Attack Prediction project! This guide covers the modernized architecture, datasets, ML/DL models, Generative AI integration, and instructions for running the system.

---

## 1. Project Overview & Architecture

This project is an advanced Machine Learning and Deep Learning-based **Intrusion Detection System (IDS)** that classifies network traffic as **"Normal"** or a specific **"Cyber Attack"**.

The project features a hybrid architecture:

- **A. Research Environment** (Jupyter Notebooks): For data analysis, model comparison, and Deep Learning experiments.
- **B. Production Web Application** (Flask + Bootstrap 5): A modernized, responsive UI for real-time predictions.
- **C. Model Persistence Layer**: A dedicated training script (`train_model.py`) to save models, ensuring the web app is fast and efficient.
- **D. Generative AI Insight Engine**: Automatically generates natural language explanations and mitigation steps for detected attacks.

---

## 2. Dataset Analysis

The system evaluates models across four major cybersecurity datasets:

- **NSL-KDD** (`kdd_train.csv`): Primary dataset for the web app and research baseline.
- **CICIDS 2017**, **CICDDoS 2019**, **X-IIoTID**: Used in the research notebooks for multi-algorithm benchmarking.
- **Custom Captures**: User-provided CSV files for testing and inference via the web app.

### Preprocessing Steps

| Step | What It Does |
| --- | --- |
| Label Encoding | Converts text/categorical columns to numbers |
| Imputation | Fills in missing values with means or zeros |
| Normalization | Scales all features to a comparable range using `StandardScaler` |

---

## 3. AI & Machine Learning Models

### Traditional ML & Deep Learning

- Random Forest, KNN, SVM, MLP, Logistic Regression, Naive Bayes
- Deep Neural Networks (DNN) built with Keras/TensorFlow

### Generative AI Integration *(New)*

After a prediction is made, the system provides a detailed AI-generated explanation of the threat and recommended security measures.

### Explainable AI (XAI)

Uses **SHAP** (SHapley Additive exPlanations) in the notebooks to visualize which network features most impacted the model's decision.

---

## 4. Folder Structure

### Inside `CyberAttackPrediction/`

| File / Folder | Description |
| --- | --- |
| `Main.py` | The Flask backend server (optimized for model loading) |
| `train_model.py` | Run this to train and save the ML model to disk |
| `.env` | Secure storage for admin credentials and secret keys |
| `templates/base.html` | Modern Jinja2 base template with Bootstrap 5 |
| `model/trained_rf_model.pkl` | The persistent, pre-trained model file |
| `requirements.txt` | All dependencies including `python-dotenv` |

### Inside the main `Project/` folder

| File / Folder | Description |
| --- | --- |
| `.venv` | Isolated Python virtual environment containing all libraries |
| `.gitignore` | Keeps bulky datasets and sensitive `.env` files out of version control |

---

## 5. How to Run the Project

### Step 1: Initial Setup *(First Time Only)*

1. Open a terminal in the project root.
2. Install dependencies:

   ```bat
   .venv\Scripts\python.exe -m pip install -r CyberAttackPrediction\requirements.txt
   ```

3. Train the model:

   ```bat
   .venv\Scripts\python.exe CyberAttackPrediction\train_model.py
   ```

### Step 2: Running the Project

#### A. Research & Notebooks

1. Double-click **`Start_Jupyter_Venv.bat`** in the main folder.
2. Open `ExtensionCyberAttack.ipynb` or `ProposeCyberAttack.ipynb`.
3. Run cells to view graphs, model comparisons, and SHAP plots.

#### B. User-Facing Web Application

1. Double-click **`Start_WebApp_Venv.bat`** in the main folder.
2. Wait for `Running on http://127.0.0.1:2026/` in the terminal.
3. Open <http://127.0.0.1:2026> in your browser.
4. Login using the credentials in your `.env` file *(default: admin / admin)*.
5. Upload `testData.csv` to see real-time predictions and AI insights.

---

> **Important:** Always use the `.bat` files or the `.venv` path to ensure you are using the correct Python version and libraries.
