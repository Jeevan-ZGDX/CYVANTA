# Product Requirements Document (PRD) & Master Build Prompt
**Product Name:** Neon by Ascertn (`tryneonai.com`)  
**Product Category:** Enterprise AI SEO, Website Builder & Omnichannel Visibility SaaS  
**Design System:** High-Contrast Professional Enterprise White Theme  

---

## Part 1: Copy-Paste Master AI Engineering Prompt
*(Copy the block below to instruct an AI coding agent or engineering team to build or extend the full-stack production repository)*

```text
You are a Principal Full-Stack Architect and Staff SEO Systems Engineer. Build a production-ready, enterprise-grade SaaS platform called "Neon by Ascertn" (modeled after tryneonai.com) that unifies an AI Website Builder, an Omnichannel Campaign Studio (100K+ email + social), a Technical & Semantic AI SEO Auditor, and a real-time Visibility Score Engine (0–100).

1. DESIGN & UI SYSTEM (STRICT PROFESSIONAL WHITE ENTERPRISE THEME):
- Aesthetic: Clean, editorial enterprise daylight design (inspired by Linear Light, Stripe, and Vercel). Zero dark/neon gradients.
- Surfaces: Crisp Alabaster White (#FFFFFF) primary cards, Soft Slate (#F8FAFC / slate-50) secondary containers, and subtle hairline borders (#E2E8F0 / slate-200).
- Typography & CTAs: Deep Slate Charcoal (#0F172A / slate-900) for primary headings and primary action buttons; Muted Slate (#475569 / slate-600) for body copy; Enterprise Emerald (#059669 / emerald-600) for positive SEO telemetry, badges, and live score indicators.

2. APPLICATION ARCHITECTURE (DUAL-MODE SPA / SSR):
The platform must seamlessly support two interconnected modes sharing real-time state:
- Mode A: Public Marketing Website (`/`):
  - Sticky enterprise white header with "Log In / Live Workspace" and "Book Demo" modal trigger.
  - Hero Section ("Be Seen Everywhere You Matter") featuring an interactive browser frame (`tryneonai.com/dashboard`) displaying live Neon CMS telemetry: Visibility Score (82/100), KPI counters (Pages: 24, Campaigns: 12, Opens: 68%, SEO: Good), Top Pages list, interactive Upcoming Tasks checklist, and a working "Ask Neon" AI prompt bar.
  - Social Proof Bar (200+ Growth teams, 4–6 Weeks to go live, 100K+ Emails per campaign) + Module Pills.
  - "01 · Website", "02 · Campaigns", "03 · Visibility" feature pillars with direct deep-links into the workspace.
  - Filterable Templates Gallery (All, Ecommerce, Agencies, B2B, Campaigns, Hospitality) where clicking "Use Template" instantiates the page inside the visual builder.
  - Interactive 5-Tab "Power of AI" showcase (Website, Email, Social, SEO, Report) + 6-card capability grid + Enterprise Pricing Card + 6-question FAQ accordion.

- Mode B: Authenticated SaaS Workspace (`/dashboard`):
  - Persistent Left Sidebar (Neon CMS) with live Visibility Score gauge + Top "Ask Neon" AI Command Bar.
  - Module 1: Growth & Visibility Command Center (KPIs, Top Pages & Live SEO Scores, Actionable Growth Queue).
  - Module 2: Advanced AI SEO Assistant & Technical Auditor:
    - Page selector dropdown, Live Google SERP Snippet preview, real-time character & pixel-width validation for Meta Titles (50–60 chars / ~540px) and Meta Descriptions (140–160 chars).
    - H1/H2 semantic hierarchy inspector, word count & internal link telemetry, automated issue detection, and 1-Click "Auto-Optimize with Neon AI".
    - Auto-generated, copyable Schema.org JSON-LD structured data (`WebPage`, `ProductCollection`, `SoftwareApplication`, `Organization`).
    - AI Keyword Cluster & Programmatic SEO Researcher (generates search intent, monthly volume, KD score, target slug, and 1-click page creation).
  - Module 3: No-Code Visual Website Builder (editable section blocks on the left, live responsive brand-styled preview canvas on the right).
  - Module 4: Omnichannel Campaign Studio (unified campaign cards tracking email, social, and SEO keyword lift).
  - Module 5: Email at Scale (100K+ parallel batch sender simulation, A/B subject line testing, DKIM/SPF/DMARC telemetry).
  - Module 6: Multi-Channel Social Scheduler (LinkedIn, Instagram, Facebook queue with AI post generation).
  - Module 7: Centralized Brand Kit (Brand name, custom domain, primary color tokens, AI tone-of-voice guardrails).
  - Module 8: Live Visibility Score Breakdown (weighted calculation across Technical SEO 40%, Content Velocity 30%, Campaign Engagement 30%).

3. AI INTEGRATION:
- Wire all generative actions ("Ask Neon" omnichannel generator, "1-Click Auto-Optimize SEO", and "AI Keyword Cluster Researcher") to the Google Gemini API (`gemini-3-flash-preview`) using structured JSON schemas (`responseSchema`) and exponential backoff retry logic, with deterministic offline fallbacks so the UI never fails.
```

