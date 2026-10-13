import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# This is a heading one

## This is a heading two

### This is a heading three

#### This is a heading four

##### This is a heading five

###### This is a heading six
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading one</h1><h2>This is a heading two</h2><h3>This is a heading three</h3><h4>This is a heading four</h4><h5>This is a heading five</h5><h6>This is a heading six</h6></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is a quote
> with some **bold** text
> as well as some
>
> _-- italic text_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with some <b>bold</b> text as well as some  <i>-- italic text</i></blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- This is an unordered list
- with some **bold** text
- as well as some
- _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>with some <b>bold</b> text</li><li>as well as some</li><li><i>italic</i> text</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. with some **bold** text
3. as well as some
4. _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>with some <b>bold</b> text</li><li>as well as some</li><li><i>italic</i> text</li></ol></div>"
        )

    def test_headings_with_paragraphs(self):
        md = """
# This is a heading one

this is a paragraph with some **bold** text

## this is a heading two

this is a paragraph with some _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading one</h1><p>this is a paragraph with some <b>bold</b> text</p><h2>this is a heading two</h2><p>this is a paragraph with some <i>italic</i> text</p></div>"
        )


if __name__ == "__main__":
    unittest.main()
