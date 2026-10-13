import os

from markdown_to_html import markdown_to_html_node

TITLE_PLACEHOLDER = "{{ Title }}"
CONTENT_PLACEHOLDER = "{{ Content }}"


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from '{from_path}' to '{dest_path}'")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    html_page = template.replace(TITLE_PLACEHOLDER, title).replace(CONTENT_PLACEHOLDER, content)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(dest_path)
    with open(dest_path, "w") as f:
        f.write(html_page)



def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.removeprefix("#").strip()
    raise ValueError("h1 header not found")
