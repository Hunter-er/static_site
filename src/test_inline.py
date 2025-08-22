import unittest

from textnode import TextNode, TextType # type: ignore
from inline import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes # type: ignore

class TestInlineMarkdown(unittest.TestCase):
    
    def test_split_code_delimiter(self):
        # Test the basic case from the lesson
        node = TextNode("This is text with a `code block` word", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("This is text with a ", TextType.plain),
            TextNode("code block", TextType.code),
            TextNode(" word", TextType.plain),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_bold_delimiter(self):
        # Test with bold delimiters
        node = TextNode("This has **bold text** in it", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        expected = [
            TextNode("This has ", TextType.plain),
            TextNode("bold text", TextType.bold),
            TextNode(" in it", TextType.plain),
        ]
        self.assertListEqual(expected, new_nodes)   

    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode("This has `unmatched delimiter", TextType.plain)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.code)

    def test_multiple_delimiters(self):
        # Test multiple code blocks in one string
        node = TextNode("text `code1` and `code2` end", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("text ", TextType.plain),
            TextNode("code1", TextType.code),
            TextNode(" and ", TextType.plain),
            TextNode("code2", TextType.code),
            TextNode(" end", TextType.plain),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_delimiter_at_start(self):
        # Test when delimiter is at the beginning
        node = TextNode("`code` text", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("code", TextType.code),
            TextNode(" text", TextType.plain),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_delimiter_at_end(self):
        # Test when delimiter is at the end
        node = TextNode("text `code`", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("text ", TextType.plain),
            TextNode("code", TextType.code),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_mixed_node_types(self):
        # Test with a mix of node types - only plain should be split
        nodes = [
            TextNode("normal `code` text", TextType.plain),
            TextNode("already bold", TextType.bold),
            TextNode("more `code` here", TextType.plain),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.code)
        expected = [
            TextNode("normal ", TextType.plain),
            TextNode("code", TextType.code),
            TextNode(" text", TextType.plain),
            TextNode("already bold", TextType.bold),  # unchanged
            TextNode("more ", TextType.plain),
            TextNode("code", TextType.code),
            TextNode(" here", TextType.plain),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_no_delimiters(self):
        # Test text with no delimiters - should return unchanged
        node = TextNode("just plain text with no delimiters", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("just plain text with no delimiters", TextType.plain),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_empty_delimited_section(self):
        # Test what happens with empty delimited sections like ``, which creates empty strings
        node = TextNode("text `` more text", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("text ", TextType.plain),
            TextNode(" more text", TextType.plain),
        ]
        # Note: empty string should be skipped, so no TextNode("", TextType.code)
        self.assertListEqual(expected, new_nodes)

    def test_only_delimiters(self):
        # Test a string that's only delimiters
        node = TextNode("`code`", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("code", TextType.code),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_empty_input_list(self):
        # Test with empty input list
        new_nodes = split_nodes_delimiter([], "`", TextType.code)
        expected = []
        self.assertListEqual(expected, new_nodes)


class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([('to boot dev','https://www.boot.dev')], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
            TextNode("This is text with an ", TextType.plain),
            TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.plain),
            TextNode("second image", TextType.image, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes)
        
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link1](https://i.imgur.com/zjjcJKZ.png) and another [link2](https://i.imgur.com/3elNhQu.png)",
            TextType.plain,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain),
                TextNode("link1", TextType.link, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain),
                TextNode(
                    "link2", TextType.link, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
    )


    def test_text_to_textnodes(self):
        text = (
            "This is **bold** and _italic_ text with a `code block`, "
            "an ![image desc](https://img.com/img.png), "
            "and a [link title](https://link.com)."
        )
        nodes = text_to_textnodes(text)
        test = []
        for node in nodes:
            test.append(f"value: {node.text!r}, type: {node.text_type}, url: {getattr(node, 'url', None)}")

        answer = [
            "value: 'This is ', type: TextType.plain, url: None",
            "value: 'bold', type: TextType.bold, url: None",
            "value: ' and ', type: TextType.plain, url: None",
            "value: 'italic', type: TextType.italic, url: None",
            "value: ' text with a ', type: TextType.plain, url: None",
            "value: 'code block', type: TextType.code, url: None",
            "value: ', an ', type: TextType.plain, url: None",
            "value: 'image desc', type: TextType.image, url: https://img.com/img.png",
            "value: ', and a ', type: TextType.plain, url: None",
            "value: 'link title', type: TextType.link, url: https://link.com",
            "value: '.', type: TextType.plain, url: None"
        ]
        
        self.assertListEqual(answer, test)



if __name__ == "__main__":
    unittest.main()