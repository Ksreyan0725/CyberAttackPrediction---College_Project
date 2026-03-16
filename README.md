# 🛡️ Cyber Attack Prediction: From Traditional ML to Generative AI

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask-red.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive final year BCA project that predicts network intrusions using advanced Machine Learning (Random Forest) and provides human-readable mitigation strategies using a simulated Generative AI engine.

---

## 🚀 Key Features

- **Multi-Model Analysis**: Utilizes Random Forest, DNN, and Hybrid Stacking for high-accuracy detection.
- **Generative AI Insights**: Provides natural language explanations for detected attacks (e.g., Neptune, Teardrop, Smurf).
- **Modern Web UI**: A clean, Bootstrap 5-powered dashboard for easy data upload and analysis.
- **Explainable AI (XAI)**: Includes SHAP interpretation to show *why* the AI made a specific decision.
- **Academic Ready**: Comes with a 2000+ line [PROJECT_GUIDE.md](PROJECT_GUIDE.md) and full team details.

---

## 🏛️ Project Information

- **Institution**: Roland Institute of Computer & Mgmt. Studies, Surya Vihar, Berhampur
- **Academic Year**: 2023-2026 (6th Semester)
- **Guide Teacher**: Mr. Rasmi Roy Badakumar

### 👥 Team Members
- **Kumar Sreyan Pattanayak** (Roll No: 23PBCA1355)
- **Ankita Pati** (Roll No: 23PBCA1335)
- **Subhashree Pathy** (Roll No: 23PBCA1386)
- **Tanmaya Ranjan Jena** (Roll No: 23PBCA1391)

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ksreyan0725/CyberAttackPrediction---College_Project.git
   cd CyberAttackPrediction---College_Project
   ```

2. **Setup Virtual Environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r CyberAttackPrediction/requirements.txt
   ```

4. **Train the Model**:
   ```bash
   python CyberAttackPrediction/train_model.py
   ```

5. **Run the Application**:
   ```bash
   .\Start_WebApp_Venv.bat
   ```

---

## 📊 Dataset Reference
This project primarily uses the **NSL-KDD** dataset, an industry-standard benchmark for network intrusion detection systems, solving the redundancy issues of the original KDD'99 dataset.

---

## 📂 Documentation
For an exhaustive deep dive into the code, logic, and Viva preparation, please refer to the master guide:
[PROJECT_GUIDE.md](PROJECT_GUIDE.md)

---

## 🏗️ Project Structure (Clickable)
*Explore the project files directly!*

- 📁 [CyberAttackPrediction](CyberAttackPrediction/) (Main Project Folder)
    - 📁 [static](CyberAttackPrediction/static/) (Styles & Images)
        - 📄 [default.css](CyberAttackPrediction/static/default.css) (Colors and Layout)
    - 📁 [templates](CyberAttackPrediction/templates/) (The Webpages)
        - 📄 [base.html](CyberAttackPrediction/templates/base.html) (The Master Layout)
        - 📄 [index.html](CyberAttackPrediction/templates/index.html) (Home Page)
        - 📄 [Predict.html](CyberAttackPrediction/templates/Predict.html) (The Upload Page)
        - 📄 [UserLogin.html](CyberAttackPrediction/templates/UserLogin.html) (Login Page)
        - 📄 [UserScreen.html](CyberAttackPrediction/templates/UserScreen.html) (Results Page)
    - 📁 [model](CyberAttackPrediction/model/) (The AI's Brain Files)
    - 📁 [Dataset](CyberAttackPrediction/Dataset/) (The Textbooks/Data)
    - 🐍 [Main.py](CyberAttackPrediction/Main.py) (The Heart of the Project)
    - 🐍 [train_model.py](CyberAttackPrediction/train_model.py) (The AI Trainer script)
    - 📄 [requirements.txt](CyberAttackPrediction/requirements.txt) (List of needed libraries)

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
