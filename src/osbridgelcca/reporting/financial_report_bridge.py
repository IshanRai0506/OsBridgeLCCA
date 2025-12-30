# osbridgelcca/reporting/financial_report_bridge.py
from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data, time_cost):
    root = Path(__file__).resolve().parents[1]

    template_path = root / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "reports" / "output"
    logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator(template_path, output_dir)

    return generator.generate(
        data=data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )
