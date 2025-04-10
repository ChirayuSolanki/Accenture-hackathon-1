from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
# from pinecone_search import search_resumes
from services.send_Invite import send_interview_invitation
from services.json_to_sqlite import ResumeDatabase
from fastapi.middleware.cors import CORSMiddleware
from services.db_searching import search_resumes
from schema.models import JobDescription, EmailRequest, InterviewInviteRequest



db = ResumeDatabase()
app = FastAPI()

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search-resumes")
def search(job: JobDescription):
    try:
        matches = search_resumes(job.jd)
        return {"results": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-interview-invite")
def send_invite(req: InterviewInviteRequest):
    try:
        send_interview_invitation(
            recipient_email=req.email,
            interview_date=req.interview_date,
            interview_time=req.interview_time
        )
        return {"message": "Interview invitation sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resume/{sql_id}")
def get_resume(sql_id: int):
    try:
        resume = db.get_resume_by_sql_id(sql_id)
        return {"resume": resume}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Resume not found")