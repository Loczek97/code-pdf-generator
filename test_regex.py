import re

html_snippet = """<div class="source" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><span style="color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px;">1</span><span style="color: #557799">#include</span>
<span style="color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px;">2</span><span style="color: #333399; font-weight: bold">int</span>
</pre></div>"""

# Regex to find line number spans based on their unique padding style
pattern = re.compile(r'(<span style="[^"]*padding-left: 5px; padding-right: 5px;[^"]*">)\s*(\d+)\s*(</span>)')

def replacement(match):
    # match.group(1) is opening tag
    # match.group(2) is the number
    # match.group(3) is closing tag
    # We replace the text content with empty string, and add a class/attribute where we will inject content via CSS
    # Note: We can reuse the existing span or create a new one.
    # Let's keep the existing span effectively hidden/empty and append a specialized span?
    # Or just inject data-ln into the opening tag and remove the content.
    
    opening_tag = match.group(1)
    number = match.group(2)
    closing_tag = match.group(3)
    
    # Inject data-ln attribute into opening tag
    new_opening = opening_tag.replace('style="', f'data-ln="{number}" class="uncopyable-ln" style="')
    
    # Return empty content
    return f'{new_opening}{closing_tag}'

new_html = pattern.sub(replacement, html_snippet)

print("Original:")
print(html_snippet)
print("\nNew:")
print(new_html)
