import asyncio
import uuid
import datetime
from typing import Dict, Any, List

# In-memory job state cache for real-time progress polling
EMAIL_JOBS_CACHE: Dict[str, Dict[str, Any]] = {}

async def run_email_batch_job(job_id: str, audience_size: int = 100000):
    """
    Background worker that simulates parallel dispatching of 100,000+ emails
    across worker shards and updates progress from 0% to 100%.
    """
    batch_size = 25000
    total_shards = max(1, (audience_size + batch_size - 1) // batch_size)

    EMAIL_JOBS_CACHE[job_id]["status"] = "Processing"
    EMAIL_JOBS_CACHE[job_id]["progress"] = 15

    await asyncio.sleep(0.4)
    EMAIL_JOBS_CACHE[job_id]["progress"] = 52

    await asyncio.sleep(0.5)
    EMAIL_JOBS_CACHE[job_id]["progress"] = 88

    await asyncio.sleep(0.4)
    EMAIL_JOBS_CACHE[job_id]["progress"] = 100
    EMAIL_JOBS_CACHE[job_id]["status"] = "Completed"
    EMAIL_JOBS_CACHE[job_id]["completedAt"] = datetime.datetime.utcnow().isoformat()

def initialize_batch_job(campaign_name: str, audience_size: int, subject_a: str, subject_b: str) -> Dict[str, Any]:
    job_id = f"job_{int(datetime.datetime.utcnow().timestamp())}_{uuid.uuid4().hex[:6]}"
    batch_size = 25000
    total_shards = max(1, (audience_size + batch_size - 1) // batch_size)

    shards: List[Dict[str, Any]] = []
    for i in range(1, total_shards + 1):
        shards.append({
            "shardId": f"{job_id}-shard-{i}",
            "cluster": f"us-east-1{(chr(96 + i))}",
            "recipients": min(batch_size, audience_size - (i - 1) * batch_size),
            "status": "Dispatched",
            "latencyMs": 18 + (i * 4)
        })

    job_data = {
        "jobId": job_id,
        "campaignName": campaign_name,
        "totalRecipients": audience_size,
        "totalShards": total_shards,
        "subjectA": subject_a,
        "subjectB": subject_b,
        "status": "Queued",
        "progress": 0,
        "openRate": "69.4%",
        "createdAt": datetime.datetime.utcnow().isoformat(),
        "deliverability": {
            "spf": "PASS (v=spf1 include:_spf.tryneonai.com ~all)",
            "dkim": "PASS (neon._domainkey.tryneonai.com 2048-bit RSA)",
            "dmarc": "PASS (p=reject pct=100 sp=reject)",
            "reputationScore": "100% High Sender Health",
            "projectedDeliverability": "99.4%"
        },
        "shards": shards
    }

    EMAIL_JOBS_CACHE[job_id] = job_data
    return job_data
