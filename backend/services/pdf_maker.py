import jinja2
from weasyprint import HTML, CSS
from datetime import datetime
import os
from .highlighter import SyntaxHighlighter

class PdfGenerator:
    def __init__(self, template_dir="backend/templates"):
        self.template_loader = jinja2.FileSystemLoader(searchpath=os.path.abspath(template_dir))
        self.template_env = jinja2.Environment(loader=self.template_loader)
        self.template_file = "pdf_template.html"

    def generate_pdf(self, items: list, title: str = "Code Documentation") -> bytes:
        """
        items: List of dicts with keys: filename, language, code, description (optional)
        """
        # Enhance items with highlighrted code
        processed_items = []
        for item in items:
            highlighted = SyntaxHighlighter.highlight_code(item['code'], item['language'])
            processed_items.append({
                **item,
                'highlighted_code': highlighted
            })

        highlight_css = SyntaxHighlighter.get_css()
        
        template = self.template_env.get_template(self.template_file)
        html_content = template.render(
            items=processed_items,
            title=title,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            highlight_css=highlight_css
        )
        
        # Determine base_url to be the root of the project to resolve paths if needed
        # but here we rely on inline styles mostly.
        return HTML(string=html_content).write_pdf()
