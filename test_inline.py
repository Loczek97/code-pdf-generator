from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

code = """
#include <iostream>
int main() { return 0; }
"""

# Test inline styles
formatter = HtmlFormatter(style='colorful', linenos='inline', cssclass="source", noclasses=True)
html = highlight(code, CppLexer(), formatter)

print(html)
