# generate_report_test.py

from database_manager import DatabaseManager
from reportGenerator_latex import CreateLatex

def main():
    # Create DB manager
    db = DatabaseManager()

    # These may be empty/minimal — that's OK for now
    uiObj = getattr(db, "ui_data", {})
    Design_Check = getattr(db, "design_check", [])
    reportsummary = getattr(db, "report_summary", {
        "ProfileSummary": {
            "CompanyName": "Test Company",
            "CompanyLogo": "",
            "Group/TeamName": "Test Team",
            "Designer": "Ishan",
            "JobNumber": "001",
            "Client": "Test Client"
        },
        "ProjectTitle": "Financial LCCA Report",
        "Subtitle": "Auto-generated",
        "does_design_exist": False
    })

    report = CreateLatex()

    report.save_latex(
        uiObj=uiObj,
        Design_Check=Design_Check,
        reportsummary=reportsummary,
        filename="Financial_LCCA_Report",
        rel_path=".",
        Disp_2d_image=None,
        Disp_3d_image=None,
        module="LCCA"
    )

    print("✅ Report generation triggered")

if __name__ == "__main__":
    main()
