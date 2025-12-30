from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data, time_cost, logo_path, filename):
        tex = self.template.read_text()

        # replace placeholders
        tex = tex.replace("<<LOGO_PATH>>", logo_path)
        for key, value in data.items():
            tex = tex.replace(f"<<{key}>>", str(value))
        tex = tex.replace("<<TIME_COST>>", str(time_cost))

        tex_file = self.output_dir / f"{filename}.tex"
        pdf_file = self.output_dir / f"{filename}.pdf"

        tex_file.write_text(tex)

        # compile TeX
        subprocess.run(["pdflatex", str(tex_file.name)], cwd=self.output_dir)

        return pdf_file
