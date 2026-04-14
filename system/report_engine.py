from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# PDF GENERATOR
# =========================
def generate_pdf(
    filename,
    client,
    project,
    country,
    score,
    level,
    decision_conf,
    explanation,
    analysis,
    profile,
    volatility,
    confidence_label,
    confidence_score,
    recommendation
):

    # =========================
    # DOCUMENT SETUP
    # =========================
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    # =========================
    # HEADER
    # =========================
    content.append(Paragraph("GDSN-X™ ELITE REPORT", styles["Title"]))
    content.append(Spacer(1, 12))

    # =========================
    # CLIENT INFO
    # =========================
    content.append(Paragraph(f"<b>Client:</b> {client}", styles["Normal"]))
    content.append(Paragraph(f"<b>Project:</b> {project}", styles["Normal"]))
    content.append(Paragraph(f"<b>Country:</b> {country}", styles["Normal"]))
    content.append(Spacer(1, 12))

    # =========================
    # EXECUTIVE SUMMARY TABLE
    # =========================
    table_data = [
        ["Metric", "Value"],
        ["Risk Score", score],
        ["Risk Level", level],
        ["Decision Confidence", f"{decision_conf}%"],
        ["Volatility", volatility],
        ["Data Confidence", f"{confidence_label} ({confidence_score}%)"],
    ]

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    content.append(table)
    content.append(Spacer(1, 15))

    # =========================
    # KEY DRIVERS
    # =========================
    content.append(Paragraph("<b>Key Drivers</b>", styles["Heading2"]))
    content.append(Paragraph(explanation, styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # ANALYSIS
    # =========================
    content.append(Paragraph("<b>Analysis</b>", styles["Heading2"]))
    content.append(Paragraph(analysis, styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # PROFILE
    # =========================
    content.append(Paragraph("<b>Risk Profile</b>", styles["Heading2"]))
    content.append(Paragraph(profile, styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # RECOMMENDATION
    # =========================
    content.append(Paragraph("<b>Final Recommendation</b>", styles["Heading2"]))
    content.append(Paragraph(recommendation, styles["Normal"]))
    content.append(Spacer(1, 20))

    # =========================
    # DISCLAIMER
    # =========================
    content.append(Paragraph(
        "Disclaimer: This report is generated using a deterministic model "
        "and should not be considered financial or policy advice.",
        styles["Italic"]
    ))

    # =========================
    # BUILD PDF
    # =========================
    doc.build(content)

    return filename
