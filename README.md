# Neon by Ascertn (`tryneonai.com`)

> **Enterprise AI SEO, Website Builder & Omnichannel Visibility SaaS Platform**  
> Built strictly according to the Product Requirements Document (PRD) specifications with a high-contrast enterprise white daylight design system (inspired by Linear Light, Stripe, and Vercel).

---

## 🌟 Architecture Overview

Neon by Ascertn unifies four critical pillars under a single shared brain:
1. **AI Visual Website Builder** — Real-time block editing, responsive device preview (desktop, tablet, mobile), and 1-click standalone HTML and JSON site config export.
2. **Technical & Semantic AI SEO Auditor** — Live Google SERP snippet previews, real-time character & pixel-width meters, H1/H2 hierarchy inspector, Schema.org JSON-LD generator, and a **Live Cheerio Web Crawler** that audits any public URL.
3. **Omnichannel Campaign Studio** — High-velocity orchestration synchronizing landing pages, 100,000+ recipient parallel email batch sender simulation, and multi-channel social queues (LinkedIn, Instagram, Facebook).
4. **Live Visibility Score Engine (0–100)** — A real-time mathematical score engine reacting dynamically to every page audit, completed growth task, and active campaign.

---

## 📊 Live Visibility Score Formula

The platform dynamically calculates the **Live Visibility Score ($0 - 100$)** using the exact PRD formula:

$$\text{Visibility Score} = \min\left(99, \text{round}\left(0.88 \times \overline{\text{SEO}}_{\text{pages}} + 2 \times T_{\text{completed}} + 3 \times C_{\text{active}}\right)\right)$$

Where:
* $\overline{\text{SEO}}_{\text{pages}}$ is the mean technical and on-page SEO score across all workspace pages.
* $T_{\text{completed}}$ is the count of completed SEO and marketing growth tasks.
* $C_{\text{active}}$ is the number of active omnichannel campaigns.

Sub-score weight distribution:
* **Technical & On-Page SEO**: 40%
* **Content Freshness & Velocity**: 30%
* **Campaign Reach & Engagement**: 30%

---

## 🔍 Technical & Semantic SEO Auditor Rules

| Audit Rule | Optimal Threshold | Failure Warning | AI Auto-Fix Behavior |
| :--- | :--- | :--- | :--- |
| **Meta Title Length** | $45 - 60\text{ chars}$ ($\approx 400 - 560\text{px}$) | Warning if $<45$ or $>65\text{ chars}$ | Rewrites title to $52-60\text{ chars}$ with target keyword front-loaded. |
| **Meta Description** | $120 - 160\text{ chars}$ | Warning if $<120$ or $>165\text{ chars}$ | Generates high-CTR summary ($145-158\text{ chars}$) with clear value proposition. |
| **Semantic Word Count** | $\ge 1,150\text{ words}$ for B2B SERPs | Flags thin content ($<700\text{ words}$) | Expands section blocks and appends semantic H2 subheadings. |
| **Internal Link Depth** | $\ge 10\text{ contextual links}$ | Flags orphan or low-link pages ($<5$) | Injects contextual internal links from pillar pages. |
| **Structured Data** | Valid `Schema.org` JSON-LD | Missing or unvalidated schema | Auto-generates and injects `JSON-LD` block matching page type. |

---

## 🚀 Local Development & Hosting Guide

### Prerequisites
* **Node.js**: v18.0.0 or higher (v20+ recommended)
* **npm**: v9.0.0 or higher
* **Python**: v3.10 or higher (Python 3.14 supported)

---

### 1. Initial Setup

#### Clone & Install Frontend Dependencies
```bash
git clone <repo-url>
cd "Neon Project"
npm install
```

#### Setup Python Backend Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate       # On Linux / macOS
# .venv\Scripts\activate        # On Windows (cmd / PowerShell)

# Install backend dependencies
pip install -r neon-backend/requirements.txt greenlet
```

#### Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
> **Zero-Config Database**: By default, the backend runs on **Async SQLite** (`sqlite+aiosqlite:///./neon.db`) with automatic table creation and seed data on startup. No external database setup is required.  
> **Dual-Mode AI Engine**: If `GEMINI_API_KEY` is not provided, the system seamlessly uses deterministic high-fidelity AI fallbacks for 100% offline functionality. You can also connect your key via the in-app **"Configure AI Key"** modal.

