import subprocess
from pathlib import Path

class FinancialReportGenerator:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.template = self.root / "reports" / "templates" / "financial_report.tex"
        self.output_dir = self.root / "reports" / "output"

    def generate(self, data: dict, time_cost: float, logo_path: str, filename="financial_lcca_report"):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        tex_file = self.output_dir / f"{filename}.tex"
        content = self.template.read_text()

        # replace variables
        for key, value in data.items():
            content = content.replace(f"<<{key}>>", str(value))

        content = content.replace("<<TIME_COST>>", str(time_cost))
        content = content.replace("<<LOGO_PATH>>", logo_path.replace("\\", "/"))

        tex_file.write_text(content)

        # run pdflatex
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            check=True
        )

        return self.output_dir / f"{filename}.pdf"
