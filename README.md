# 🛡️ Cyber Attack Prediction: From Traditional ML to Generative AI

<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img src="CyberAttackPrediction/static/images/favicon.svg" alt="CyberShield AI Logo" width="160" height="160">
</p>

<h1 align="center">CyberShield AI</h1>

<p align="center">
  <strong>Predicting network intrusions with precision. Explaining security with intelligence.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue.svg?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/flask-v3.0-EA4335.svg?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E.svg?style=for-the-badge&logo=scikit-learn" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Status-Academic--Ready-success.svg?style=for-the-badge" alt="Status">
</p>

---

## 🌟 Executive Summary

**CyberShield AI** is a final-year Bachelor of Computer Applications (BCA) project that bridges the gap between traditional network security and modern Artificial Intelligence. By analyzing network traffic patterns using the industry-standard **NSL-KDD dataset**, the system classifies attacks into four primary families (DoS, Probe, R2L, U2R) and provides human-readable mitigation strategies via a simulated Generative AI engine.

---

## 🚀 Key Features

| **🚀 Dual-Docs** | Features a two-stage documentation experience: A high-level **Interactive Overview** for beginners and a **Repository Explorer** for technical deep dives. |
| **💎 Liquid Glass UI** | A premium, responsive interface featuring glassmorphism, translucency, and refractive background animations for a modern feel. |
| **🧠 Stacking ML** | Uses a multi-model stacking architecture (Random Forest, KNN, MLP) for superior prediction accuracy over single-model systems. |
| **🔍 XAI (SHAP)** | Explainable AI that visually breaks down *why* a specific network packet was flagged as an attack using SHAP values. |
| **🛡️ Secure Auth** | Integrated **Hashed Multi-User Authentication** using PBKDF2 with SHA256. Features account management, signup capabilities, and ultimate admin bypass. |
| **🤖 GenAI Insights** | Transforms complex technical results into clear, actionable advice for security administrators. |

---

## 📊 Project Evolution & Roadmap

![Project Roadmap](Project%20materials/roadmap.png)
*Above: The systematic development lifecycle from data ingestion to Generative AI integration.*

---

## 🛡️ Cybersecurity Foundations

This project is built upon the core principles of network defense.

![Five Pillars](Project%20materials/five%20pillors%20of%20cybersecurity.png)
*The system aligns with standard cybersecurity frameworks to ensure comprehensive protection and monitoring.*

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

4. **Run the Application**:
   Launch via `Start_WebApp_Venv.bat` or `python CyberAttackPrediction/Main.py`.

---

- 🌟 [**Documentation Overview**](/documentation) — The primary interactive summary and project guide.
- 📂 [**Repository Explorer**](/explorer) — Interactive technical browser for all source code and notebooks.
- 📖 [**Full Project Manual**](docs/PROJECT_GUIDE.md) — Comprehensive 2000+ line technical manual and Viva Q&A.
- 🎓 [**Academic Readiness**](docs/BeReady.md) — The interactive BCA syllabus and readiness checklist.
- 🎨 [**Design Walkthrough**](docs/UI_Refinement_Walkthrough.md) — Documentation of the premium design system.

---

## 🏗️ Detailed Project Structure (Clickable)

*Explore the project files directly!*

