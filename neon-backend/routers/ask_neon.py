import time
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models
import schemas
from services.gemini_service import generate_ask_neon_campaign
from services.scoring import calculate_page_seo_score, calculate_visibility_metrics

router = APIRouter(tags=["Ask Neon Generator"])

@router.post("/ask-neon", response_model=schemas.AskNeonResponse)
async def ask_neon(payload: schemas.AskNeonRequest, db: AsyncSession = Depends(get_db)):
    """
    Simultaneously creates and persists:
    1. A new SEO-optimized Page with 3 responsive sections and Schema.org markup
    2. A synchronized Campaign record
    3. A scheduled SocialPost draft
    Returns the hydrated entities and updated Live Visibility Score metrics.
    """
    if not payload.prompt or not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    # Fetch default brand kit if not provided
    brand_kit = payload.brandKit or {}
    if not brand_kit:
        bk_res = await db.execute(select(models.BrandKit).where(models.BrandKit.id == "default"))
        bk_obj = bk_res.scalar_one_or_none()
        if bk_obj:
            brand_kit = {
                "brandName": bk_obj.brand_name,
                "domain": bk_obj.domain,
                "toneOfVoice": bk_obj.tone_of_voice
            }

    data = await generate_ask_neon_campaign(payload.prompt, brand_kit, payload.apiKey)

    # 1. Create Page
    new_page_id = f"page-{int(time.time() * 1000)}"
    clean_slug = data["slug"] if data["slug"].startswith("/") else f"/{data['slug']}"
    domain = brand_kit.get("domain", "tryneonai.com")

    sections = [
        {"id": f"{new_page_id}-s1", "type": "Hero", "heading": data["h1"], "subheading": data["subheading"]},
        {"id": f"{new_page_id}-s2", "type": "Features", "heading": "Engineered for Search Authority & Omnichannel Lift", "subheading": "Pre-configured with JSON-LD schema, responsive blocks, and 100K+ email sync."},
        {"id": f"{new_page_id}-s3", "type": "CTA", "heading": "Launch Your Campaign Today", "subheading": "Get started in minutes with full Brand Kit alignment."}
    ]

    h2s = ["Key Benefits & ROI", "How It Works in 3 Steps", "Trusted by 200+ Growth Teams"]
    seo_score, issues = calculate_page_seo_score(
        meta_title=data["metaTitle"],
        meta_description=data["metaDescription"],
        target_keyword=data["targetKeyword"],
        h1=data["h1"],
        h2s=h2s,
        word_count=1350,
        internal_links=12,
        schema_type="WebPage"
    )

    page = models.Page(
        id=new_page_id,
        title=data["pageTitle"],
        slug=clean_slug,
        status="Published",
        views="124 (Live)",
        seo_score=seo_score,
        meta_title=data["metaTitle"],
        meta_description=data["metaDescription"],
        target_keyword=data["targetKeyword"],
        h1=data["h1"],
        h2s=h2s,
        schema_type="WebPage",
        canonical=f"https://{domain}{clean_slug}",
        internal_links=12,
        word_count=1350,
        sections=sections,
        issues=issues
    )
    db.add(page)

    # 2. Create Campaign
    new_camp_id = f"camp-{int(time.time() * 1000)}"
    campaign = models.Campaign(
        id=new_camp_id,
        name=data["pageTitle"],
        status="Active",
        channels=["Website", "Email", "Social", "SEO"],
        emails_sent="100,000 (Ready)",
        open_rate="69.2% (Est)",
        click_rate="15.1% (Est)",
        seo_keywords_ranked=12,
        visibility_impact="+22% Lift"
    )
    db.add(campaign)

    # 3. Create SocialPost
    new_sp_id = f"sp-{int(time.time() * 1000)}"
    social_post = models.SocialPost(
        id=new_sp_id,
        platform="LinkedIn",
        day="Today · Auto-Scheduled",
        status="Scheduled",
        content=data["socialPost"],
        likes_est="310+"
    )
    db.add(social_post)

    await db.commit()
    await db.refresh(page)
    await db.refresh(campaign)
    await db.refresh(social_post)

    # Recalculate metrics
    p_res = await db.execute(select(models.Page))
    pages = p_res.scalars().all()
    t_res = await db.execute(select(models.TaskItem))
    tasks = t_res.scalars().all()
    c_res = await db.execute(select(models.Campaign))
    campaigns = c_res.scalars().all()

    metrics = calculate_visibility_metrics(pages, tasks, campaigns)

    return {
        "success": True,
        "data": data,
        "hydrated": {
            "page": schemas.PageSchema.from_orm(page),
            "campaign": schemas.CampaignSchema.from_orm(campaign),
            "socialPost": schemas.SocialPostSchema.from_orm(social_post)
        },
        "visibilityMetrics": metrics
    }
