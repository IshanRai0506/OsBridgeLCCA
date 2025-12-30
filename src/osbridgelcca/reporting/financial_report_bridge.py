from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data: dict, time_cost: float):
    root = Path(__file__).resolve().parents[2]

    template = root / "osbridgelcca" / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "osbridgelcca" / "reports" / "output"
    logo_path = root / "osbridgelcca" / "reports" / "templates" / "osbridge_logo.png"

    generator = FinancialReportGenerator(template=template, output_dir=output_dir)
    pdf_path = generator.generate(
        data=data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )

    print("📎 PDF Saved At:", pdf_path)
    return pdf_path
