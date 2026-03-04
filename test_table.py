from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

code = """
#include <iostream>
int main() { return 0; }
"""

# Test table output
formatter = HtmlFormatter(style='colorful', linenos='table', cssclass="source", noclasses=True)
html = highlight(code, CppLexer(), formatter)

print(html)
