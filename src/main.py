from textnode import TextNode, TextType # type: ignore
from htmlnode import HTMLNode, ParentNode, LeafNode # type: ignore

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.plain:
        new_htmlNode = LeafNode(value=text_node.text)
        return new_htmlNode
    elif text_node.text_type == TextType.bold:
        new_htmlNode = LeafNode(tag="b", value=text_node.text)
        return new_htmlNode
    elif text_node.text_type == TextType.italic:
        new_htmlNode = LeafNode(tag="i", value=text_node.text)
        return new_htmlNode
    elif text_node.text_type == TextType.code:
        new_htmlNode = LeafNode(tag="code", value=text_node.text)
        return new_htmlNode 
    elif text_node.text_type == TextType.link:
        new_htmlNode = LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        return new_htmlNode  
    elif text_node.text_type == TextType.image:
        new_htmlNode = LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
        return new_htmlNode
    else:
        raise Exception("Type is not supported")
