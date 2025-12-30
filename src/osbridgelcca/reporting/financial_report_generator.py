from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self):
        # templates folder inside osbridgelcca/reports/templates
        self.template = Path(__file__).resolve().parents[1] / "templates" / "financial_report.tex"

    def generate(self, data: dict, time_cost: float, logo_path: str, filename="financial_lcca_report"):

        root = Path(__file__).resolve().parents[2]
        output_dir = root / "reports" / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        tex_path = output_dir / f"{filename}.tex"
        pdf_path = output_dir / f"{filename}.pdf"

        # Read template content
        template_text = self.template.read_text()

        # Replace placeholders
        for key, value in data.items():
            template_text = template_text.replace(f"<<{key}>>", str(value))

        template_text = template_text.replace("<<TIME_COST>>", str(time_cost))
        template_text = template_text.replace("<<LOGO_PATH>>", logo_path)

        tex_path.write_text(template_text, encoding="utf-8")

        # Compile with pdflatex
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path.name], cwd=output_dir)

        return pdf_path
