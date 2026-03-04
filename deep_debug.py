from backend.services.highlighter import SyntaxHighlighter
from backend.services.detector import LanguageDetector
from backend.services.highlighter import SyntaxHighlighter
from backend.services.detector import LanguageDetector
# from backend.services.pdf_maker import PdfGenerator - skipped to avoid weasyprint dep for debug

code_snippet = """
#include <iostream>
using namespace std;

int main() {
    cout << "Hello World";
    return 0;
}
"""

print("--- 1. Testing Language Detection ---")
lang = LanguageDetector.detect_language(code_snippet)
print(f"Detected Language: {lang}")

print("\n--- 2. Testing Highlighter ---")
html_out = SyntaxHighlighter.highlight_code(code_snippet, lang)
print("HTML Output Snippet:")
print(html_out[:200] + "...")

print("\n--- 3. Testing CSS Generation ---")
css = SyntaxHighlighter.get_css()
print("CSS Output Snippet:")
print(css[:200] + "...")

print("\n--- 4. Testing PDF Template Render ---")
# Manually render template to check final HTML
import jinja2
import os

template_loader = jinja2.FileSystemLoader(searchpath=os.path.abspath("backend/templates"))
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("pdf_template.html")

rendered = template.render(
    items=[{'filename': 'test.cpp', 'language': lang, 'highlighted_code': html_out}],
    title="Debug Doc",
    date="2024-01-01",
    highlight_css=css
)

print("Rendered HTML Snippet (checking CSS injection):")
if css in rendered:
    print("SUCCESS: CSS is present in rendered HTML")
else:
    print("FAILURE: CSS is MISSING from rendered HTML")

print("\n--- 5. checking if styles match ---")
if ".source .k" in css:
    print("CSS contains keywords style (.k)")
else:
    print("CSS missing .k style")
