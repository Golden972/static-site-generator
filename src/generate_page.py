import os

from markdown_to_html import markdown_to_html_node

TITLE_PLACEHOLDER = "{{ Title }}"
CONTENT_PLACEHOLDER = "{{ Content }}"


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    dir_entries = os.listdir(dir_path_content)
    if len(dir_entries) == 0:
        return
    for entry in dir_entries:
        content_path = os.path.join(dir_path_content, entry)
        destination = os.path.join(dest_dir_path, entry)
        if not os.path.isfile(content_path):
            if not os.path.isdir(content_path):
                raise ValueError(f"Specified path {content_path} is not a file or directory")
            os.mkdir(destination)
            print(f"MKDIR: '{destination}'")
            generate_pages_recursive(content_path, template_path, destination, basepath)
        else:
            generate_page(content_path, template_path, destination.removesuffix(".md") + ".html", basepath)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from '{from_path}' to '{dest_path}'")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)
    html_page = template
    html_page = html_page.replace(TITLE_PLACEHOLDER, title)
    html_page = html_page.replace(CONTENT_PLACEHOLDER, content)
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')
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