- 📁 [**CyberAttackPrediction**](CyberAttackPrediction/) (Main Project Folder)
  - 📁 [static](CyberAttackPrediction/static/) (Styles & Images)
    - 📄 [default.css](CyberAttackPrediction/static/default.css) (Colors and Layout)
  - 📁 [templates](CyberAttackPrediction/templates/) (The Webpages)
    - 📄 [base.html](CyberAttackPrediction/templates/base.html) (The Master Design Layout)
    - [index.html](CyberAttackPrediction/templates/index.html) (Home Page)
    - [project overview.html](CyberAttackPrediction/templates/project%20overview.html) (Project Overview Landing Page)
    - [documentation.html](CyberAttackPrediction/templates/documentation.html) (Technical Repository Explorer)
    - [Predict.html](CyberAttackPrediction/templates/Predict.html) (The Attack Upload & Analysis Page)
    - [UserLogin.html](CyberAttackPrediction/templates/UserLogin.html) (Modern Split-UI Login Page)
    - [UserScreen.html](CyberAttackPrediction/templates/UserScreen.html) (Results & Explanation Dashboard)
    - [HowItWorks.html](CyberAttackPrediction/templates/HowItWorks.html) (GenAI Human-Readable Explanations)
    - [Train.html](CyberAttackPrediction/templates/Train.html) (AI Model Training & Management Page)
  - 📁 [model](CyberAttackPrediction/model/) (The AI's Brain Files)
  - 📁 [Dataset](CyberAttackPrediction/Dataset/) (The Textbooks/Data)
  - 🐍 [**Main.py**](CyberAttackPrediction/Main.py) (Heart of the Project)
  - 🐍 [train_model.py](CyberAttackPrediction/train_model.py) (The AI Trainer script)
  - 📔 [ExtensionCyberAttack.ipynb](CyberAttackPrediction/ExtensionCyberAttack.ipynb) (Research & Extension)
  - 📔 [ProposeCyberAttack.ipynb](CyberAttackPrediction/ProposeCyberAttack.ipynb) (Initial Model Proposal)
  - 📖 [PROJECT_BOOK.md](CyberAttackPrediction/PROJECT_BOOK.md) (Full Technical Guide)
  - 📃 [SCREEENS.pdf](CyberAttackPrediction/SCREEENS.pdf) (Project Screenshots)
  - 📄 [DatasetLink.txt](CyberAttackPrediction/DatasetLink.txt) (Dataset mirror link)
  - ⚙️ [runFlask.bat](CyberAttackPrediction/runFlask.bat) (Internal launcher)
  - ⚙️ [runJupyter.bat](CyberAttackPrediction/runJupyter.bat) (Internal launcher)
  - 📄 [requirements.txt](CyberAttackPrediction/requirements.txt) (List of needed libraries)
- 📁 [**Software**](Software/) (Venv Helpers & NLTK Data)
  - ⚙️ [Pack Install.bat](Software/Pack%20Install.bat) (One-click legacy dependency installer)
  - 📄 [Requirements.txt](Software/Requirements.txt) (Dependency list)
  - 📁 [nltk](Software/nltk/) (Offline NLTK data)
  - 🐍 [python-3.11.9-amd64.exe](Software/python-3.11.9-amd64.exe) (Python 3.11 installer)
- 📁 [**backups**](backups/) (Original zip files & legacy installers)
- 📁 [**docs/**](docs/) (Documentation, Study Guides, & Manuals)
- 📁 [**Project materials**](Project%20materials/) (Graphics, Roadmaps, and Reference images)
- ⚙️ [**Start_WebApp_Venv.bat**](Start_WebApp_Venv.bat) (Quick launcher for Web App)
- ⚙️ [**Start_Jupyter_Venv.bat**](Start_Jupyter_Venv.bat) (Launcher for Jupyter Notebook research)
- 📜 [install_deps.ps1](install_deps.ps1) (Automated dependency installation script)
- 📝 [to do list.txt](to%20do%20list.txt) (Project task tracking - Old)

---

## 🏛️ Academic Institutional Details

- **Institution**: Roland Institute of Computer & Management Studies, Berhampur
- **Program**: Bachelor of Computer Applications (BCA) — Final Year
- **Session**: 2023–2026
- **Guide**: Mr. Rasmi Roy Badakumar

### 👥 The Development Team

- **Kumar Sreyan Pattanayak** (Roll: 23PBCA1355)
- **Ankita Pati** (Roll: 23PBCA1335)
- **Subhashree Pathy** (Roll: 23PBCA1386)
- **Tanmaya Ranjan Jena** (Roll: 23PBCA1391)

---
<p align="center">
  Built with ❤️ for Academic Excellence — 2026
</p>
