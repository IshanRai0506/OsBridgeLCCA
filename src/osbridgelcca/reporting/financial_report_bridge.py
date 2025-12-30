from pathlib import Path
from .financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict, time_cost: float):
    """
    Generates Financial LCCA PDF using Osdag-style LaTeX template.
    """

    # Base project folder
    root = Path(__file__).resolve().parents[2]

    # Correct template location
    template_path = root / "reports" / "templates" / "financial_report.tex"

    # Correct output folder
    output_dir = root / "reports" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Logo auto-included by generator.replace
    generator = FinancialReportGenerator(template_path, output_dir)

    pdf_path = generator.generate(
        financial_data=financial_data,
        time_cost=time_cost,
        filename="financial_lcca_report"     # output filename
    )

    return pdf_path
