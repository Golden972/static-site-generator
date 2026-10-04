import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplit_Nodes(unittest.TestCase):
    def test_invalid_markdown_none(self):
        old_nodes = [
            TextNode("This isn't some bold text", TextType.PLAIN)
        ]
        try:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        except ValueError as e:
            self.assertEqual(
                repr(ValueError("Not valid Markdown syntax: no closing ** found.")),
                repr(e)
            )

    def test_invalid_markdown_one(self):
        old_nodes = [
            TextNode("This isn't some **bold text", TextType.PLAIN)
        ]
        try:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        except ValueError as e:
            self.assertEqual(
                repr(ValueError("Not valid Markdown syntax: no closing ** found.")),
                repr(e)
            )

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
        self.assertEqual(expected_new_nodes, actual_new_nodes)

    def test_bold_single_start(self):
        old_nodes = [
            TextNode("**Bold** at the start of this node", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("", TextType.PLAIN),
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start of this node", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(expected_new_nodes, actual_new_nodes)

    def test_bold_single_end(self):
        old_nodes = [
            TextNode("At the end of this node is some **bold text**", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("At the end of this node is some ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
            TextNode("", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(expected_new_nodes, actual_new_nodes)

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
        self.assertEqual(expected_new_nodes, actual_new_nodes)

    def test_italic_single_start(self):
        old_nodes = [
            TextNode("_italic_ at the start of this node", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" at the start of this node", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(expected_new_nodes, actual_new_nodes)

    def test_italic_single_end(self):
        old_nodes = [
            TextNode("At the end of this node is some _italic text_", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("At the end of this node is some ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode("", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(expected_new_nodes, actual_new_nodes)

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
        self.assertEqual(expected_new_nodes, actual_new_nodes)

    def test_code_single_start(self):
        old_nodes = [
            TextNode("`code` at the start of this node", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" at the start of this node", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(expected_new_nodes, actual_new_nodes)

    def test_code_single_end(self):
        old_nodes = [
            TextNode("At the end of this node is some `code text`", TextType.PLAIN)
        ]
        expected_new_nodes = [
            TextNode("At the end of this node is some ", TextType.PLAIN),
            TextNode("code text", TextType.CODE),
            TextNode("", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(expected_new_nodes, actual_new_nodes)

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
            TextNode("", TextType.PLAIN),
            TextNode("Bold", TextType.BOLD),
            TextNode(" starting text node", TextType.PLAIN),
            TextNode("This is a node that ends with ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
            TextNode("", TextType.PLAIN),
        ]
        actual_new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(expected_new_nodes, actual_new_nodes)
