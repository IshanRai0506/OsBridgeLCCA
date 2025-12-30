from pathlib import Path
import subprocess
import tempfile

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data: dict, time_cost: float, logo_path: str, filename: str):
        tex = self.template.read_text()

        # Replace placeholders
        for key, value in data.items():
            tex = tex.replace(f"<<{key}>>", str(value))

        tex = tex.replace("<<TIME_COST>>", str(time_cost))
        tex = tex.replace("<<LOGO_PATH>>", logo_path.replace("\\", "/"))

        # Write temp file
        temp_tex = self.output_dir / f"{filename}.tex"
        temp_tex.write_text(tex)

        # Run pdflatex
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", temp_tex.name],
            cwd=self.output_dir,
        )

        pdf_file = self.output_dir / f"{filename}.pdf"
        return str(pdf_file)
