from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data, time_cost):
    root = Path(__file__).resolve().parents[2]
    template = root / "osbridgelcca" / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "osbridgelcca" / "reports" / "output"

    generator = FinancialReportGenerator(template, output_dir)

    pdf_path = generator.generate(data, time_cost, filename="financial_lcca_report")
    print("📁 PDF generated at:", pdf_path)
    return pdf_path

