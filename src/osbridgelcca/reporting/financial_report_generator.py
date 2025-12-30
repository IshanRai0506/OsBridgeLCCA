from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data, time_cost, filename):
        tex = self.template.read_text()

        for key, val in data.items():
            tex = tex.replace(f"<<{key}>>", str(val))

        tex = tex.replace("<<TIME_COST>>", str(time_cost))

        tex_file = self.output_dir / f"{filename}.tex"
        tex_file.write_text(tex)

        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            cwd=self.output_dir
        )

        return str(self.output_dir / f"{filename}.pdf")

