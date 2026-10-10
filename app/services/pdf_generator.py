import os
from pathlib import Path
from uuid import uuid4

from reportlab.pdfgen import canvas

from templates.certificate_template import (
    PAGE_SIZE,
    draw_certificate,
)


def generate_certificate_pdf(
    recipient_name: str,
    course_name: str,
    certificate_date,
    recipient_id: int,
) -> str:
    output_dir = Path(
        os.getenv("CERTIFICATE_DIR", "generated")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"certificate_{recipient_id}_{uuid4().hex}.pdf"
    file_path = output_dir / filename

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=PAGE_SIZE,
    )

    draw_certificate(
        pdf,
        recipient_name,
        course_name,
        certificate_date.strftime("%d %B %Y"),
    )

    pdf.save()

    return str(file_path.resolve())
