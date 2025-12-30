import subprocess
from pathlib import Path


class FinancialReportGenerator:
    def __init__(self):
        # Root = src/osbridgelcca
        self.root = Path(__file__).resolve().parents[1]

        # Template inside osbridgelcca/reports/templates
        self.template = (
            self.root
            / "reports"
            / "templates"
            / "financial_report.tex"
        )

        # Output inside osbridgelcca/reports/output
        self.output_dir = (
            self.root
            / "reports"
            / "output"
        )

    def generate(self, data: dict, filename="financial_lcca_report"):
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        tex_file = self.output_dir / f"{filename}.tex"

        # Read LaTeX template safely
        content = self.template.read_text(encoding="utf-8")

        # Replace placeholders like <<KEY>>
        for key, value in data.items():
            content = content.replace(f"<<{key}>>", str(value))

        # Write final .tex file
        tex_file.write_text(content, encoding="utf-8")

        # Compile using TinyTeX (pdflatex)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            check=True
        )

        return self.output_dir / f"{filename}.pdf"
