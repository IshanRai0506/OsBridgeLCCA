from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self):
        root = Path(__file__).resolve().parents[1]
        self.template = root / "reporting" / "templates" / "financial_report.tex"
        self.output_dir = root / "reporting" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data: dict, time_cost: float, logo_path: str, filename: str = "financial_lcca_report"):
        tex_path = self.output_dir / f"{filename}.tex"
        pdf_path = self.output_dir / f"{filename}.pdf"

        # Read template
        template_text = self.template.read_text()

        # Fill placeholders in LaTeX
        for key, value in data.items():
            template_text = template_text.replace(f"<<{key}>>", str(value))
        template_text = template_text.replace("<<TIME_COST>>", str(time_cost))
        template_text = template_text.replace("<<LOGO_PATH>>", logo_path.replace("\\", "/"))

        tex_path.write_text(template_text)

        # Compile latex
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_path.name],
            cwd=self.output_dir
        )

        return pdf_path
