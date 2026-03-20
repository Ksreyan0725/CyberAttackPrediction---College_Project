# 🛡️ Cyber Attack Prediction: From Traditional ML to Generative AI

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask-red.svg)](https://flask.palletsprojects.com/)
[![Jupyter](https://img.shields.io/badge/notebook-Jupyter-orange.svg)](https://jupyter.org/)

A comprehensive final year BCA project that predicts network intrusions using advanced Machine Learning (Random Forest) and provides human-readable mitigation strategies using a simulated Generative AI engine.

---

## 🚀 Key Features

- **Liquid Glass UI**: Premium glassmorphism aesthetic with translucent panels and animated background refractive blobs.
- **Smart Security**: Implements an inactivity-based logout (1 hour) and page-context-aware reload protection for results.
- **Split Login UI**: A premium, dual-panel login screen with character-by-character typing animations and password visibility toggle.
- **Explainable AI (XAI)**: Includes SHAP interpretation to show *why* the AI made a specific decision.
- **Jupyter Research**: Includes `.ipynb` notebooks used for the initial model proposal, extension research, and performance benchmarking.
- **Academic Ready**: Comes with a 2000+ line [PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) and full team details.

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

For an exhaustive deep dive into the code, logic, and Viva preparation, please refer to the master guides:

- 📖 [PROJECT_BOOK.md](CyberAttackPrediction/PROJECT_BOOK.md) (Step-by-Step Technical Guide)
- 📖 [PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) (Master Project Manual)
- 🎓 [BeReady.md](docs/BeReady.md) (Interactive Study Guide Checklist)
- 📝 [BeReady.txt](docs/BeReady.txt) (Plain Text Study Guide)
- 🎨 [UI_Refinement_Walkthrough.md](docs/UI_Refinement_Walkthrough.md) (UI improvements details)

---

## 🏗️ Project Structure (Clickable)

*Explore the project files directly!*

- 📁 [CyberAttackPrediction](CyberAttackPrediction/) (Main Project Folder)
  - 📁 [static](CyberAttackPrediction/static/) (Styles & Images)
    - 📄 [default.css](CyberAttackPrediction/static/default.css) (Colors and Layout)
  - 📁 [templates](CyberAttackPrediction/templates/) (The Webpages)
    - 📄 [base.html](CyberAttackPrediction/templates/base.html) (The Master Layout)
    - [index.html](CyberAttackPrediction/templates/index.html) (Home Page)
    - [Predict.html](CyberAttackPrediction/templates/Predict.html) (The Upload Page)
    - [UserLogin.html](CyberAttackPrediction/templates/UserLogin.html) (Split Login Page)
    - [UserScreen.html](CyberAttackPrediction/templates/UserScreen.html) (Results Page)
    - [HowItWorks.html](CyberAttackPrediction/templates/HowItWorks.html) (GenAI Explainers)
  - 📁 [model](CyberAttackPrediction/model/) (The AI's Brain Files)
  - 📁 [Dataset](CyberAttackPrediction/Dataset/) (The Textbooks/Data)
  - 🐍 [Main.py](CyberAttackPrediction/Main.py) (The Heart of the Project)
  - 🐍 [train_model.py](CyberAttackPrediction/train_model.py) (The AI Trainer script)
  - 📔 [ExtensionCyberAttack.ipynb](CyberAttackPrediction/ExtensionCyberAttack.ipynb) (Research & Extension)
  - 📔 [ProposeCyberAttack.ipynb](CyberAttackPrediction/ProposeCyberAttack.ipynb) (Initial Model Proposal)
  - 📖 [PROJECT_BOOK.md](CyberAttackPrediction/PROJECT_BOOK.md) (Full Technical Guide)
  - 📄 [requirements.txt](CyberAttackPrediction/requirements.txt) (List of needed libraries)
- 📁 [Soft](Soft/) (Essential Software/Installers)
  - 📁 [vs_Community](Soft/vs_Community/) (Visual Studio Setup)
  - 🐍 [Python_v3.7.2.exe](Soft/Python_%2864bit%29_v3.7.2.exe)
  - 📄 [mysql-5.5.46.msi](Soft/mysql-5.5.46-win32.msi)
  - 📄 [node-v12.13.1.msi](Soft/node-v12.13.1-x64.msi)
- 📁 [model](model/) (Extra Model storage)
- 📁 [docs/](docs/) (Documentation, Study Guides, & Manuals)
- 📁 [backups/](backups/) (Original zip files provided by college)
- ⚙️ [Start_WebApp_Venv.bat](Start_WebApp_Venv.bat) (Quick launcher)

---

### Built with ❤️ for Academic Excellence - 2026