---

## Part 2: Detailed Functional Requirements & Scoring Formulas

### 1. The Live Visibility Score Algorithm ($0 - 100$)
The platform's signature metric is the **Visibility Score**, which updates dynamically whenever a user optimizes a page, completes a task, or launches a campaign.

$$\text{Visibility Score} = \min\left(99, \text{round}\left(0.88 \times \overline{\text{SEO}}_{\text{pages}} + 2 \times T_{\text{completed}} + 3 \times C_{\text{active}}\right)\right)$$

Where:
* $\overline{\text{SEO}}_{\text{pages}}$ is the mean technical and on-page SEO score across all workspace pages.
* $T_{\text{completed}}$ is the count of completed SEO and marketing tasks.
* $C_{\text{active}}$ is the number of active omnichannel campaigns.

---

### 2. Technical & Semantic SEO Auditor Specifications
Every page in the workspace must be evaluated against the following rules:

| Audit Rule | Optimal Threshold | Failure Warning | AI Auto-Fix Behavior |
| :--- | :--- | :--- | :--- |
| **Meta Title Length** | $45 - 60\text{ chars}$ ($\approx 400 - 560\text{px}$) | Triggers warning if $<45$ or $>65\text{ chars}$ | Rewrites title to $52-60\text{ chars}$ with primary keyword front-loaded. |
| **Meta Description** | $120 - 160\text{ chars}$ | Triggers warning if $<120$ or $>165\text{ chars}$ | Generates high-CTR summary ($145-158\text{ chars}$) with clear value proposition. |
| **Semantic Word Count** | $\ge 1,150\text{ words}$ for B2B SERPs | Flags thin content ($<700\text{ words}$) | Expands section blocks and appends semantic H2 subheadings. |
| **Internal Link Depth** | $\ge 10\text{ contextual links}$ | Flags orphan or low-link pages ($<5\text{ links}$) | Injects contextual internal links from high-authority pillar pages. |
| **Structured Data** | Valid `Schema.org` JSON-LD | Missing or unvalidated schema | Auto-generates and injects `JSON-LD` block matching page type. |

---

### 3. Production Backend API Blueprint (For Full-Stack Scaling)
When connecting the React frontend (`App.jsx`) to a persistent backend (Next.js API Routes or Python FastAPI + PostgreSQL), implement these core endpoints:

* `POST /api/v1/ask-neon` — Accepts `{ prompt, brandKit }`, invokes Gemini structured output, creates a new Page, Campaign, and Social Draft in PostgreSQL, and returns the hydrated payload.
* `POST /api/v1/seo/audit-url` — Uses Playwright/Cheerio to crawl any live URL, extract DOM metadata (`<title>`, `<meta name="description">`, `<h1>`–`<h6>`, canonicals, JSON-LD, internal links), and compute the on-page SEO score.
* `POST /api/v1/seo/auto-fix` — Accepts `{ pageId, currentMetadata, targetKeyword }`, runs the LLM optimization prompt, and patches the page record.
* `POST /api/v1/seo/keyword-clusters` — Accepts `{ seedKeyword }`, queries SERP/keyword intelligence + Gemini clustering, and returns 4–10 structured topic clusters with search intent and URL slug recommendations.
* `POST /api/v1/campaigns/email-batch` — Queues parallel batch email jobs via Redis/Celery (or AWS SES / Resend) for $100,000+$ recipient lists.