import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_content(self):
        node = TextNode("This is a text node with content A", TextType.PLAIN)
        node2 = TextNode("This is a text node with content B", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_not_eq_empty_content(self):
        node = TextNode("", TextType.PLAIN)
        node2 = TextNode(" ", TextType.PLAIN)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
