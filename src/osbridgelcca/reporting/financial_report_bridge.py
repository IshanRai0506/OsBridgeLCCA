from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict, time_cost: float):
    """
    Bridge API called from UI FinancialData -> generates PDF using template and generator.
    """

    root = Path(__file__).resolve().parents[1]   # /osbridgelcca
    output_dir = root / "reports" / "output"
    templates_dir = root / "reporting" / "templates"
    logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator(
        template_path=templates_dir / "financial_report.tex",
        output_dir=output_dir
    )

    return generator.generate(
        data=financial_data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )
