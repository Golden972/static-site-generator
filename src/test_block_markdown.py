import unittest

from block_markdown import markdown_to_blocks


class test_block_markdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_markdown_to_blocks_extra_newlines_and_spaces(self):
        md = """
  This is **bolded** paragraph





 This is another paragraph after excessive newlines and spaces which should be ignored


     - This is a list
- with items, after an excessive newline and spaces which should be ignored
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph after excessive newlines and spaces which should be ignored",
                "- This is a list\n- with items, after an excessive newline and spaces which should be ignored"
            ],
            blocks,
        )


if __name__ == "__main__":
    unittest.main()
