from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data: dict, time_cost: float):
    """Generate OSBridge–LCCA PDF using LaTeX template"""

    root = Path(__file__).resolve().parents[1]
    output_dir = root / "reports" / "output"
    template = root / "reports" / "templates" / "financial_report.tex"
    logo_path = root.parent / "desktop_app" / "resources" / "osbridge_logo.png"

    output_dir.mkdir(parents=True, exist_ok=True)

    generator = FinancialReportGenerator(template)

    return generator.generate(
        data=data,
        time_cost=time_cost,
        output_dir=str(output_dir),
        logo_path=str(logo_path),
        filename="financial_lcca_report"
    )
