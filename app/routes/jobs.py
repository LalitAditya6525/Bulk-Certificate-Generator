from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, Recipient
from app.schemas import JobCreate, JobCreated, JobStatus
from app.workers.generator import process_job

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("", response_model=JobCreated, status_code=202)
def create_job(
    payload: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    job = Job(
        course_name=payload.course_name,
        certificate_date=payload.certificate_date,
        status="queued",
        total_count=len(payload.recipients),
        success_count=0,
        failed_count=0,
    )

    db.add(job)
    db.flush()

    for item in payload.recipients:
        recipient = Recipient(
            name=item.name.strip(),
            email=str(item.email),
            status="pending",
            job_id=job.id,
        )
        db.add(recipient)

    db.commit()
    db.refresh(job)

    job_id = job.id
    background_tasks.add_task(process_job, job_id)

    return JobCreated(
        id=job.id,
        status=job.status,
        total_count=job.total_count,
    )


@router.get("/{job_id}", response_model=JobStatus)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    recipients = (
        db.query(Recipient)
        .filter(Recipient.job_id == job_id)
        .order_by(Recipient.id)
        .all()
    )

    processed_count = job.success_count + job.failed_count

    progress = (
        round(processed_count * 100 / job.total_count, 2)
        if job.total_count
        else 0.0
    )

    return JobStatus(
        id=job.id,
        course_name=job.course_name,
        certificate_date=job.certificate_date,
        status=job.status,
        total_count=job.total_count,
        success_count=job.success_count,
        failed_count=job.failed_count,
        progress_percent=progress,
        created_at=job.created_at,
        recipients=recipients,
    )
