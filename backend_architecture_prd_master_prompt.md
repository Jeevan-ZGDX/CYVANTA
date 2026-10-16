# Backend Engineering PRD & Master AI Build Prompt
**Product Name:** Neon by Ascertn — Backend API, SEO Crawler & Omnichannel Queue Engine  
**Target Stack:** Python 3.11+, FastAPI, PostgreSQL (`asyncpg` + SQLAlchemy 2.0), Redis + Celery, Playwright + BeautifulSoup4, Google GenAI SDK (`gemini-2.5-flash`)  
**Purpose:** Provide a drop-in, production-grade backend service that replaces the in-memory state in `App.jsx` with persistent database storage, live headless-browser technical SEO crawling, real-time Visibility Score calculation, and parallel 100K+ email batch processing.

---

## Part 1: Copy-Paste Master Backend Engineering Prompt
*(Copy the block below into Cursor, Windsurf, Claude Code, or hand it to your backend engineering team to generate the complete backend microservice repository)*

```text
You are a Principal Backend Systems Architect and Staff Technical SEO Engineer. Build a complete, production-ready Python FastAPI backend (`neon-backend/`) that powers the "Neon by Ascertn" React frontend (`App.jsx`).

1. CORE TECH STACK & ARCHITECTURE:
- Framework: FastAPI (Python 3.11+) with full async/await support, CORS configured for Vite (`http://localhost:5173`) and production domains.
- Database: PostgreSQL with SQLAlchemy 2.0 (async) and Pydantic v2 schemas for strict validation. (Include an automatic SQLite fallback `sqlite+aiosqlite:///./neon.db` so the server runs zero-config out of the box).
- AI Engine: Google Gemini API (`google-genai` SDK using `gemini-2.5-flash`) with structured JSON outputs (`response_schema`) for deterministic SEO fixes, keyword clustering, and omnichannel campaign generation.
- Live SEO Crawler: Async HTTP/DOM crawler (`httpx` + `BeautifulSoup4`, with optional Playwright headless mode) that fetches any live URL, parses `<title>`, `<meta name="description">`, canonical URLs, `<h1>`–`<h6>` hierarchy, word count, internal/external links, and existing `application/ld+json` Schema.org blocks.
- High-Volume Background Workers: Celery + Redis (with FastAPI `BackgroundTasks` fallback) to simulate or execute parallel 100,000+ recipient email batch sending and asynchronous domain-wide SEO crawls.

2. DATABASE MODELS (`models.py`):
Create relational tables that map 1:1 to the state objects in `App.jsx`:
- `BrandKit`: `id`, `brand_name`, `domain`, `primary_color`, `secondary_color`, `heading_font`, `tone_of_voice`, `target_audience`, `updated_at`
- `Page`: `id`, `title`, `slug`, `status`, `views`, `seo_score`, `meta_title`, `meta_description`, `target_keyword`, `h1`, `h2s` (JSON array), `schema_type`, `canonical`, `internal_links`, `word_count`, `sections` (JSON array of builder blocks), `issues` (JSON array), `updated_at`
- `Campaign`: `id`, `name`, `status`, `channels` (JSON array), `emails_sent`, `open_rate`, `click_rate`, `seo_keywords_ranked`, `visibility_impact`, `updated_at`
- `TaskItem`: `id`, `title`, `due`, `type`, `done`
- `SocialPost`: `id`, `platform`, `day`, `status`, `content`, `likes_est`
- `EmailBlastJob`: `id`, `campaign_name`, `audience_size`, `subject_a`, `subject_b`, `preheader`, `body`, `status`, `progress`, `open_rate`

3. REQUIRED REST API ENDPOINTS (`routers/`):
Build and wire the following endpoints so `App.jsx` can hydrate and mutate all state:
- `GET /api/v1/workspace/bootstrap`: Returns the complete initial state (`pages`, `campaigns`, `tasks`, `brandKit`, `socialPosts`, `emailBlast`, and computed `visibilityMetrics`). Automatically seeds the database with the default `tryneonai.com` dataset if the database is empty.
- `POST /api/v1/ask-neon`: Accepts `{ prompt, brandKit }`. Calls Gemini with a structured JSON schema to simultaneously create and persist:
  1. A new SEO-optimized `Page` (with 3 responsive builder sections, 50-60 char Meta Title, 140-160 char Meta Description, and H1/H2 hierarchy).
  2. A new `Campaign` record linked to that page.
  3. A scheduled `SocialPost` draft.
  Returns the newly created objects plus the updated `visibilityMetrics`.
