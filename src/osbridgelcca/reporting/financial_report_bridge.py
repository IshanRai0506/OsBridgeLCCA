from osbridgelcca.reportGenerator_latex import CreateLatex

def generate_financial_pdf(financial_data, time_cost):
    """
    Generates OSDAg-style Financial LCCA PDF using TinyTeX
    """

    # 1. Convert LIVE UI data to OSDAg input table
    uiObj = {
        "Discount Rate (Inflation Adjusted)": f"{financial_data['Discount Rate(Inflation Adjusted)']*100:.2f} %",
        "Inflation Rate": f"{financial_data['Inflation Rate']*100:.2f} %",
        "Interest Rate": f"{financial_data['Interest Rate']*100:.2f} %",
        "Investment Ratio": str(financial_data['Investment Ratio']),
        "Design Life": f"{financial_data['Design Life']} years",
        "Analysis Period": f"{financial_data['Analysis Period']} years",
        "Total Time Cost": f"{time_cost:,.2f}"
    }

    # 2. Financial module has no checks yet
    Design_Check = []

    # 3. OSDAg report header metadata
    reportsummary = {
        "ProfileSummary": {
            "CompanyName": "OsBridgeLCCA",
            "CompanyLogo": "",
            "Group/TeamName": "LCCA Team",
            "Designer": "Ishan Rai",
            "JobNumber": "FIN-001",
            "Client": "Demo Client"
        },
        "ProjectTitle": "Financial LCCA Report",
        "Subtitle": "Generated automatically using TinyTeX",
        "does_design_exist": True,
        "logger_messages": "INFO: Financial report generated successfully"
    }

    # 4. Generate report
    report = CreateLatex()

    report.save_latex(
        uiObj=uiObj,
        Design_Check=Design_Check,
        reportsummary=reportsummary,
        filename="Financial_LCCA_Report",
        rel_path="reports/",
        Disp_2d_image=[],
        Disp_3d_image='',
        module=''
    )
