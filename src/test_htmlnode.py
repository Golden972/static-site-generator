import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_values(self):
        node = HTMLNode("span", "cool text")
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "cool text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("label", "Email:", props={"for": "email"})
        test_string = "HTMLNode: tag=label, value=Email:, children=None, props={'for': 'email'}"
        self.assertEqual(repr(node), test_string)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        test_string = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), test_string)

    def test_leaf_to_html_a_props(self):
        node = LeafNode("a", "boot.dev", {"href": "https://boot.dev", "id": "boot-dev-link"})
        test_string = '<a href="https://boot.dev" id="boot-dev-link">boot.dev</a>'
        self.assertEqual(node.to_html(), test_string)

    def test_plain_text(self):
        node = LeafNode(None, "this is raw text")
        test_string = "this is raw text"
        self.assertEqual(node.to_html(), test_string)

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a leaf node", {"class": "leafy"})
        test_string = "LeafNode: tag=p, value=This is a leaf node, props={'class': 'leafy'}"
        self.assertEqual(repr(node), test_string)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        test_string = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), test_string)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        test_string = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), test_string)

    def test_to_html_with_branching_children_and_props(self):
        left_grandchild_node = LeafNode("label", "Full Name:", {"for": "name"})
        left_child_node = ParentNode("fieldset", [left_grandchild_node], {"class": "attention"})
        right_grandchild_node1 = LeafNode("b", "beware!")
        right_grandchild_node2 = LeafNode("i", "spoilers ahead")
        right_child_node = ParentNode("p", [right_grandchild_node1, right_grandchild_node2])
        parent_node = ParentNode("section", [left_child_node, right_child_node], {"id": "introduction"})
        test_string = (
            '<section id="introduction"><fieldset class="attention"><label for="name">Full Name:</label></fieldset><p><b>beware!</b><i>spoilers ahead</i></p></section>'
        )
        self.assertEqual(parent_node.to_html(), test_string)

    def test_parent_repr(self):
        child_node = LeafNode("p", "This is a child node")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        test_string = (
            "ParentNode: tag=div, children=[LeafNode: tag=p, value=This is a child node, props=None], props={'class': 'container'}"
        )
        self.assertEqual(repr(parent_node), test_string)


if __name__ == "__main__":
    unittest.main()
