import re

from block_markdown import block_to_block_type, markdown_to_blocks
from blocknode import BlockType
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def create_paragraph_node(block: str) -> ParentNode:
    # Replace newlines with spaces without creating multiple spaces in a row
    cleaned_block = re.sub(r"[\r\n]+", " ", block)
    child_nodes = text_to_children(cleaned_block)
    return ParentNode("p", child_nodes)


def create_heading_node(block: str) -> ParentNode:
    cleaned_block = block.lstrip("#").strip()
    child_nodes = text_to_children(cleaned_block)
    # TODO: could refactor this into a loop
    if block.startswith("######"):
        return ParentNode("h6", child_nodes)
    elif block.startswith("#####"):
        return ParentNode("h5", child_nodes)
    elif block.startswith("####"):
        return ParentNode("h4", child_nodes)
    elif block.startswith("###"):
        return ParentNode("h3", child_nodes)
    elif block.startswith("##"):
        return ParentNode("h2", child_nodes)
    else:
        return ParentNode("h1", child_nodes)


def create_code_node(block: str) -> ParentNode:
    cleaned_block = block.removeprefix("```\n").removesuffix("```")
    plain_node = text_node_to_html_node(TextNode(cleaned_block, TextType.PLAIN))
    code_node = ParentNode("code", [plain_node])
    return ParentNode("pre", [code_node]) # nest <code> inside <pre> tag


def create_quote_node(block: str) -> ParentNode:
    lines = block.splitlines()
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())
    cleaned_block = " ".join(cleaned_lines)
    child_nodes = text_to_children(cleaned_block)
    return ParentNode("blockquote", child_nodes)


def block_to_list_items(block: str, prefix_len: int) -> list[HTMLNode]:
    lines = block.splitlines()
    list_nodes = []
    for line in lines:
        cleaned_line = line[prefix_len:] # remove list prefix
        child_nodes = text_to_children(cleaned_line)
        list_nodes.append(ParentNode("li", child_nodes))
    return list_nodes


def create_ulist_node(block: str) -> ParentNode:
    list_items = block_to_list_items(block, 2)
    return ParentNode("ul", list_items)


def create_olist_node(block: str) -> ParentNode:
    list_items = block_to_list_items(block, 3)
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                child_nodes.append(create_paragraph_node(block))
            case BlockType.HEADING:
                child_nodes.append(create_heading_node(block))
            case BlockType.CODE:
                child_nodes.append(create_code_node(block))
            case BlockType.QUOTE:
                child_nodes.append(create_quote_node(block))
            case BlockType.ULIST:
                child_nodes.append(create_ulist_node(block))
            case BlockType.OLIST:
                child_nodes.append(create_olist_node(block))
            case _:
                raise ValueError("invalid block type")
    return ParentNode("div", child_nodes)
