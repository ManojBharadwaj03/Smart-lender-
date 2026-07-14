import os
from datetime import datetime

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "Smart_Lender_Project.pdf")
FILES_TO_INCLUDE = [
    "README.md",
    "requirements.txt",
    "train_model.py",
    "app.py",
    ".gitignore",
    os.path.join("data", "loan_data.csv"),
    os.path.join("templates", "index.html"),
    os.path.join("templates", "result.html"),
]

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CenteredTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        spaceBefore=16,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="SubHeader",
        parent=styles["Heading3"],
        spaceBefore=12,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="CustomCode",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8,
        leading=10,
        leftIndent=0,
        rightIndent=0,
    )
)
styles.add(
    ParagraphStyle(
        name="Note",
        parent=styles["Italic"],
        fontSize=10,
        textColor="#333333",
        spaceAfter=12,
    )
)


def read_file_contents(path):
    absolute_path = os.path.join(PROJECT_ROOT, path)
    if not os.path.exists(absolute_path):
        return None
    with open(absolute_path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def read_file_preview(path, max_lines=12):
    absolute_path = os.path.join(PROJECT_ROOT, path)
    if not os.path.exists(absolute_path):
        return None
    with open(absolute_path, "r", encoding="utf-8", errors="replace") as handle:
        lines = [line.rstrip() for _, line in zip(range(max_lines), handle)]
    return "\n".join(lines)


def build_intro():
    content = read_file_contents("README.md")
    if not content:
        return [Paragraph("README file not found.", styles["Normal"])]

    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    story = [Paragraph("Project Overview", styles["SectionHeader"])]
    for paragraph in paragraphs[:3]:
        story.append(Paragraph(paragraph.replace("\n", " "), styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))
    return story


def build_intro():
    content = read_file_contents("README.md")
    story = [Paragraph("Project Overview", styles["SectionHeader"])]
    if not content:
        story.append(Paragraph("README file not found.", styles["Normal"]))
        return story

    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    for paragraph in paragraphs:
        story.append(Paragraph(paragraph.replace("\n", " "), styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))
    return story


def add_file_section(story, path, is_last=False):
    story.append(Paragraph(f"File: {path}", styles["SectionHeader"]))
    content = read_file_contents(path)
    if content is None:
        story.append(Paragraph("File not found.", styles["Normal"]))
    else:
        story.append(Paragraph("Full file contents:", styles["SubHeader"]))
        story.append(Preformatted(content, styles["CustomCode"]))
    if not is_last:
        story.append(PageBreak())


def build_document():
    story = []
    story.append(Paragraph("Smart Lender - Loan Eligibility Prediction", styles["CenteredTitle"]))
    story.append(Paragraph("Machine learning web application for loan approval prediction.", styles["SubHeader"]))
    story.append(Paragraph(f"Generated on {datetime.now():%Y-%m-%d %H:%M:%S}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Smart Lender predicts loan eligibility from applicant data using preprocessed features and a trained model. The report includes project architecture, setup details, dataset contents, and complete source files.", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Contents", styles["SectionHeader"]))
    for item in [
        "Project Overview and README",
        "Setup and Requirements",
        "Included Project Files",
        "Full Project Source Contents",
    ]:
        story.append(Paragraph(item, styles["Bullet"]))
    story.append(PageBreak())

    story.extend(build_intro())

    story.append(Paragraph("Setup and Requirements", styles["SectionHeader"]))
    story.append(Paragraph("Install required Python packages, train the model, and launch the Flask web application.", styles["Normal"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Recommended commands:", styles["SubHeader"]))
    story.append(Preformatted("python -m venv venv\nvenv\\Scripts\\activate\npip install -r requirements.txt\npython train_model.py\npython app.py", styles["CustomCode"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Data columns used in the loan dataset:", styles["Normal"]))
    for column in [
        "Gender", "Married", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome",
        "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area", "Loan_Status",
    ]:
        story.append(Paragraph(column, styles["Bullet"]))
    story.append(PageBreak())

    story.append(Paragraph("Included Project Files", styles["SectionHeader"]))
    for path in FILES_TO_INCLUDE:
        story.append(Paragraph(path, styles["Bullet"]))
    story.append(PageBreak())

    for index, path in enumerate(FILES_TO_INCLUDE):
        add_file_section(story, path, is_last=(index == len(FILES_TO_INCLUDE) - 1))

    return story


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    page_number_text = f"Page {doc.page}"
    canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, page_number_text)
    canvas.restoreState()


def main():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    story = build_document()
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
