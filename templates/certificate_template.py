from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth


PAGE_SIZE = landscape(A4)


def draw_certificate(
    canvas,
    recipient_name: str,
    course_name: str,
    certificate_date: str,
):
    width, height = PAGE_SIZE

    # Background
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)

    # Decorative border
    margin = 28
    canvas.setStrokeColor(colors.HexColor("#17365D"))
    canvas.setLineWidth(3)
    canvas.rect(
        margin,
        margin,
        width - 2 * margin,
        height - 2 * margin,
        fill=0,
        stroke=1,
    )

    canvas.setStrokeColor(colors.HexColor("#D4AF37"))
    canvas.setLineWidth(1)
    canvas.rect(
        margin + 8,
        margin + 8,
        width - 2 * (margin + 8),
        height - 2 * (margin + 8),
        fill=0,
        stroke=1,
    )

    # Heading
    canvas.setFillColor(colors.HexColor("#17365D"))
    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawCentredString(
        width / 2,
        height - 105,
        "CERTIFICATE OF COMPLETION",
    )

    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 14)
    canvas.drawCentredString(
        width / 2,
        height - 145,
        "This certificate is proudly presented to",
    )

    # Recipient name: shrink font if the name is long.
    font_size = 28
    max_name_width = width - 120

    while (
        font_size > 14
        and stringWidth(
            recipient_name,
            "Helvetica-Bold",
            font_size,
        ) > max_name_width
    ):
        font_size -= 1

    canvas.setFillColor(colors.HexColor("#17365D"))
    canvas.setFont("Helvetica-Bold", font_size)
    canvas.drawCentredString(
        width / 2,
        height - 195,
        recipient_name,
    )

    canvas.setStrokeColor(colors.HexColor("#D4AF37"))
    canvas.line(
        width / 2 - 150,
        height - 208,
        width / 2 + 150,
        height - 208,
    )

    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 14)
    canvas.drawCentredString(
        width / 2,
        height - 245,
        "for successfully completing the course",
    )

    canvas.setFillColor(colors.HexColor("#17365D"))
    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(
        width / 2,
        height - 280,
        course_name,
    )

    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(
        width / 2,
        height - 325,
        f"Date of completion: {certificate_date}",
    )

    # Signature area
    canvas.setStrokeColor(colors.HexColor("#555555"))
    canvas.line(
        width / 2 - 85,
        85,
        width / 2 + 85,
        85,
    )

    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(
        width / 2,
        68,
        "Authorized Signature",
    )
