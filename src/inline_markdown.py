import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Not valid Markdown syntax: no closing {delimiter} found.")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.PLAIN))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # Return list of ('alt text', 'URL') tuples from markdown format "![alt text](URL)".
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # match only "![str](str)", not "[str](str)".


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # Return list of ('anchor text', 'URL') tuples from markdown format "[anchor text](URL)".
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # don't match "![str](str)", only "[str](str)".
