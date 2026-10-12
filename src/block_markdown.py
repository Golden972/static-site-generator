import re

from blocknode import BlockType


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        stripped_blocks.append(stripped_block)
    return stripped_blocks


def block_to_block_type(markdown: str) -> BlockType:
    if re.match(r"#{1,6}(?= )", markdown):
        return BlockType.HEADING
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    if re.fullmatch(r"(?:>.*(?:\n|$))+", markdown):
        return BlockType.QUOTE
    if re.fullmatch(r"(?:- .*(?:\n|$))+", markdown):
        return BlockType.ULIST
    if markdown.startswith("1. "):
        lines = markdown.split("\n")
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH
