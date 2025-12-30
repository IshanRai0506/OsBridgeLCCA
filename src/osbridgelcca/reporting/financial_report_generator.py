from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self):
        root = Path(__file__).resolve().parents[1]
        self.template = root / "templates" / "financial_report.tex"

    def generate(self, financial_data: dict, time_cost: float, logo_path: str, filename: str = "financial_lcca_report"):
        template_text = self.template.read_text()

        # Replace placeholders
        for key, value in financial_data.items():
            template_text = template_text.replace(f"<<{key}>>", str(value))

        template_text = template_text.replace("<<TIME_COST>>", str(time_cost))
        template_text = template_text.replace("<<LOGO_PATH>>", logo_path)

        root = Path(__file__).resolve().parents[2]
        output_dir = root / "reports" / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        tex_file = output_dir / f"{filename}.tex"
        pdf_file = output_dir / f"{filename}.pdf"

        tex_file.write_text(template_text)

        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file.name], cwd=output_dir)

        return pdf_file
