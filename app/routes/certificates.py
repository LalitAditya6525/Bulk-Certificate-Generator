from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Certificate, Job, Recipient
from app.schemas import CertificateResponse

router = APIRouter(tags=["Certificates"])


@router.get(
    "/api/jobs/{job_id}/certificates",
    response_model=list[CertificateResponse],
)
def list_job_certificates(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    certificates = (
        db.query(Certificate)
        .join(Recipient, Certificate.recipient_id == Recipient.id)
        .filter(Recipient.job_id == job_id)
        .order_by(Certificate.id)
        .all()
    )

    return certificates


@router.get("/api/certificates/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    certificate = db.get(Certificate, certificate_id)

    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found",
        )

    file_path = Path(certificate.file_path)

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found",
        )

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf",
    )
