from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict, time_cost: float):
    root = Path(__file__).resolve().parents[2]
    logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator()
    return generator.generate(
        financial_data=financial_data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )
