import asyncio
from app.db.database import AsyncSessionLocal
from app.models.resume import Resume, ResumeStatus
from app.models.score import Score
from app.ai.extractors import extract_text_from_file
from app.ai.llm_client import analyze_resume_text

async def process_resume_impl(resume_id: str, filepath: str):
    text = extract_text_from_file(filepath)
    # perform lightweight pre-processing
    text = text[:20000]  # limit length
    # call LLM or model
    result = await analyze_resume_text(text)
    # persist
    async with AsyncSessionLocal() as session:
        resume = await session.get(Resume, resume_id)
        if resume:
            resume.status = ResumeStatus.processing
        score = Score(
            resume_id=resume_id,
            overall_score=result["overall_score"],
            skills_score=result["skills_score"],
            communication_score=result["communication_score"],
            technical_score=result["technical_score"],
            details=result.get("details")
        )
        session.add(score)
        if resume:
            resume.status = ResumeStatus.done
        await session.commit()
