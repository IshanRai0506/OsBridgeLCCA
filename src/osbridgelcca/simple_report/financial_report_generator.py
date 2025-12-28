import subprocess
from pathlib import Path

class FinancialReportGenerator:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.template = self.root / "osbridgelcca" / "reports" / "templates" / "financial_report.tex"
        self.output_dir = self.root / "osbridgelcca" / "reports" / "output"

        # Path of OSBridge logo for header
        self.logo_path = str(self.root / "osbridgelcca" / "desktop_app" / "resources" / "osbridge_logo.png")

    def generate(self, data: dict, filename="financial_lcca_report"):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        tex_file = self.output_dir / f"{filename}.tex"

        content = self.template.read_text()

        # Replace placeholders inside LaTeX template
        for key, value in data.items():
            content = content.replace(f"<<{key}>>", str(value))

        # Insert logo inside <<LOGO_PATH>>
        content = content.replace("<<LOGO_PATH>>", self.logo_path.replace("\\", "/"))

        tex_file.write_text(content, encoding="utf-8")

        # Run LaTeX compiler
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            check=True
        )

        return self.output_dir / f"{filename}.pdf"
