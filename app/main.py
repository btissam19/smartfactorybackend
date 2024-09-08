from fastapi import FastAPI
from app.routes.uploadfiles import router as resume_upload
from app.routes.resumeinfo import router as resume_info
from app.routes.generatequestions import router as questions
from app.routes.jobmatch import router as jobmatch
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # You can change this to specific domain when deploying
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (this is important for file uploads)
)

app.include_router(resume_upload)
app.include_router(resume_info)
app.include_router(questions)
app.include_router(jobmatch)
