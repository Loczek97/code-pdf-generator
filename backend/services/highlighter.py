from pygments import highlight
from pygments.formatters import HtmlFormatter
from .detector import LanguageDetector

class SyntaxHighlighter:
    @staticmethod
    def highlight_code(code: str, language: str) -> str:
        lexer = LanguageDetector.get_lexer(language)
        # Use 'table' to create physically separate columns for line numbers and code
        formatter = HtmlFormatter(style='colorful', linenos='table', cssclass="source", noclasses=True)
        return highlight(code, lexer, formatter)

    @staticmethod
    def get_css() -> str:
        formatter = HtmlFormatter(style='colorful', cssclass="source")
        return formatter.get_style_defs('.source')
