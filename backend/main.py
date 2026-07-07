from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI application instance
app = FastAPI()

# Schema used for creating a job application
class JobCreate(BaseModel):
    company: str
    title: str
    status: str
    
# Temporary in-memory storage until database integration is added
jobs = []

# Temporary ID counter until database-generated IDs are added
next_job_id = 1

# Home endpoint used to verify that the backend is running
@app.get("/")
def home():
    return {"message": "Hello, Job Tracker!"}

# Returns all job applications currently stored in memory
@app.get("/jobs")
def get_jobs():
    return jobs

# Returns a single job application by its ID
@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    for job in jobs:
        if job["id"] == job_id:
            return job
    return {"error": "Job not found"}


# Creates a new job application
# Request data is validated against the Job schema before this function executes
@app.post("/jobs")
def create_job(job: JobCreate):
    global next_job_id

    new_job = {
        "id": next_job_id,
        "company": job.company,
        "title": job.title,
        "status": job.status
    }

    jobs.append(new_job)
    next_job_id += 1

    return new_job