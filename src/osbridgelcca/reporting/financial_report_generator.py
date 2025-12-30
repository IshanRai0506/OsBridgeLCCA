# osbridgelcca/reporting/financial_report_generator.py
from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data, time_cost, logo_path, filename):
        tex_text = self.template.read_text()

        # Replace placeholders
        safe_logo_path = logo_path.replace("\\", "/")
        tex_text = tex_text.replace("<<LOGO_PATH>>", safe_logo_path)

        for key in data:
            tex_text = tex_text.replace(f"<<{key}>>", str(data[key]))
        tex_text = tex_text.replace("<<TIME_COST>>", str(time_cost))

        tex_file = self.output_dir / f"{filename}.tex"
        tex_file.write_text(tex_text)

        # Run pdflatex in output folder
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        pdf_path = self.output_dir / f"{filename}.pdf"
        return str(pdf_path)
