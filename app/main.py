from fastapi import FastAPI
from app.routes.uploadfiles import router as resume_upload
from app.routes.resumeinfo import router as resume_info
from app.routes.generatequestions import router as questions
from app.routes.jobmatch import router as jobmatch
from fastapi.middleware.cors import CORSMiddleware
from app.routes.last_news_jobs import router as last_news_jobs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hiringwebsite.netlify.app"],  # You can change this to specific domain when deploying
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (this is important for file uploads)
)

app.include_router(resume_upload)
app.include_router(resume_info)
app.include_router(questions)
app.include_router(jobmatch)
app.include_router(last_news_jobs)