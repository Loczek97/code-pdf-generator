from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

code = """def long_function_name_with_many_arguments(arg1, arg2, arg3, arg4, arg5):
    # This is a very long comment that should ideally wrap to the next line without causing any layout issues or overlapping text.
    print("Hello World" * 100)
"""

formatter = HtmlFormatter(style='friendly', linenos='inline', cssclass="source")
html = highlight(code, PythonLexer(), formatter)
css = formatter.get_style_defs('.source')

print("CSS:")
print(css)
print("\nHTML:")
print(html)
