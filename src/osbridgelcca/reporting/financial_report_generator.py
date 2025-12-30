from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data: dict, time_cost: float, logo_path: str, filename: str):
        tex_text = self.template.read_text()

        # Replace placeholders
        for key, val in data.items():
            tex_text = tex_text.replace(f"<<{key}>>", str(val))

        tex_text = tex_text.replace("<<TIME_COST>>", str(time_cost))
        tex_text = tex_text.replace("<<LOGO_PATH>>", logo_path.replace("\\", "/"))

        # Write temporary TEX file
        tex_file = self.output_dir / f"{filename}.tex"
        tex_file.write_text(tex_text)

        # Compile TeX → PDF
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return self.output_dir / f"{filename}.pdf"
