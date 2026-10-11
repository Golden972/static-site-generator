import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.test_textnode import TestTextNode
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_bold_single_middle(self):
        old_nodes = [
            TextNode("This is some **bold text** inline", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("This is some ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
            TextNode(" inline", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_bold_single_start(self):
        old_nodes = [
            TextNode("**Bold** at the start of this node", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start of this node", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_bold_single_end(self):
        old_nodes = [
            TextNode("At the end of this node is some **bold text**", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("At the end of this node is some ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_italic_single_middle(self):
        old_nodes = [
            TextNode("This is some _italic text_ inline", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("This is some ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" inline", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_italic_single_start(self):
        old_nodes = [
            TextNode("_italic_ at the start of this node", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" at the start of this node", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_italic_single_end(self):
        old_nodes = [
            TextNode("At the end of this node is some _italic text_", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("At the end of this node is some ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_code_single_middle(self):
        old_nodes = [
            TextNode("This is some `code text` inline", TextType.PLAIN),
        ]
        expected_new_nodes = [
            TextNode("This is some ", TextType.PLAIN),
            TextNode("code text", TextType.CODE),
            TextNode(" inline", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_code_single_start(self):
        old_nodes = [
            TextNode("`code` at the start of this node", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start of this node", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_code_single_end(self):
        old_nodes = [
            TextNode("At the end of this node is some `code text`", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("At the end of this node is some ", TextType.PLAIN),
            TextNode("code text", TextType.CODE),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_bold_many(self):
        old_nodes = [
            TextNode("This is a **bold text** node", TextType.PLAIN),
            TextNode("**Bold** starting text node", TextType.PLAIN),
            TextNode("This is a node that ends with **bold text**", TextType.PLAIN),
        ]
        expected_new_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
            TextNode(" node", TextType.PLAIN),
            TextNode("Bold", TextType.BOLD),
            TextNode(" starting text node", TextType.PLAIN),
            TextNode("This is a node that ends with ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_bold_multi_inline(self):
        old_nodes = [
            TextNode("This is a **bold** text node with additional **bold** text", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text node with additional ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(expected_new_nodes, actual_new_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "this is text with a [link](https://boot.dev)"
        )
        self.assertListEqual(([("link", "https://boot.dev")]), matches)

    def test_extract_markdown_images_ignores_links(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_captures_all_matches(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and an ![additional image](https://i.imgur.com/0H106oO.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("additional image", "https://i.imgur.com/0H106oO.png"),
            ],
            matches
        )

    def test_extract_markdown_links_captures_all_matches(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and an [additional link](https://freecodecamp.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("additional link", "https://freecodecamp.org"),
            ],
            matches,
        )

    def test_extract_markdown_images_invalid_format(self):
        matches = extract_markdown_images(
            "This text ![shouldn't match]](because it's not valid markdown)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_invalid_format(self):
        matches = extract_markdown_links(
            "This text [shouldn't match]](because it's not valid markdown)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and an [additional link](https://freecodecamp.org)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("additional link", TextType.LINK, "https://freecodecamp.org"),
            ],
            new_nodes,
        )

    def test_split_images_trailing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text afterwards",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text afterwards", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_links_trailing_text(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and some text afterwards",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and some text afterwards", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_images_no_leading_text(self):
        node = TextNode(
            "![an image](https://i.imgur.com/zjjcJKZ.png) right at the start of the text",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" right at the start of the text", TextType.PLAIN),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_reverse_order(self):
        nodes = text_to_textnodes("This is text with a [link](https://boot.dev), an ![obi wan image](https://i.imgur.com/fJrm4Vk.jpeg), a `code block`, and _italic_ and **bold** text")
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(", an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJrm4Vk.jpeg"),
                TextNode(", a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(", and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple(self):
        nodes = text_to_textnodes("This is **text** with _italic_ and **bold** alternating _a few_ times with [two links](https://boot.dev) _thrown_ in the [middle](https://freecodecamp.org) **too**")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" alternating ", TextType.PLAIN),
                TextNode("a few", TextType.ITALIC),
                TextNode(" times with ", TextType.PLAIN),
                TextNode("two links", TextType.LINK, "https://boot.dev"),
                TextNode(" ", TextType.PLAIN),
                TextNode("thrown", TextType.ITALIC),
                TextNode(" in the ", TextType.PLAIN),
                TextNode("middle", TextType.LINK, "https://freecodecamp.org"),
                TextNode(" ", TextType.PLAIN),
                TextNode("too", TextType.BOLD),
            ],
            nodes
        )

    def test_text_textnodes_plain_only(self):
        nodes = text_to_textnodes("This is plain text with no inline markdown at all")
        self.assertListEqual([TextNode("This is plain text with no inline markdown at all", TextType.PLAIN)], nodes)
