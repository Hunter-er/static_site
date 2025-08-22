import unittest
from blocks import markdown_to_blocks, block_to_blocktype, BlockType, markdown_to_html_node # type: ignore


class TestInlineMarkdown(unittest.TestCase):
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
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_basic(self):
        md = """# Heading

This is a paragraph
with a second line.

- Item one
- Item two
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph\nwith a second line.",
                "- Item one\n- Item two"
            ]
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        # A simple paragraph block
        block = "This is a simple paragraph."
        expected_type = BlockType.paragraph
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_heading_level_1(self):
        # A level 1 heading
        block = "# This is a heading"
        expected_type = BlockType.heading
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_code_block(self):
        # A basic code block
        block = "```\nprint('Hello, world!')\n```"
        expected_type = BlockType.code
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_quote_block_valid_multi_line(self):
        block = (
            "> This is a quoted line.\n"
            "> This is another line in the quote.\n"
            "> And a third one."
        )
        expected_type = BlockType.quote
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_quote_block_invalid_mixed_lines(self):
        # A quote block that has a non-quote line in the middle
        block = (
            "> This is a quoted line.\n"
            "This line is NOT a quote.\n"
            "> But this one is again."
        )
        # Expected behavior: It should default to a paragraph because not all lines start with '>'
        expected_type = BlockType.paragraph
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_unordered_list_valid_multi_line(self):
        block = (
            "- First item\n"
            "- Second item\n"
            "- Third item"
        )
        expected_type = BlockType.unordered_list
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_unordered_list_invalid_mixed_lines(self):
        # An unordered list that has a non-list line
        block = (
            "- First item\n"
            "This is not a list item.\n"
            "- Third item"
        )
        expected_type = BlockType.paragraph
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_ordered_list_valid(self):
        block = (
            "1. First ordered item\n"
            "2. Second ordered item\n"
            "3. Third ordered item"
        )
        expected_type = BlockType.ordered_list
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_ordered_list_invalid_not_starting_at_one(self):
        # Ordered list must start at 1
        block = (
            "2. First ordered item\n"
            "3. Second ordered item"
        )
        expected_type = BlockType.paragraph # Or whatever your fallback is if it doesn't match
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_ordered_list_invalid_skipped_number(self):
        # Ordered list numbers must increment by 1
        block = (
            "1. First ordered item\n"
            "3. Third ordered item"
        )
        expected_type = BlockType.paragraph
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_heading_too_many_hashes(self):
        # Headings should only have 1-6 '#'
        block = "####### This has too many hashes"
        expected_type = BlockType.paragraph # Or whatever your fallback is
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_heading_no_space_after_hash(self):
        # Heading must have a space after the hashes
        block = "#No space here"
        expected_type = BlockType.paragraph
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_code_block_incomplete_start(self):
        # If it starts with backticks but doesn't end with them
        block = "```\nCode block content"
        expected_type = BlockType.paragraph # Or how your function handles this.
        self.assertEqual(block_to_blocktype(block), expected_type)

    def test_code_block_incomplete_end(self):
        # If it ends with backticks but doesn't start with them
        block = "Code block content\n```"
        expected_type = BlockType.paragraph
        self.assertEqual(block_to_blocktype(block), expected_type)


    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_blocktype(block), BlockType.heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_blocktype(block), BlockType.quote)
        block = "- list\n- items"
        self.assertEqual(block_to_blocktype(block), BlockType.unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_blocktype(block), BlockType.ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_blocktype(block), BlockType.paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

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

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
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
    


if __name__ == '__main__':
    unittest.main()