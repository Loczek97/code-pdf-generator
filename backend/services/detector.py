from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound

class LanguageDetector:
    @staticmethod
    def detect_language(code: str) -> str:
        try:
            lexer = guess_lexer(code)
            return lexer.name
        except ClassNotFound:
            return "Text"

    @staticmethod
    def get_lexer(language_name: str):
        try:
            return get_lexer_by_name(language_name)
        except ClassNotFound:
            return get_lexer_by_name("text")
