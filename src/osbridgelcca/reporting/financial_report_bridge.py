from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data_dict, time_cost):
    gen = FinancialReportGenerator()

    mapped = {k: v for k, v in data_dict.items()}
    root = Path(__file__).resolve().parents[2]
    logo_path = str(root / "desktop_app" / "resources" / "osbridge_logo.png")

    return gen.generate(
        mapped=mapped,
        time_cost=time_cost,
        logo_path=logo_path
    )
