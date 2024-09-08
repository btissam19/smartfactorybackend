from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.controllers.jobmatch import compare_resume_to_job_description ,genrate_coverletter_resume_to_job_description ,genrate_tips_resume_to_job_description

router = APIRouter()

class JobDescriptionRequest(BaseModel):
    job_description: str

@router.post("/compare_resume")
async def compare_resume_endpoint(request: JobDescriptionRequest):
    job_description = request.job_description
    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required.")
    result= await compare_resume_to_job_description(job_description)
    if not result.get("comparison_results"):
        raise HTTPException(status_code=500, detail="we coudn't compare things")
    return result


@router.post("/cover_letter")
async def cover_letter_endpoint(request: JobDescriptionRequest):
    job_description = request.job_description
    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required.")
    result = await genrate_coverletter_resume_to_job_description(job_description)
    if not result.get("cover letter"):
        raise HTTPException(status_code=500, detail="Cover letter not generated.")
    return result


@router.post("/tips")
async def tips_endpoint(request: JobDescriptionRequest):
    job_description = request.job_description
    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required.")
    return await genrate_tips_resume_to_job_description(job_description)
