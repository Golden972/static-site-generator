import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="boot.dev", props={"href": "https://boot.dev", "target": "_blank"})
        test_string = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), test_string)
        self.assertNotEqual(node.props_to_html(), "shouldn't equal this string")

    def test_eq_props_to_html(self):
        node = HTMLNode(tag="p", value="This is a HTML node", props={"class": "centered"})
        node2 = HTMLNode(tag="section", props={"class": "centered"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_not_eq_props_to_html(self):
        node = HTMLNode(tag="p", value="This is a HTML node", props={"class": "centered"})
        node2 = HTMLNode(tag="section", props={"id": "gift-card"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())
