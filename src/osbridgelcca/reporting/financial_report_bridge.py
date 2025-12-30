from pathlib import Path
from .financial_report_generator import FinancialReportGenerator


def generate_financial_pdf(data, time_cost):
    root = Path(__file__).resolve().parents[2]

    # Output folder
    output_dir = root / "reports" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Template location
    template = root / "reports" / "templates" / "financial_report.tex"

    # Logo path
    logo_path = root / "osbridgelcca" / "desktop_app" / "resources" / "osbridge_logo.png"

    # Create report generator
    generator = FinancialReportGenerator(template, output_dir)

    # Generate PDF
    pdf_path = generator.generate(
        data=data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )

    print("PDF SAVED AT:", pdf_path)
    return pdf_path
