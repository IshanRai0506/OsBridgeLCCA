from pathlib import Path
from osbridgelcca.simple_report.financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(data_dict, time_cost, logo_path=None):
    """
    Generates financial PDF report using mapped UI data + time cost
    """

    root = Path(__file__).resolve().parents[2]
    output_dir = root / "reports" / "output"
    template_file = root / "reports" / "templates" / "financial_report.tex"

    generator = FinancialReportGenerator(
        template_path=template_file,
        output_dir=output_dir,
        logo_path=logo_path
    )

    mapped = {
        "<<Analysis Period>>": data_dict.get("Analysis Period"),
        "<<Design Life>>": data_dict.get("Design Life"),
        "<<Discount Rate(Inflation Adjusted)>>": data_dict.get("Discount Rate(Inflation Adjusted)"),
        "<<Inflation Rate>>": data_dict.get("Inflation Rate"),
        "<<Interest Rate>>": data_dict.get("Interest Rate"),
        "<<Investment Ratio>>": data_dict.get("Investment Ratio"),
        "<<Time for Construction of Base Project>>": data_dict.get("Time for Construction of Base Project"),
        "<<TIME_COST>>": time_cost
    }

    return generator.generate(mapped)