- `POST /api/v1/seo/audit-url`: Accepts `{ url, targetKeyword }`. Performs a real live HTTP GET + DOM parse of the target URL. Extracts actual meta tags, headings, word count, internal link count, and JSON-LD schema, runs the deterministic Neon SEO Scoring Engine (0–100), and returns a detailed audit report + list of specific technical issues.
- `POST /api/v1/seo/auto-fix/{page_id}`: Fetches the `Page` from Postgres, sends its current metadata and `target_keyword` to Gemini, rewrites `meta_title` (strictly 52–60 chars, primary keyword front-loaded), `meta_description` (strictly 145–158 chars), optimizes the `h1`, appends a semantic `h2`, generates valid `Schema.org` JSON-LD, clears the `issues` array, recalculates `seo_score` (94–99), saves to DB, and returns the updated `Page`.
- `POST /api/v1/seo/keyword-clusters`: Accepts `{ seedKeyword }`. Uses Gemini structured output to return 4–8 high-intent keyword clusters (`cluster`, `intent`, `volume`, `difficulty`, `recSlug`).
- `PUT /api/v1/pages/{page_id}`: Updates page sections, metadata, or status from the Visual Website Builder and recalculates its `seo_score` and `issues` in real time.
- `POST /api/v1/email/send-batch`: Accepts `{ campaignName, audienceSize, subjectA, subjectB, body }`. Starts an async background batch job that increments progress (`0 -> 100%`) across parallel worker shards and updates deliverability telemetry (`SPF/DKIM/DMARC`).
- `PATCH /api/v1/tasks/{task_id}`: Toggles a task's `done` boolean and returns the freshly recalculated `visibilityMetrics`.
- `PUT /api/v1/brand-kit`: Updates the centralized `BrandKit` tokens.

4. DETERMINISTIC SEO & VISIBILITY SCORING ENGINE (`services/scoring.py`):
Implement pure Python functions that calculate:
- Page SEO Score (0–100) based on exact character/pixel thresholds, keyword presence in Title/H1/Description, word count (>=1,150 words), internal links (>=10), and valid JSON-LD Schema.
- Workspace Visibility Score (0–100): `min(99, round(0.88 * avg_page_seo + 2 * completed_tasks + 3 * active_campaigns))`.
```

---

## Part 2: Detailed Backend Functions & Business Logic Specifications

### 1. Live Technical SEO DOM Crawler (`services/crawler.py`)
When a user audits an external URL or publishes a page, the backend executes `crawl_and_evaluate_url(url: str, target_keyword: str)`:

```python
# Core Crawler Logic Specification
async def crawl_and_evaluate_url(url: str, target_keyword: str) -> dict:
    """
    1. Fetches HTML via httpx.AsyncClient (timeout=10.0, follow_redirects=True)
    2. Parses DOM with BeautifulSoup(html, 'lxml')
    3. Extracts:
       - meta_title = soup.title.string
       - meta_description = soup.find('meta', attrs={'name': 'description'})['content']
       - canonical = soup.find('link', attrs={'rel': 'canonical'})['href']
       - h1_tags = [h.get_text(strip=True) for h in soup.find_all('h1')]
       - h2_tags = [h.get_text(strip=True) for h in soup.find_all('h2')]
       - json_ld_scripts = [s.string for s in soup.find_all('script', type='application/ld+json')]
       - body_words = len(soup.body.get_text(" ", strip=True).split())
       - internal_links = count of <a href> matching the same root domain
    4. Passes extracted telemetry into `calculate_page_seo_score()`
    """
