from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RecipientInput(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr


class JobCreate(BaseModel):
    course_name: str = Field(min_length=1, max_length=200)
    certificate_date: date
    recipients: list[RecipientInput] = Field(min_length=1)


class JobCreated(BaseModel):
    id: int
    status: str
    total_count: int


class RecipientStatus(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: str
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobStatus(BaseModel):
    id: int
    course_name: str
    certificate_date: date
    status: str
    total_count: int
    success_count: int
    failed_count: int
    progress_percent: float
    created_at: datetime
    recipients: list[RecipientStatus]


class CertificateResponse(BaseModel):
    id: int
    recipient_id: int
    file_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
