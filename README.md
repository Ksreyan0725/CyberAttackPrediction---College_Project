<!-- markdownlint-disable MD033 -->
<h1 align="center">
  <img src="CyberAttackPrediction/static/images/logo_with_bg.svg" alt="CyberShield Logo" width="32" vertical-align="middle"> Cyber Attack Prediction: From Traditional ML to Generative AI
</h1>

<p align="center">
  <img src="CyberAttackPrediction/static/images/favicon.svg" alt="CyberShield Favicon" width="128">
</p>

<h2 align="center">CyberShield AI</h2>

<p align="center">
  **Predicting network intrusions with precision. Explaining security with intelligence.**
</p>

![Python](https://img.shields.io/badge/Python-3.13.2-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-v3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-v1.8.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Status](https://img.shields.io/badge/Status-Stable--2026--Hardened-success?style=for-the-badge)

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
2. **Configure Secrets**: Create a `.env` file in the root directory (use `.env.example` as a template) to secure your admin credentials and Flask session keys.
3. **Setup Dependencies**: Run the [⚙️ Pack Install.bat](Software/Pack%20Install.bat) or `install_deps.ps1` to automatically prepare the high-performance environment.
4. **Unified Launch**: Run [🐍 launcher.py](launcher.py) to access the **Command Center**. Choose **Mode 1** for the Web Dashboard or **Mode 2** for Jupyter research.
5. **Active Session Guard**: Start scripts now feature **Venv Persistence**, ensuring the `.venv` environment remains active and isolated for high-performance operation.

> [!TIP]
> **Admin Dashboard Bypass**: Use Username `admin` and Password `admin` to immediately access the full features and Master Badge interface.

---

## 💎 Key Features

- **🧠 Stacking Ensemble AI** — Multi-model architecture (Random Forest, KNN, MLP) achieving **98%+ accuracy**.
- **🤖 GenAI Mitigation Insights** — Converts classification results into plain-English advice for security administrators.
- **![CyberShield Logo](CyberAttackPrediction/static/images/logo_with_bg.svg) Stable-2026 Hardening** — Integrated **Neural Firewall** (path traversal protection) and **Cryptographic Identity** (HMAC session tokens).
- **🔍 Explainable AI (SHAP)** — Visualizes *why* a network packet was flagged using Shapley Additive Explanations.
- **📂 In-Browser Repository Explorer** — Logged-in users can browse and read all project files directly in the app, protected by root-level sandboxing.

---

## 📊 Project Foundations

![Project Roadmap](CyberAttackPrediction/static/images/roadmap_HD.png)
*The systematic development lifecycle from data ingestion to Generative AI integration.*

![Five Pillars](CyberAttackPrediction/static/images/five_pillars_HD.png)
*Aligning with cybersecurity frameworks for comprehensive monitoring and defense.*

---

## 🛠️ Installation & Setup

1. **Clone the repository**:

```bash
git clone https://github.com/Ksreyan0725/CyberAttackPrediction---College_Project.git
cd CyberAttackPrediction---College_Project
```

1. **Setup Virtual Environment**:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

1. **Install Dependencies**:

```bash
pip install -r CyberAttackPrediction/requirements.txt
```

1. **Configure Environment**:
   Create a `.env` file in the root based on the following template:

```env
FLASK_SECRET_KEY=your_secure_hex_key
ADMIN_USER=admin
ADMIN_PASS=admin
ADMIN_HASH=pbkdf2:sha256:600000$...
```

1. **Run the Application**:
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
  - 🔐 [.env](.env) — Sensitive configuration & secrets
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

Built with ❤️ for Academic Excellence — 2026
