from osbridgelcca.simple_report.financial_report_generator import FinancialReportGenerator

def generate_financial_pdf(financial_data: dict):
    generator = FinancialReportGenerator()

    mapped = {
        "DISCOUNT_RATE": financial_data["Discount Rate(Inflation Adjusted)"],
        "INFLATION_RATE": financial_data["Inflation Rate"],
        "INTEREST_RATE": financial_data["Interest Rate"],
        "INVESTMENT_RATIO": financial_data["Investment Ratio"],
        "DESIGN_LIFE": financial_data["Design Life"],
        "CONSTR_TIME": financial_data["Time for Construction of Base Project"],
        "ANALYSIS_PERIOD": financial_data["Analysis Period"],
    }

    pdf_path = generator.generate(mapped, filename="financial_report")
    print("PDF generated at:", pdf_path)
    return pdf_path