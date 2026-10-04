from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)

        splits = []
        print(f"{node.text=}")
        split_text = node.text.split(delimiter, 2)
        print(f"{split_text=}")
        print(f"{len(split_text)}")
        if len(split_text) != 3:
            raise ValueError(f"Not valid Markdown syntax: no closing {delimiter} found.")
        splits.append(TextNode(split_text[0], TextType.PLAIN)) # Plain text before delimiter
        splits.append(TextNode(split_text[1], text_type)) # Inline text within delimiters
        splits.append(TextNode(split_text[2], TextType.PLAIN)) # Plain text after delimiter

        new_nodes.extend(splits)

    return new_nodes
