from fastapi import FastAPI, HTTPException, Depends, status
from app.database import Base, engine
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.models.job import Job
from sqlalchemy.orm import Session
from app.dependencies import get_db
from sqlalchemy import select

# Creates database tables that do not already exist
Base.metadata.create_all(bind=engine)

# FastAPI application instance
app = FastAPI()

# Home endpoint used to verify that the backend is running
@app.get("/")
def home():
    return {"message": "Hello, Job Tracker!"}

# Returns all job applications stored in the database
@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db)
):
    statement = select(Job)
    result = db.execute(statement)
    jobs = result.scalars().all()

    return jobs

# Creates a new job application
@app.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    new_job = Job(
        company=job.company,
        title=job.title,
        status=job.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

# Returns a single job application by its ID
@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Job).where(Job.id == job_id)
    result = db.execute(statement)
    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

# Updates an existing job application
@app.patch("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
):
    statement = select(Job).where(Job.id == job_id)
    result = db.execute(statement)
    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Only update fields that were included in the request
    update_data = job_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job

# Deletes a job application by its ID
@app.delete("/jobs/{job_id}", response_model=JobResponse)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    statement = select(Job).where(Job.id == job_id)
    result = db.execute(statement)
    job = result.scalar_one_or_none()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return job
