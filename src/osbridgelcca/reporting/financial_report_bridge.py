from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data, time_cost):
    root = Path(__file__).resolve().parents[2]       # src/osbridgelcca
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
    print("📁 PDF generated at:", pdf_path)
    return pdf_path