```

### 2. Deterministic Page SEO Scoring Function (`services/scoring.py`)
Every time a `Page` is created, edited in the builder, or auto-fixed by AI, the backend runs this exact scoring function before saving to PostgreSQL:

$$\text{Page SEO Score} = B_{\text{base}} + S_{\text{title}} + S_{\text{desc}} + S_{\text{headings}} + S_{\text{content}} + S_{\text{links}} + S_{\text{schema}}$$

| Component | Max Points | Exact Backend Evaluation Rule | Issue Appended if Failed |
| :--- | :--- | :--- | :--- |
| **Meta Title ($S_{\text{title}}$)** | $25\text{ pts}$ | $15\text{ pts}$ if $45 \le \text{len} \le 60$; $+10\text{ pts}$ if `target_keyword.lower()` in `meta_title.lower()` | `"Meta Title length ({len} chars) is outside optimal 45–60 char (540px) window"` |
| **Meta Description ($S_{\text{desc}}$)** | $20\text{ pts}$ | $15\text{ pts}$ if $120 \le \text{len} \le 160$; $+5\text{ pts}$ if `target_keyword.lower()` in `meta_description.lower()` | `"Meta Description ({len} chars) should be between 120 and 160 chars"` |
| **Semantic Headings ($S_{\text{headings}}$)** | $15\text{ pts}$ | $10\text{ pts}$ if non-empty `H1`; $+5\text{ pts}$ if $\ge 2$ `H2` subheadings exist | `"Missing semantic H2 subheadings to structure topic entities"` |
| **Content Depth ($S_{\text{content}}$)** | $20\text{ pts}$ | $20\text{ pts}$ if `word_count >= 1150`; $10\text{ pts}$ if `700 <= word_count < 1150`; $4\text{ pts}$ if `< 700` | `"Word count ({word_count}) is below SERP top-3 average (1,150 words)"` |
| **Internal Links ($S_{\text{links}}$)** | $10\text{ pts}$ | $10\text{ pts}$ if `internal_links >= 10`; $5\text{ pts}$ if `5 <= internal_links < 10` | `"Low internal link count ({links} links) — add contextual links from pillar pages"` |
| **Schema.org JSON-LD ($S_{\text{schema}}$)** | $10\text{ pts}$ | $10\text{ pts}$ if valid `schema_type` (`WebPage`, `ProductCollection`, `SoftwareApplication`, `Organization`) | `"Missing valid Schema.org JSON-LD structured data"` |

---

## Part 3: Frontend-to-Backend Wiring Guide (`App.jsx` Integration)

Once your FastAPI backend is running on `http://localhost:8000`, connect your exported `App.jsx` by adding an API client helper at the top of `src/App.jsx` and replacing the local handlers:

### 1. Hydrate Workspace State on Mount (`useEffect`)
```javascript
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

useEffect(() => {
  async function bootstrapWorkspace() {
    try {
      const res = await fetch(`${API_BASE}/workspace/bootstrap`);
      if (!res.ok) return;
      const data = await res.json();
      setPages(data.pages);
      setCampaigns(data.campaigns);
      setTasks(data.tasks);
      setBrandKit(data.brandKit);
      setSocialPosts(data.socialPosts);
    } catch (err) {
      console.warn("Backend offline, using built-in seed state:", err);
    }
  }
  bootstrapWorkspace();
}, []);
```

### 2. Wire the 4 Primary Action Handlers in `App.jsx`
| Frontend Handler in `App.jsx` | Backend Endpoint to Call | Request Payload |
| :--- | :--- | :--- |
| `handleRunAskNeon(prompt)` | `POST /api/v1/ask-neon` | `{ prompt: promptToRun, brandKit }` |
| `handleAutoFixPageSeo(pageToFix)` | `POST /api/v1/seo/auto-fix/${pageToFix.id}` | `{ targetKeyword: pageToFix.targetKeyword }` |
| `handleGenerateKeywordClusters()` | `POST /api/v1/seo/keyword-clusters` | `{ seedKeyword: keywordSeed }` |
| `handleTriggerEmailBatch()` | `POST /api/v1/email/send-batch` | `emailBlast` state object |

---

## Part 4: Recommended Backend Folder Structure

```text
neon-backend/
├── main.py                     # FastAPI entry point, CORS middleware, lifespan DB seeding
├── config.py                   # Pydantic BaseSettings (.env loader for DATABASE_URL, GEMINI_API_KEY, REDIS_URL)
├── database.py                 # AsyncEngine, AsyncSessionLocal, declarative Base
├── models.py                   # SQLAlchemy 2.0 ORM tables (Page, Campaign, TaskItem, BrandKit, SocialPost)
├── schemas.py                  # Pydantic v2 Request/Response schemas matching App.jsx state
├── routers/
│   ├── workspace.py            # GET /workspace/bootstrap, PUT /brand-kit, PATCH /tasks/{id}
│   ├── ask_neon.py             # POST /ask-neon (Omnichannel Gemini generator)
│   ├── seo_engine.py           # POST /seo/audit-url, POST /seo/auto-fix/{id}, POST /seo/keyword-clusters
│   └── campaigns.py            # POST /email/send-batch, GET /email/batch-status/{job_id}
├── services/
│   ├── gemini_service.py       # Google GenAI SDK wrapper with structured JSON schemas & retry logic
│   ├── crawler.py              # Async httpx + BeautifulSoup4 + Playwright live URL SEO inspector
│   ├── scoring.py              # Deterministic Page SEO (0-100) & Visibility Score (0-100) calculator
│   └── email_worker.py         # Parallel 100K+ email batch dispatcher & deliverability telemetry
├── requirements.txt            # fastapi, uvicorn, sqlalchemy, aiosqlite, asyncpg, httpx, beautifulsoup4, google-genai
└── docker-compose.yml          # PostgreSQL 16 + Redis 7 + FastAPI service definition
```