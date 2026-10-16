from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models
import schemas
from services.scoring import calculate_visibility_metrics, calculate_page_seo_score

router = APIRouter(tags=["Workspace"])

INITIAL_PAGES_SEED = [
    {
        "id": "page-1",
        "title": "Holiday Gifting Page",
        "slug": "/holiday-gifting-corporate",
        "status": "Published",
        "views": "1,204",
        "seo_score": 92,
        "meta_title": "Corporate Holiday Gifting 2026 | Curated Luxury Boxes — Neon",
        "meta_description": "Delight clients and remote teams with custom-branded corporate holiday gift boxes. Instant global shipping, bulk discounts, and automated gift tracking.",
        "target_keyword": "corporate holiday gifting",
        "h1": "Unforgettable Corporate Holiday Gifting, Automated at Scale",
        "h2s": ["Curated Gift Collections", "Seamless Global Delivery", "Custom Brand Packaging"],
        "schema_type": "ProductCollection",
        "canonical": "https://tryneonai.com/holiday-gifting-corporate",
        "internal_links": 14,
        "word_count": 1420,
        "sections": [
            {"id": "s1", "type": "Hero", "heading": "Unforgettable Corporate Holiday Gifting, Automated at Scale", "subheading": "Send curated luxury boxes to 50 or 50,000 recipients in clicks. Full brand customization and live tracking."},
            {"id": "s2", "type": "Features", "heading": "Why Growth Teams Choose Our Gifting Studio", "subheading": "Zero spreadsheets, automated address collection, and instant budget controls."},
            {"id": "s3", "type": "CTA", "heading": "Ready to Launch Your Q4 Gifting Campaign?", "subheading": "Lock in early-bird inventory and custom packaging in under 5 minutes."}
        ],
        "issues": []
    },
    {
        "id": "page-2",
        "title": "Corporate Rewards",
        "slug": "/corporate-rewards-platform",
        "status": "Published",
        "views": "876",
        "seo_score": 78,
        "meta_title": "Corporate Rewards & Employee Recognition",
        "meta_description": "Automate employee milestones and B2B pipeline incentives with instant digital and physical rewards.",
        "target_keyword": "B2B corporate rewards platform",
        "h1": "Modern Corporate Rewards That Drive Pipeline & Retention",
        "h2s": ["Automated Milestone Triggers", "CRM & HRIS Integrations"],
        "schema_type": "SoftwareApplication",
        "canonical": "https://tryneonai.com/corporate-rewards-platform",
        "internal_links": 5,
        "word_count": 680,
        "sections": [
            {"id": "s2-1", "type": "Hero", "heading": "Modern Corporate Rewards That Drive Pipeline & Retention", "subheading": "Reward prospects for demo attendance and celebrate team milestones automatically."},
            {"id": "s2-2", "type": "Features", "heading": "Native CRM & Slack Workflows", "subheading": "Trigger gifts directly from HubSpot, Salesforce, or Slack."}
        ],
        "issues": [
            "Meta Title is under 45 characters (missing primary keyword modifier)",
            "Word count (680) is below SERP top-3 average (1,150 words)"
        ]
    },
    {
        "id": "page-3",
        "title": "Summer Promo",
        "slug": "/summer-promo-drop",
        "status": "Published",
        "views": "310",
        "seo_score": 68,
        "meta_title": "Summer Flash Sale — VIP Access",
        "meta_description": "Shop our limited seasonal drop with exclusive VIP discounts on brand merch.",
        "target_keyword": "summer promotional gifts",
        "h1": "Exclusive VIP Summer Merch Drop",
        "h2s": ["Featured Items"],
        "schema_type": "None",
        "canonical": "https://tryneonai.com/summer-promo-drop",
        "internal_links": 2,
        "word_count": 420,
        "sections": [
            {"id": "s3-1", "type": "Hero", "heading": "Exclusive VIP Summer Merch Drop", "subheading": "Premium branded apparel and summer swag curated for your top clients."}
        ],
        "issues": [
            "Missing valid Schema.org JSON-LD structured data",
            "Meta Description is under-optimized (82 chars vs recommended 140–160)",
            "Low internal link count (2 links) — add contextual links from high-authority pages"
        ]
    }
]

