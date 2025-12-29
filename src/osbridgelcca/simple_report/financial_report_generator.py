import subprocess
from pathlib import Path

class FinancialReportGenerator:
    def __init__(self, template_path, output_dir, logo_path=None):
        self.template = template_path
        self.output_dir = output_dir
        self.logo_path = logo_path

    def generate(self, values_dict, filename="financial_lcca_report"):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        tex_file = self.output_dir / f"{filename}.tex"
        pdf_file = self.output_dir / f"{filename}.pdf"

        content = self.template.read_text()

        # Insert Logo
        if "<<LOGO_PATH>>" in content:
            content = content.replace("<<LOGO_PATH>>", self.logo_path.replace("\\", "/"))

        # Insert values
        for key, value in values_dict.items():
            content = content.replace(str(key), str(value))

        tex_file.write_text(content)

        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            check=False
        )

        return pdf_file
