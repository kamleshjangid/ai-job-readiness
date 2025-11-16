from app.celery_app import celery
from app.db.database import AsyncSessionLocal
from app.models.resume import Resume, ResumeStatus
from app.models.score import Score
import asyncio, json
from uuid import UUID
from typing import Dict

@celery.task(name="app.jobs.process_resume")
def process_resume(resume_id: str, filepath: str):
    """
    Celery task wrapper — we call a sync entrypoint that uses asyncio to run async DB code.
    """
    # call the async implementation (so you can reuse same logic)
    import asyncio
    from app.jobs.process_impl import process_resume_impl
    asyncio.run(process_resume_impl(resume_id, filepath))