INITIAL_CAMPAIGNS_SEED = [
    {
        "id": "camp-1",
        "name": "Q4 VIP Gifting Drop",
        "status": "Active",
        "channels": ["Website", "Email", "Social", "SEO"],
        "emails_sent": "115,000",
        "open_rate": "68.4%",
        "click_rate": "14.2%",
        "seo_keywords_ranked": 14,
        "visibility_impact": "+28% Lift"
    },
    {
        "id": "camp-2",
        "name": "Employee Rewards Rollout",
        "status": "Active",
        "channels": ["Website", "Email", "LinkedIn"],
        "emails_sent": "42,000",
        "open_rate": "72.1%",
        "click_rate": "18.6%",
        "seo_keywords_ranked": 8,
        "visibility_impact": "+16% Lift"
    },
    {
        "id": "camp-3",
        "name": "Summer Flash Drop",
        "status": "Draft",
        "channels": ["Email", "Instagram"],
        "emails_sent": "0",
        "open_rate": "—",
        "click_rate": "—",
        "seo_keywords_ranked": 3,
        "visibility_impact": "Pending"
    }
]

INITIAL_TASKS_SEED = [
    {"id": "task-1", "title": "Optimize Thin Content on Summer Promo LP (420 -> 1,150 words)", "due": "Today", "type": "SEO", "done": False},
    {"id": "task-2", "title": "Front-load 'B2B Corporate Rewards' keyword on Page 2 title tag", "due": "Today", "type": "SEO", "done": False},
    {"id": "task-3", "title": "Inject ProductCollection JSON-LD schema to Holiday Gifting LP", "due": "Tomorrow", "type": "Technical", "done": True},
    {"id": "task-4", "title": "Schedule 3 LinkedIn updates for Q4 gifting launch", "due": "Tomorrow", "type": "Social", "done": True}
]

INITIAL_SOCIAL_SEED = [
    {"id": "sp-1", "platform": "LinkedIn", "day": "Tomorrow · 9:00 AM", "status": "Scheduled", "content": "Why stitch together 6 tools when your website, SEO, email, and social can share one brain? Meet Neon by Ascertn — built for growth teams. #MarTech #SEO #Growth", "likes_est": "240+"},
    {"id": "sp-2", "platform": "Instagram", "day": "Friday · 5:00 PM", "status": "Scheduled", "content": "Unbox Q4 pipeline growth ✨ See how our Holiday Gifting template converts 3.4x higher out of the box.", "likes_est": "410+"},
    {"id": "sp-3", "platform": "Facebook", "day": "Saturday · 11:30 AM", "status": "Draft", "content": "Our Live Visibility Score just hit 82! Here are the exact 3 technical SEO fixes our AI executed automatically today.", "likes_est": "130+"}
]

async def seed_database_if_empty(db: AsyncSession):
    # Check BrandKit
    res = await db.execute(select(models.BrandKit).where(models.BrandKit.id == "default"))
    bk = res.scalar_one_or_none()
    if not bk:
        bk = models.BrandKit(id="default")
        db.add(bk)

    # Check Pages
    p_res = await db.execute(select(models.Page))
    existing_pages = p_res.scalars().all()
    if not existing_pages:
        for p_data in INITIAL_PAGES_SEED:
            page = models.Page(**p_data)
            db.add(page)

    # Check Campaigns
    c_res = await db.execute(select(models.Campaign))
    existing_c = c_res.scalars().all()
    if not existing_c:
        for c_data in INITIAL_CAMPAIGNS_SEED:
            camp = models.Campaign(**c_data)
            db.add(camp)

    # Check Tasks
    t_res = await db.execute(select(models.TaskItem))
    existing_t = t_res.scalars().all()
    if not existing_t:
        for t_data in INITIAL_TASKS_SEED:
            task = models.TaskItem(**t_data)
            db.add(task)

    # Check Social
    s_res = await db.execute(select(models.SocialPost))
    existing_s = s_res.scalars().all()
    if not existing_s:
        for s_data in INITIAL_SOCIAL_SEED:
            sp = models.SocialPost(**s_data)
            db.add(sp)

    await db.commit()

