from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict, time_cost: float):
    root = Path(__file__).resolve().parents[1]
    template = root / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "reports" / "output"
    logo = root / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator(template, output_dir)
    pdf_path = generator.generate(
        financial_data, time_cost, str(logo), "financial_lcca_report"
    )
    return pdf_path
