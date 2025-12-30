from pathlib import Path
from .financial_report_generator import FinancialReportGenerator


def generate_financial_pdf(data, time_cost):
    """
    Generates the financial LCCA report
    """

    # -------- locate project root --------
    root = Path(__file__).resolve().parents[2]

    # -------- correct template + output paths --------
    template_path = root / "osbridgelcca" / "reports" / "templates" / "financial_report.tex"
    output_dir = root / "osbridgelcca" / "reports" / "output"
    logo_path = root / "osbridgelcca" / "desktop_app" / "resources" / "osbridge_logo.png"

    # ensure folders exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # -------- generate PDF --------
    generator = FinancialReportGenerator(template_path, output_dir)

    pdf_path = generator.generate(
        data=data,
        time_cost=time_cost,
        logo_path=str(logo_path),
        filename="financial_lcca_report",
        output_dir=str(output_dir),
        template_file=str(template_path)
    )

    print("📁 PDF generated at:", pdf_path)
    return pdf_path