@router.get("/workspace/bootstrap", response_model=schemas.WorkspaceBootstrapResponse)
async def bootstrap_workspace(db: AsyncSession = Depends(get_db)):
    """
    Hydrates the complete Neon workspace state for the frontend.
    Auto-seeds SQLite/Postgres with seed data if the database is fresh.
    """
    await seed_database_if_empty(db)

    # Fetch all records
    p_res = await db.execute(select(models.Page).order_by(models.Page.updated_at.desc()))
    pages = p_res.scalars().all()

    c_res = await db.execute(select(models.Campaign).order_by(models.Campaign.updated_at.desc()))
    campaigns = c_res.scalars().all()

    t_res = await db.execute(select(models.TaskItem))
    tasks = t_res.scalars().all()

    bk_res = await db.execute(select(models.BrandKit).where(models.BrandKit.id == "default"))
    brand_kit = bk_res.scalar_one()

    sp_res = await db.execute(select(models.SocialPost))
    social_posts = sp_res.scalars().all()

    # Get email blast default state
    email_blast = schemas.EmailBlastSchema(
        campaignName="Q4 Holiday VIP Access Blast",
        audienceSize=115000,
        subjectA="Skip the Q4 gifting rush — your custom portal is ready ✨",
        subjectB="How 200+ growth teams automate holiday client gifting",
        preheader="Launch branded gift boxes in 60 seconds with Neon AI.",
        body="Hi {{first_name}},\n\nWith Q4 accelerating, your team shouldn’t be managing spreadsheets and shipping labels.\n\nClaim your complimentary sample kit below.",
        isSending=False,
        progress=100,
        lastOpenRate="68.4%"
    )

    metrics = calculate_visibility_metrics(pages, tasks, campaigns)

    return {
        "pages": pages,
        "campaigns": campaigns,
        "tasks": tasks,
        "brandKit": brand_kit,
        "socialPosts": social_posts,
        "emailBlast": email_blast,
        "visibilityMetrics": metrics
    }

@router.put("/brand-kit", response_model=schemas.BrandKitSchema)
async def update_brand_kit(payload: schemas.BrandKitUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates the centralized BrandKit design tokens.
    """
    res = await db.execute(select(models.BrandKit).where(models.BrandKit.id == "default"))
    bk = res.scalar_one_or_none()
    if not bk:
        bk = models.BrandKit(id="default")
        db.add(bk)

    for field, val in payload.dict(exclude_unset=True).items():
        if val is not None:
            # Map camelCase to snake_case if needed
            snake_key = {
                "brandName": "brand_name",
                "primaryColor": "primary_color",
                "secondaryColor": "secondary_color",
                "headingFont": "heading_font",
                "toneOfVoice": "tone_of_voice",
                "targetAudience": "target_audience"
            }.get(field, field)
            setattr(bk, snake_key, val)

    await db.commit()
    await db.refresh(bk)
    return bk

@router.patch("/tasks/{task_id}")
async def toggle_task(task_id: str, payload: Optional[schemas.TaskToggleRequest] = None, db: AsyncSession = Depends(get_db)):
    """
    Toggles a growth task done status and recalculates VisibilityMetrics in real time.
    """
    res = await db.execute(select(models.TaskItem).where(models.TaskItem.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload and payload.done is not None:
        task.done = payload.done
    else:
        task.done = not task.done

    await db.commit()
    await db.refresh(task)

    # Recalculate metrics
    p_res = await db.execute(select(models.Page))
    pages = p_res.scalars().all()
    t_res = await db.execute(select(models.TaskItem))
    tasks = t_res.scalars().all()
    c_res = await db.execute(select(models.Campaign))
    campaigns = c_res.scalars().all()

    metrics = calculate_visibility_metrics(pages, tasks, campaigns)
    return {"task": task, "visibilityMetrics": metrics}

@router.put("/pages/{page_id}", response_model=schemas.PageSchema)
async def update_page(page_id: str, payload: schemas.PageUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates page sections, metadata, or status from the visual builder,
    recalculating on-page SEO score and issues in real time.
    """
    res = await db.execute(select(models.Page).where(models.Page.id == page_id))
    page = res.scalar_one_or_none()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    if payload.title is not None:
        page.title = payload.title
    if payload.slug is not None:
        page.slug = payload.slug
    if payload.status is not None:
        page.status = payload.status
    if payload.metaTitle is not None:
        page.meta_title = payload.metaTitle
    if payload.metaDescription is not None:
        page.meta_description = payload.metaDescription
    if payload.targetKeyword is not None:
        page.target_keyword = payload.targetKeyword
    if payload.h1 is not None:
        page.h1 = payload.h1
    if payload.h2s is not None:
        page.h2s = payload.h2s
    if payload.schemaType is not None:
        page.schema_type = payload.schemaType
    if payload.sections is not None:
        page.sections = [s.dict() for s in payload.sections]

    # Recalculate SEO score
    score, issues = calculate_page_seo_score(
        meta_title=page.meta_title,
        meta_description=page.meta_description,
        target_keyword=page.target_keyword,
        h1=page.h1,
        h2s=page.h2s or [],
        word_count=page.word_count,
        internal_links=page.internal_links,
        schema_type=page.schema_type
    )
    page.seo_score = score
    page.issues = issues

    await db.commit()
    await db.refresh(page)
    return page
