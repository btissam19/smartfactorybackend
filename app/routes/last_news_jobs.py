from fastapi import  HTTPException ,APIRouter
from pydantic import BaseModel
from gnews import GNews
from typing import  Dict
from app.controllers.last_jobs_news import *

router = APIRouter()

# Initialize GNews
google_news = GNews()

# Request body model
class NewsSearchRequest(BaseModel):
    query: str
    
    
class JobSearchRequest(BaseModel):
    job: str
    location: str


@router.post("/search_news")
async def search_news_endpoint(request: NewsSearchRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Search query is required.")
    
    # Fetch news based on the user's input
    google_news.period = '3d'  # You can make this dynamic
    google_news.max_results = 20  # Limit number of results
    news_by_keyword = google_news.get_news(query)
    
    if not news_by_keyword:
        raise HTTPException(status_code=500, detail="No news found for the query.")
    
    return news_by_keyword




# FastAPI route to handle job search requests
@router.post("/search_job")
async def search_all_jobs(request: JobSearchRequest) -> Dict:
    job = request.job
    location = request.location
    try:
        google_jobs = search_google_jobs(job,location)
        return {
                "google_jobs": google_jobs,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
