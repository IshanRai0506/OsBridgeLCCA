from pathlib import Path
import subprocess
import tempfile

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data, time_cost, logo_path, filename, output_dir, template_file):
        tex_text = Path(template_file).read_text()

        tex_text = tex_text.replace("<<LOGO_PATH>>", logo_path)
        tex_text = tex_text.replace("<<Discount Rate(Inflation Adjusted)>>", str(data["Discount Rate(Inflation Adjusted)"]))
        tex_text = tex_text.replace("<<Inflation Rate>>", str(data["Inflation Rate"]))
        tex_text = tex_text.replace("<<Interest Rate>>", str(data["Interest Rate"]))
        tex_text = tex_text.replace("<<Investment Ratio>>", str(data["Investment Ratio"]))
        tex_text = tex_text.replace("<<Design Life>>", str(data["Design Life"]))
        tex_text = tex_text.replace("<<Time for Construction of Base Project>>", str(data["Time for Construction of Base Project"]))
        tex_text = tex_text.replace("<<Analysis Period>>", str(data["Analysis Period"]))
        tex_text = tex_text.replace("<<TIME_COST>>", str(time_cost))

        output_dir.mkdir(parents=True, exist_ok=True)
        tex_path = output_dir / f"{filename}.tex"
        pdf_path = output_dir / f"{filename}.pdf"

        tex_path.write_text(tex_text)

        import subprocess
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path.name], cwd=output_dir)

        return pdf_path
