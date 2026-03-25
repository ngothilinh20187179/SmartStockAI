# SmartStockAI: Intelligent Invoice Matching & Inventory Pipeline

## 🎯 Overview
**SmartStock AI** is an end-to-end automated pipeline engineered to eliminate the "data entry bottleneck" in retail and logistics management.

In traditional warehousing, manual invoice entry is a time-consuming process prone to human error. This project bridges that gap by transforming messy, unstructured paper invoices into actionable inventory insights. By integrating **AI-powered OCR** with a custom **Intelligent Matching Engine**, the system automates the transition from raw text to standardized master data.

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| 🖥️ **Frontend** | **Next.js, TanStack Query, Tailwind CSS, Shadcn/ui, Framer Motion** |
| 🐍 **Backend** | **Python, FastAPI, Pydantic, SQLModel (ORM), Alembic** |
| 📊 **Database** | **PostgreSQL** |
| ☁️ **Cloud Storage** | **AWS S3/ Supabase** |
| 🤖 **AI Orchestration** | **LangChain, Google Cloud Document AI, Gemini 1.5** |
| 🧠 **Algorithm** | **RapidFuzz, Keyword Scoring Logic** |
| 🔐 **Security** | **NextAuth.js, JWT (JSON Web Token)** |
| 🐳 **Infrastructure** | **Docker, Docker Compose, GitHub Actions (CI/CD)**|


## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SmartStockAI
```

### 2. Set up environment

```bash
cp .env.example .env
```

### 3. Start Database + Backend (Docker Compose)

```bash
docker-compose up -d
```
This will:
- start PostgreSQL (with healthcheck)
- run `alembic upgrade head`
- run `python backend/scripts/check_db.py` (DB connectivity check)
- run `python backend/scripts/seed.py` (seed demo users, idempotent)
- start FastAPI at `http://localhost:8000`

Test the sample API:
```bash
curl http://localhost:8000/api/users
```

#### (Optional) Run Backend locally (DB in Docker)
If you prefer running FastAPI on your machine while keeping Postgres in Docker:

```bash
docker-compose up -d db
cd backend
source venv/bin/activate
pip install -r requirements.txt
python scripts/check_db.py
python scripts/seed.py
uvicorn app.main:app --reload
```

### 4. Run Frontend

```bash
cd frontend 
npm install 
npm run dev
```

## 🚀 Live Demo

## 🏗️ Project Structure
SmartStockAI - A fullstack application built as a monorepo with separate frontend, backend and AI services.

```bash
SmartStockAI/
├── backend/                # Primary FastAPI application source
│   ├── app/                # Application core logic
│   │   ├── api/            # Endpoints
│   │   ├── core/           # Global configurations (Database, Security, Config)
│   │   ├── models/         # Database table definitions (SQLModel classes)
│   │   ├── schemas/        # Pydantic models for Data Validation (Request/Response)
│   │   ├── services/       # Business logic
│   │   └── main.py
│   ├── migrations/         # Database version control files (Alembic)
│   │   └── versions/
│   ├── alembic.ini
│   ├── scripts/         
│   │   ├── check_db.py      # DB connectivity check
│   │   └── seed.py          # Seed demo data
│   ├── Dockerfile
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js (TypeScript) - Modern Web Dashboard
│   ├── src/
│   │   ├── app/            # App Router (Pages, Layouts, Loading states)
│   │   ├── components/     # Reusable UI components (shadcn/ui, tailwind)
│   │   ├── lib/            # Utilities (API clients, formatting, helpers)
│   │   ├── hooks/          # Custom React hooks (Data fetching, Auth)
│   │   └── store/          # State management (Zustand or Redux)
│   ├── public/             # Static assets (Images, Icons, Fonts)
│   └── package.json        # Node.js dependencies & scripts
├── docker-compose.yml
├── .env
└── .gitignore
```