---

### 2. Running Locally

#### Option A: Unified 1-Command Startup (Recommended)
Runs both the **FastAPI backend** (port `8000`) and the **Vite frontend** (port `5173`) concurrently:
```bash
npm run start
```
* **Client App**: [http://localhost:5173](http://localhost:5173) (Vite reverse-proxies `/api` to port `8000`)
* **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
* **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

#### Option B: Running Backend & Frontend in Separate Terminals

**Terminal 1 — FastAPI Backend (Port 8000):**
```bash
# Using npm script:
npm run server

# Or directly with Python / Uvicorn:
.venv/bin/python -m uvicorn main:app --app-dir neon-backend --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Vite Frontend (Port 5173):**
```bash
npm run dev
```

---

#### Option C: Production Docker Compose (PostgreSQL 16 + Redis 7 + FastAPI)
If you prefer running the backend in containers with PostgreSQL and Redis:
```bash
cd neon-backend
docker compose up -d --build
```

---

### 3. Verify Backend Status

Test that the backend is responding properly:

```bash
# Health Check
curl -s http://localhost:8000/api/v1/health

# Bootstrap Workspace State
curl -s http://localhost:8000/api/v1/workspace/bootstrap

# Test Live DOM Crawler
curl -X POST http://localhost:8000/api/v1/seo/audit-url \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

---

### 4. Build for Production
```bash
npm run build
```
Generates an optimized, tree-shaken static production bundle in `dist/`.

---

## 🛠️ FastAPI Backend Architecture & API Blueprint

The backend is built with **FastAPI**, **SQLAlchemy 2.0 (asyncio)**, **Pydantic v2**, and **HTTPX / BeautifulSoup4**.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Health check reporting service status, version, and active modules. |
| `GET` | `/api/v1/workspace/bootstrap` | Rehydrates workspace state (Brand Kit, Pages, Campaigns, Tasks, Metrics). |
| `PUT` | `/api/v1/brand-kit` | Updates centralized Brand Kit tokens (colors, fonts, tone of voice). |
| `PUT` | `/api/v1/pages/{page_id}` | Updates page sections, publish status, slug, and triggers SEO rescoring. |
| `PATCH` | `/api/v1/tasks/{task_id}` | Toggles growth task completion and updates real-time Visibility Score. |
| `POST` | `/api/v1/ask-neon` | AI-orchestrates landing page, campaign draft, and social post in 1 prompt. |
| `POST` | `/api/v1/seo/audit-url` | Live DOM crawler extracting metadata and evaluating 0–100 SEO health. |
| `POST` | `/api/v1/seo/auto-fix/{page_id}` | Generates optimized title, meta description, and injected JSON-LD schema. |
| `POST` | `/api/v1/seo/keyword-clusters` | Researches 4–8 clustered topic keywords with search intent and difficulty. |
| `POST` | `/api/v1/email/send-batch` | High-volume batch worker simulation (up to 100K+) with shard telemetry. |
| `GET` | `/api/v1/email/batch-status/{id}` | Polls real-time email dispatch status, sent counts, and deliverability. |

---

## 📱 Navigation & Deep Links

The application supports native URL hash routing and browser history navigation:
* `#/` or `#/marketing` — Public Marketing Website (`tryneonai.com`)
* `#/dashboard` or `#/workspace` — Growth & Visibility Command Center
* `#/seo` — AI SEO Assistant & Live Technical Web Crawler
* `#/pages` — No-Code Visual Website Builder with device preview & code export
* `#/view/:pageId` — Dedicated Live Full-Page Landing Page view with Brand Kit tokens & code export
* `#/campaigns` — Omnichannel Campaign Studio
* `#/email` — 100K+ Email Parallel Batch Sender & Deliverability Telemetry
* `#/social` — Multi-Channel Social Scheduler (LinkedIn, IG, FB)
* `#/brand` — Centralized Brand Kit
* `#/analytics` — Live Visibility Score Engine & Interactive Simulator

---

## 🛡️ License & Attributions
Built for enterprise scale by **Neon by Ascertn**. Designed according to enterprise daylight standards.
