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


def split_nodes_image_link_helper(node: TextNode, matches: list[tuple[str, str]], text_type: TextType) -> list[TextNode]:
    split_nodes = []
    remaining_text = node.text
    for i in range(len(matches)):
        text, url = matches[i]
        if text_type == TextType.IMAGE:
            split_text = remaining_text.split(f"![{text}]({url})", 1)
        elif text_type == TextType.LINK:
            split_text = remaining_text.split(f"[{text}]({url})", 1)
        else:
            raise ValueError(f"text_type {text_type} is invalid. Must be TextType.IMAGE or TextType.LINK")
        if len(split_text) != 2:
            raise ValueError("invalid markdown, image or link not closed")
        remaining_text = split_text[1]
        if split_text[0] != "":
            split_nodes.append(TextNode(split_text[0], TextType.PLAIN))
        split_nodes.append(TextNode(text, text_type, url))
    if remaining_text != "":
        split_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return split_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        else:
            split_nodes = split_nodes_image_link_helper(node, matches, TextType.IMAGE)
            new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        else:
            split_nodes = split_nodes_image_link_helper(node, matches, TextType.LINK)
            new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.PLAIN)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
