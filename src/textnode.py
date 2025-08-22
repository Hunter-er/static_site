from enum import Enum

class TextType(Enum):
    plain = "plain"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        if self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url: 
            return True
        else: 
            return False

    def __repr__(self):
        return f"TextNode( {self.text}, {self.text_type.value}, {self.url})"