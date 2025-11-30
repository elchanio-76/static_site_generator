
from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: Enum, url: str = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type.value == other.text_type.value and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html_node(self):
        from htmlnode import LeafNode
        
        if self.text_type == TextType.PLAIN:
            return LeafNode(None, self.text)
        if self.text_type == TextType.BOLD:
            return LeafNode("b", self.text)
        if self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text)
        if self.text_type == TextType.CODE:
            return LeafNode("code", self.text)
        if self.text_type == TextType.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        if self.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": self.url, "alt": self.text})
        raise ValueError(f"Invalid text type: {self.text_type}")