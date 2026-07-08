from pydantic import BaseModel

# Request schema used when creating a job application
class JobCreate(BaseModel):
    company: str
    title: str
    status: str

# Response schema returned to the client
class JobResponse(BaseModel):
    id: int
    company: str
    title: str
    status: str

    model_config = {
        "from_attributes": True
    }

# Request schema used when updating a job application
class JobUpdate(BaseModel):
    company: str | None = None
    title: str | None = None
    status: str | None = None