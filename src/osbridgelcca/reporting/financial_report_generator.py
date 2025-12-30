from pathlib import Path
import subprocess

class FinancialReportGenerator:
    def __init__(self, template_path: Path, output_dir: Path):
        self.template = template_path                      # template .tex
        self.output_dir = output_dir                       # directory where PDF will be created
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, data: dict, time_cost: float, logo_path: str, filename: str):
        # Load template
        tex_text = self.template.read_text()

        # Replace placeholders
        tex_text = tex_text.replace("<<LOGO_PATH>>", logo_path)
        tex_text = tex_text.replace("<<Discount Rate(Inflation Adjusted)>>", str(data["Discount Rate(Inflation Adjusted)"]))
        tex_text = tex_text.replace("<<Inflation Rate>>", str(data["Inflation Rate"]))
        tex_text = tex_text.replace("<<Interest Rate>>", str(data["Interest Rate"]))
        tex_text = tex_text.replace("<<Investment Ratio>>", str(data["Investment Ratio"]))
        tex_text = tex_text.replace("<<Design Life>>", str(data["Design Life"]))
        tex_text = tex_text.replace("<<Time for Construction of Base Project>>", str(data["Time for Construction of Base Project"]))
        tex_text = tex_text.replace("<<Analysis Period>>", str(data["Analysis Period"]))
        tex_text = tex_text.replace("<<TIME_COST>>", str(time_cost))

        # Write temporary .tex file
        tex_file = self.output_dir / f"{filename}.tex"
        tex_file.write_text(tex_text)

        # Run LaTeX command
        cmd = ["pdflatex", "-interaction=nonstopmode", str(tex_file)]
        subprocess.run(cmd, cwd=self.output_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pdf_path = self.output_dir / f"{filename}.pdf"
        return pdf_path
