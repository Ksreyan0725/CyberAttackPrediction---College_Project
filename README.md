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
  <img src="https://img.shields.io/badge/Python-3.13.2-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-v3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Scikit--Learn-v1.8.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Status-Hardened--2026-success?style=for-the-badge" alt="Status">
</p>

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

## 🌟 Executive Summary

**CyberShield AI** is a final-year Bachelor of Computer Applications (BCA) project that bridges the gap between traditional network security and modern Artificial Intelligence. By analyzing network traffic patterns using the industry-standard **NSL-KDD dataset**, the system classifies attacks into four primary families (DoS, Probe, R2L, U2R) and provides human-readable mitigation strategies via a simulated Generative AI engine.

---

## 🚀 Academic Quick Launch (Examiner Ready)

This project includes all necessary software. Follow these **3 simple steps** to launch the application for your viva:

1. **Install Python**: Open the [📁 Software/](Software/) folder and run **[🐍 python-3.13.12-amd64.exe](Software/python-3.13.12-amd64.exe)**.
2. **Setup Dependencies**: Run the [⚙️ Pack Install.bat](Software/Pack%20Install.bat) or `install_deps.ps1` to automatically prepare the high-performance environment.
3. **Unified Launch**: Run [🐍 launcher.py](launcher.py) to access the **Command Center**. Choose **Mode 1** for the Web Dashboard or **Mode 2** for Jupyter research.
4. **Active Session Guard**: Start scripts now feature **Venv Persistence**, ensuring the `.venv` environment remains active and isolated for high-performance operation.

> [!TIP]
> **Admin Dashboard Bypass**: Use Username `admin` and Password `admin` to immediately access the full features and Master Badge interface.

---

## 💎 Key Features

- **🧠 Stacking Ensemble AI** — Multi-model architecture (Random Forest, KNN, MLP) achieving **98%+ accuracy**.
- **🤖 GenAI Mitigation Insights** — Converts classification results into plain-English advice for security administrators.
- **🔍 Explainable AI (SHAP)** — Visualizes *why* a network packet was flagged using Shapley Additive Explanations.
- **🛡️ CSRF Cyber-Hardening** — Global token protection and secure header enforcement across all endpoints.
- **💎 Liquid Glass UI** — Glassmorphism design with 80px Gaussian blur and smooth staggered animations.
- **📂 In-Browser Repository Explorer** — Logged-in users can browse and read all project files directly in the app.

---

## 📊 Project Foundations

<p align="center">
  <img src="CyberAttackPrediction/static/images/roadmap_HD.png" alt="Project Roadmap" width="85%">
  <br><i>The systematic development lifecycle from data ingestion to Generative AI integration.</i>
</p>

<p align="center">
  <img src="CyberAttackPrediction/static/images/five_pillars_HD.png" alt="Five Pillars" width="85%">
  <br><i>Aligning with cybersecurity frameworks for comprehensive monitoring and defense.</i>
</p>

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

## 🏗️ Project Structure

- 📁 [**CyberAttackPrediction/**](CyberAttackPrediction/) — Main project folder
  - 📁 [static/](CyberAttackPrediction/static/) — Styles, JS & images
  - 📁 [templates/](CyberAttackPrediction/templates/) — HTML pages
  - 📁 [model/](CyberAttackPrediction/model/) — Saved AI model files
  - 📁 [Dataset/](CyberAttackPrediction/Dataset/) — All CSV training & test data
  - 📁 [scripts/](CyberAttackPrediction/scripts/) — Internal maintenance utilities
  - 🐍 **[Main.py](CyberAttackPrediction/Main.py)** — Flask backend (heart of the project)
  - 🐍 [train_model.py](CyberAttackPrediction/train_model.py) — AI trainer script
  - 📔 [ExtensionCyberAttack.ipynb](CyberAttackPrediction/ExtensionCyberAttack.ipynb) — Research notebook (Phase 2)
  - 📔 [ProposeCyberAttack.ipynb](CyberAttackPrediction/ProposeCyberAttack.ipynb) — Research notebook (Phase 1)
  - 📄 [requirements.txt](CyberAttackPrediction/requirements.txt) — Python dependencies
  - 📄 [users.json](CyberAttackPrediction/users.json) — User registry

- 📁 [**docs/**](docs/) — Unified documentation hub
  - 📖 [PROJECT_BOOK.md](docs/PROJECT_BOOK.md) — Definitive technical guide
  - 📘 [PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) — Comprehensive reference & viva prep
  - 📜 [TECHNICAL_WORKFLOW.md](docs/TECHNICAL_WORKFLOW.md) — System logic & architecture
  - 📗 [BeReady.md](docs/BeReady.md) — Student study handbook
  - 📋 [GUIDE_BOOK.md](docs/GUIDE_BOOK.md) — Quick-start & run instructions
  - 🔍 [DATASET_AUDIT.md](docs/DATASET_AUDIT.md) — Dataset folder structure explained

- 📁 [Software/](Software/) — Installers & venv helpers
- 📁 [backups/](backups/) — Original zips & legacy files
- 📁 [Project%20materials/](Project%20materials/) — Graphics & reference images

- 🐍 [launcher.py](launcher.py) — Unified command center
- ⚙️ [Start_WebApp_Venv.bat](Start_WebApp_Venv.bat) — Web app launcher
- ⚙️ [Start_Jupyter_Venv.bat](Start_Jupyter_Venv.bat) — Jupyter launcher
- 📜 [install_deps.ps1](install_deps.ps1) — Automated dependency installer
- 📝 [to%20do%20list.txt](to%20do%20list.txt) — Task tracking archive

<p align="center">
  Built with ❤️ for Academic Excellence — 2026
</p>
