from pydantic import BaseModel, EmailStr, Field
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