import unittest

from block_markdown import block_to_block_type, markdown_to_blocks
from blocknode import BlockType


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

    def test_block_to_block_type_heading_one(self):
        blocks = markdown_to_blocks("# Heading One")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_two(self):
        blocks = markdown_to_blocks("## Heading Two")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_three(self):
        blocks = markdown_to_blocks("### Heading Three")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_four(self):
        blocks = markdown_to_blocks("#### Heading Four")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_five(self):
        blocks = markdown_to_blocks("##### Heading Five")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_six(self):
        blocks = markdown_to_blocks("###### Heading Six")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_not_valid_heading(self):
        blocks = markdown_to_blocks("####### Not a heading")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_not_valid_heading_no_space(self):
        blocks = markdown_to_blocks("#Not a heading")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_code(self):
        blocks = markdown_to_blocks('```\nprint("Hello, world!")\n```')
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_not_valid_code(self):
        blocks = markdown_to_blocks('```print("Hello, world!")\n```')
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_not_valid_code_no_closing(self):
        blocks = markdown_to_blocks('```\nprint("Hello, world!")\n')
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_quote(self):
        blocks = markdown_to_blocks("""
> This is
> a markdown
> quote block
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_quote_no_space(self):
        blocks = markdown_to_blocks("""
> This is
>still a valid
> markdown quote block
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_not_valid_quote(self):
        blocks = markdown_to_blocks("""
> This is
no longer a
> valid markdown quote block
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_ulist(self):
        blocks = markdown_to_blocks("""
- This is
- an unordered
- markdown list
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.ULIST, block_type)

    def test_block_to_block_type_not_valid_ulist(self):
        blocks = markdown_to_blocks("""
- This is
-not a valid
- markdown list
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_olist(self):
        blocks = markdown_to_blocks("""
1. This is
2. an ordered
3. markdown list
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.OLIST, block_type)

    def test_block_to_block_type_olist_no_space(self):
        blocks = markdown_to_blocks("""
1. This is
2.not a valid
3. ordered markdown list
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_olist_out_of_order(self):
        blocks = markdown_to_blocks("""
1. This is
3. not in the correct
2. order, and is invalid
""")
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(BlockType.PARAGRAPH, block_type)


if __name__ == "__main__":
    unittest.main()
