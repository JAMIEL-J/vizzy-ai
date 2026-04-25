# 📊 Vizzy Analytics Platform

Vizzy is a **trust-first analytics engine** that transforms raw tabular data into high-signal conversational insights, KPIs, and domain-aware visualizations.

## 🚀 Live Prototype
**Backend:** [Link to Hugging Face Space] | **Frontend:** [Link to Vercel]

> **Recruiter Note:** To experience the system instantly without configuring API keys, please enable **"Demo Mode"** in the dashboard header and explore the **Sample Gallery**.

---

## 🛠️ Engineering Highlights

### 1. OLAP-First Architecture
Instead of traditional row-based processing, Vizzy utilizes **DuckDB** as an embedded OLAP engine.
- **Why:** Columnar storage allows for lightning-fast aggregations on millions of rows without the overhead of a full data warehouse.
- **Impact:** Complex NL-to-SQL queries that would take seconds in SQLite execute in milliseconds in DuckDB.

### 2. Hybrid "Demo" Mode
To ensure a frictionless showcase experience, I implemented a **Hybrid Data Engine**.
- **Live Path:** Full end-to-end flow: `Upload` $\rightarrow$ `DuckDB Ingestion` $\rightarrow$ `LLM Analysis` $\rightarrow$ `Dynamic Visualization`.
- **Demo Path:** A "Golden Path" architecture using pre-baked analytical results. This ensures 100% reliability during presentations and eliminates onboarding friction for recruiters.

### 3. Weighted Domain-Aware Grouping
To solve the "Semantic Drift" problem (where related charts are scattered), I built a **Weighted Scoring Engine** for chart classification.
- **Logic:** `Score = (TitleMatch * 2.5) + (DimMatch * 2.0) + (TypeMatch * 1.5) + (MetricMatch * 1.0)`
- **Result:** Charts are automatically grouped into logical business sections (e.g., "Revenue Analysis", "Churn Drivers") based on the data's semantic context, not just hard-coded keywords.

### 4. Production-Ready Pipeline
- **Backend:** FastAPI + SQLModel + Docker.
- **Frontend:** React + TypeScript + Vite + Tailwind.
- **Deployment:** Containerized via Docker and hosted on Hugging Face Spaces (Backend) and Vercel (Frontend).

---

## 📦 Tech Stack

- **Backend:** Python, FastAPI, SQLModel, DuckDB, Groq LLM (Llama 3.3).
- **Frontend:** React, TypeScript, Chart.js, Tailwind CSS.
- **DevOps:** Docker, GitHub Actions, Hugging Face Spaces, Vercel.

---

## ⚙️ Local Setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Fill in your GROQ_API_KEY
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📈 System Architecture
- **API Layer:** Handles authentication, rate limiting, and request validation.
- **Service Layer:** Orchestrates the NL-to-SQL pipeline and LLM-assisted narrative generation.
- **Storage Layer:** Hybrid approach using SQLModel (Metadata/Users) and DuckDB (Analytical Data).
