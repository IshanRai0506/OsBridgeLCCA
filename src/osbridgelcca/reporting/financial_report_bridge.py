from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data: dict, time_cost: float):
    """
    Returns path to generated PDF
    """
    root = Path(__file__).resolve().parents[2]
    template = root / "osbridgelcca" / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "osbridgelcca" / "reports" / "output"
    logo_path = root / "osbridgelcca" / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator()

    return generator.generate(
        data=data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report",
        output_dir=output_dir,
        template_file=str(template)
    )
