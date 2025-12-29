# financial_report_bridge.py

from pathlib import Path
from osbridgelcca.simple_report.financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict, time_cost=None, output_dir=None, logo_path=None):
    generator = FinancialReportGenerator()

    mapped = {
        "Analysis Period": financial_data.get("Analysis Period"),
        "Design Life": financial_data.get("Design Life"),
        "Discount Rate(Inflation Adjusted)": financial_data.get("Discount Rate(Inflation Adjusted)"),
        "Inflation Rate": financial_data.get("Inflation Rate"),
        "Interest Rate": financial_data.get("Interest Rate"),
        "Investment Ratio": financial_data.get("Investment Ratio"),
        "Time for Construction of Base Project": financial_data.get("Time for Construction of Base Project"),
        "TIME_COST": time_cost
    }

    return generator.generate(data=mapped, output_dir=output_dir, logo_path=logo_path)
