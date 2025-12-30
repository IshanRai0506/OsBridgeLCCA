from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict, time_cost: float):
    """
    Bridge wrapper for generating PDF in Osdag-style format
    """

    # Resolve correct project directory
    root = Path(__file__).resolve().parents[2]

    # Financial PDF output location
    output_dir = root / "reports" / "output"

    # Logo
    logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

    generator = FinancialReportGenerator()

    # ---- IMPORTANT: generator.generate ONLY TAKES (financial_data, time_cost, logo_path, output_path) ----
    pdf_file = generator.generate(
        financial_data,
        time_cost,
        str(logo_path),
        output_dir
    )

    return pdf_file
