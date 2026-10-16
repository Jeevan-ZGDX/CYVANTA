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

## 🚀 Quickstart

### Prerequisites
* **Node.js**: v18.0.0 or higher (v26+ supported)
* **npm**: v9.0.0 or higher

### 1. Installation
```bash
npm install
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
> **Note**: Neon includes a dual-mode AI engine. If no `GEMINI_API_KEY` is provided, it automatically utilizes deterministic high-fidelity intelligence, ensuring 100% offline functionality. You can also connect your key anytime via the in-app **"Configure AI"** modal.

### 3. Launch Development Environment
Run both the Express backend API and the Vite frontend concurrently:
```bash
npm start
```
* **Client**: [http://localhost:5173](http://localhost:5173)
* **Backend API**: [http://localhost:3001](http://localhost:3001)

### 4. Build for Production
```bash
npm run build
```
Generates an optimized, tree-shaken static production bundle in `dist/`.

---

## 🛠️ Production Backend API Blueprint

The Express server (`server/index.ts`) implements the PRD endpoints:

### `POST /api/v1/ask-neon`
Generates a complete campaign package (landing page, SEO metadata, 100K email drop, and social post) from a single prompt.
* **Payload**: `{ prompt: string, brandKit: object, apiKey?: string }`
* **Response**: Hydrated page, campaign, and social post records.

### `POST /api/v1/seo/audit-url`
Uses **Cheerio** to crawl any live URL, extract DOM metadata, evaluate against PRD SEO thresholds, and calculate the SEO score.
* **Payload**: `{ url: string }`
* **Response**: `{ success: true, targetUrl, status, seoScore, diagnostics: { title, metaDescription, allH1s, h2s, canonical, hasJsonLd, schemaType, internalLinks, wordCount, titlePixelEst, issues } }`

### `POST /api/v1/seo/auto-fix`
Runs Gemini structured optimization to fix meta titles, meta descriptions, H1s, and semantic H2s.
* **Payload**: `{ pageId: string, currentMetadata: object, targetKeyword: string, apiKey?: string }`

### `POST /api/v1/seo/keyword-clusters`
Returns 4–8 clustered topic clusters with search intent (Transactional, Commercial, Informational), volume, difficulty, and URL slug suggestions.
* **Payload**: `{ seedKeyword: string, apiKey?: string }`

### `POST /api/v1/campaigns/email-batch`
Dispatches parallel worker queues simulating 100,000+ recipient drops with live SPF, DKIM, and DMARC verification.
* **Payload**: `{ campaignName: string, audienceSize: number, subjectA: string, subjectB: string }`

### `GET /api/v1/health`
Health check endpoint reporting system uptime, platform version, and active modules.

---

## 📱 Navigation & Deep Links

The application supports native URL hash routing and browser history navigation:
* `#/` or `#/marketing` — Public Marketing Website (`tryneonai.com`)
* `#/dashboard` or `#/workspace` — Growth & Visibility Command Center
* `#/seo` — AI SEO Assistant & Live Technical Web Crawler
* `#/pages` — No-Code Visual Website Builder with device preview & code export
* `#/campaigns` — Omnichannel Campaign Studio
* `#/email` — 100K+ Email Parallel Batch Sender & Deliverability Telemetry
* `#/social` — Multi-Channel Social Scheduler (LinkedIn, IG, FB)
* `#/brand` — Centralized Brand Kit
* `#/analytics` — Live Visibility Score Engine & Interactive Simulator

---

## 🛡️ License & Attributions
Built for enterprise scale by **Neon by Ascertn**. Designed according to enterprise daylight standards.
