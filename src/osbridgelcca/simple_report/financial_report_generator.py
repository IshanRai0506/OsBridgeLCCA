import subprocess
from pathlib import Path

class FinancialReportGenerator:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.template = self.root / "reports" / "templates" / "financial_report.tex"
        self.output_dir = self.root / "reports" / "output"

    def generate(self, data: dict, filename="financial_lcca_report"):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        tex_file = self.output_dir / f"{filename}.tex"

        content = self.template.read_text(encoding="utf-8")

        for key, value in data.items():
            content = content.replace(f"<<{key}>>", str(value))

        tex_file.write_text(content, encoding="utf-8")

        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            check=True
        )

        return self.output_dir / f"{filename}.pdf"
