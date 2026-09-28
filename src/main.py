from textnode import TextNode, TextType


def main() -> None:
    text_node = TextNode("Sample text content", TextType.LINK, "https://www.boot.dev")
    print(text_node)


if __name__ == "__main__":
    main()
