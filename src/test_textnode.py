import unittest

from textnode import TextNode, TextType # type: ignore
from main import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("TEXT NODE!!!", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.italic)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_neq_nolink(self):
        node = TextNode("This is a text node", TextType.bold, "google.com")
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_neq_link(self):
        node = TextNode("This is a text node", TextType.bold, "google.com")
        node2 = TextNode("This is a text node", TextType.bold, "yahoo.com")
        self.assertNotEqual(node, node2)   



class TestTesttoHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.plain)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("Strong", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Strong")
        self.assertEqual(html_node.props, None)  # If your LeafNode defaults to None

    def test_italic(self):
        node = TextNode("slanted", TextType.italic)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "slanted")
        self.assertEqual(html_node.props, None)  # if default is None

    def test_code(self):
        node = TextNode("print('hi')", TextType.code)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Google", TextType.link, url="https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("A bear", TextType.image, url="bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "bear.png", "alt": "A bear"})

    def test_invalid_type(self):
        with self.assertRaises(Exception):
            node = TextNode("oops", None)
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()