import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode # type: ignore


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode(tag="h1", value="Title", children=["child"], props={"id": "main"})
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Title")
        self.assertEqual(node.children, ["child"])
        self.assertEqual(node.props, {"id": "main"})

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="nope")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        out = node.props_to_html()
        # Props order is not guaranteed in a dict, so check both variants:
        expected_variants = [
            'href="https://boot.dev" target="_blank"',
            'target="_blank" href="https://boot.dev"'
        ]
        self.assertIn(out, expected_variants)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_tag(self):
        node = LeafNode("p", "Hello, world!")
        answer = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), answer)
    
    def test_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        answer = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), answer)
    
    def test_basic(self):
        node = LeafNode(None, "Just text!")
        answer = "Just text!"
        self.assertEqual(node.to_html(), answer)
        
    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()