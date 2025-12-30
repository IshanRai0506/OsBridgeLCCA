from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data: dict, time_cost: float):
    root = Path(__file__).resolve().parents[2]
    template = root / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "reports" / "output"
    logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator(template_path=template, output_dir=output_dir)
    pdf_path = generator.generate(
        data=data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )
    return pdf_path
