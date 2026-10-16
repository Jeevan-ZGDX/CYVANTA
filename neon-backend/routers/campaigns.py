from typing import List, Dict, Any
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models
import schemas
from services.email_worker import initialize_batch_job, run_email_batch_job, EMAIL_JOBS_CACHE

router = APIRouter(tags=["Campaigns & Email"])

@router.get("/campaigns", response_model=List[schemas.CampaignSchema])
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    """
    Returns all active and scheduled omnichannel campaigns.
    """
    res = await db.execute(select(models.Campaign).order_by(models.Campaign.updated_at.desc()))
    return res.scalars().all()

@router.post("/email/send-batch")
async def send_email_batch(payload: schemas.EmailBatchRequest, background_tasks: BackgroundTasks):
    """
    Dispatches a parallel email drop across worker shards for 100,000+ recipients
    and updates deliverability telemetry (SPF/DKIM/DMARC) in the background.
    """
    audience = payload.audienceSize or 100000
    camp_name = payload.campaignName or "High-Velocity Omnichannel Blast"
    sub_a = payload.subjectA or "Exclusive early access inside ✨"
    sub_b = payload.subjectB or "Automate your client experience in clicks"

    job_data = initialize_batch_job(camp_name, audience, sub_a, sub_b)
    
    # Launch parallel batch dispatcher as async background task
    background_tasks.add_task(run_email_batch_job, job_data["jobId"], audience)

    return {
        "success": True,
        "message": f"Successfully queued parallel dispatch of {audience:,} emails across {job_data['totalShards']} worker shards",
        "job": job_data
    }

@router.get("/email/batch-status/{job_id}")
async def get_email_batch_status(job_id: str):
    """
    Returns live progress and deliverability logs for a background email batch.
    """
    job = EMAIL_JOBS_CACHE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Email job not found")
    return job
