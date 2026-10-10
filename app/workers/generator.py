import logging

from app.database import SessionLocal
from app.models import Certificate, Job, Recipient
from app.services.pdf_generator import generate_certificate_pdf

logger = logging.getLogger(__name__)


def process_job(job_id: int):
    """Generate certificates for all recipients in a job."""

    try:
        with SessionLocal() as db:
            job = db.get(Job, job_id)

            if job is None:
                logger.error("Job %s does not exist", job_id)
                return

            job.status = "processing"
            db.commit()

            recipient_ids = (
                db.query(Recipient.id)
                .filter(Recipient.job_id == job_id)
                .order_by(Recipient.id)
                .all()
            )

            recipient_ids = [row[0] for row in recipient_ids]

        for recipient_id in recipient_ids:
            with SessionLocal() as db:
                recipient = db.get(Recipient, recipient_id)

                if recipient is None:
                    continue

                recipient.status = "processing"
                db.commit()

                # Copy required data before doing file generation.
                name = recipient.name

                job = db.get(Job, job_id)
                if job is None:
                    continue

                course_name = job.course_name
                certificate_date = job.certificate_date

            try:
                file_path = generate_certificate_pdf(
                    recipient_name=name,
                    course_name=course_name,
                    certificate_date=certificate_date,
                    recipient_id=recipient_id,
                )

                with SessionLocal() as db:
                    recipient = db.get(Recipient, recipient_id)
                    job = db.get(Job, job_id)

                    if recipient is None or job is None:
                        raise RuntimeError(
                            "Recipient or job disappeared during processing"
                        )

                    db.add(
                        Certificate(
                            recipient_id=recipient_id,
                            file_path=file_path,
                        )
                    )

                    recipient.status = "completed"
                    recipient.error_message = None
                    job.success_count += 1
                    db.commit()

            except Exception as exc:
                logger.exception(
                    "Certificate generation failed for recipient %s",
                    recipient_id,
                )

                # Roll back any failed database transaction.
                with SessionLocal() as db:
                    recipient = db.get(Recipient, recipient_id)
                    job = db.get(Job, job_id)

                    if recipient is not None and job is not None:
                        recipient.status = "failed"
                        recipient.error_message = str(exc)[:2000]
                        job.failed_count += 1
                        db.commit()

                # Continue processing the remaining recipients.

        with SessionLocal() as db:
            job = db.get(Job, job_id)

            if job is not None:
                if job.failed_count > 0:
                    job.status = "completed_with_errors"
                else:
                    job.status = "completed"

                db.commit()

    except Exception:
        logger.exception("Unexpected failure while processing job %s", job_id)

        with SessionLocal() as db:
            job = db.get(Job, job_id)

            if job is not None:
                job.status = "failed"
                db.commit()
