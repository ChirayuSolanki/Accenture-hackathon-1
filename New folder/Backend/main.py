from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
# from pinecone_search import search_resumes
from send_Invite import send_interview_invitation
from json_to_sqlite import ResumeDatabase
from fastapi.middleware.cors import CORSMiddleware

# 3. Initialize embedding model
import json
from sentence_transformers import SentenceTransformer
import pinecone
import os
import os
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)
index_name = 'resume'
# Now do stuff
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name, 
        dimension=1536, 
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )

index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')
# 3. Define the search function
def search_resumes(job_description, top_k=5):
    # Step 1: Create embedding from JD
    jd_embedding = model.encode(job_description).tolist()

    # Step 2: Query Pinecone
    results = index.query(
        vector=jd_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # Step 3: Return matches
    matches = []
    for match in results.get("matches", []):
        matches.append({
            "score": match["score"],
            "resume_id": match["id"],
            "sql_id": match["metadata"].get("sql_id"),
            "metadata": match["metadata"]
        })
    
    return matches





app = FastAPI()
# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class JobDescription(BaseModel):
    jd: str

class EmailRequest(BaseModel):
    email: EmailStr
    subject: str
    message: str


class InterviewInviteRequest(BaseModel):
    email: EmailStr
    interview_date: str
    interview_time: str


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

db = ResumeDatabase()
@app.get("/resume/{sql_id}")
def get_resume(sql_id: int):
    try:
        resume = db.get_resume_by_sql_id(sql_id)
        return {"resume": resume}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Resume not found")