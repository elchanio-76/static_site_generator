import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node3 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        node4 = TextNode("This is some anchor text", TextType.ITALIC, "https://www.boot.dev")
        node5 = TextNode("This is some anchor text", TextType.ITALIC)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node1)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)

    def test_to_html_node(self):
        # Test PLAIN text type
        plain_node = TextNode("Hello world", TextType.PLAIN)
        plain_html = plain_node.to_html_node()
        self.assertIsInstance(plain_html, LeafNode)
        self.assertEqual(plain_html.tag, None)
        self.assertEqual(plain_html.value, "Hello world")
        self.assertEqual(plain_html.props, None)
        
        # Test BOLD text type
        bold_node = TextNode("Bold text", TextType.BOLD)
        bold_html = bold_node.to_html_node()
        self.assertIsInstance(bold_html, LeafNode)
        self.assertEqual(bold_html.tag, "b")
        self.assertEqual(bold_html.value, "Bold text")
        self.assertEqual(bold_html.props, None)
        
        # Test ITALIC text type
        italic_node = TextNode("Italic text", TextType.ITALIC)
        italic_html = italic_node.to_html_node()
        self.assertIsInstance(italic_html, LeafNode)
        self.assertEqual(italic_html.tag, "i")
        self.assertEqual(italic_html.value, "Italic text")
        self.assertEqual(italic_html.props, None)
        
        # Test CODE text type
        code_node = TextNode("console.log()", TextType.CODE)
        code_html = code_node.to_html_node()
        self.assertIsInstance(code_html, LeafNode)
        self.assertEqual(code_html.tag, "code")
        self.assertEqual(code_html.value, "console.log()")
        self.assertEqual(code_html.props, None)
        
        # Test LINK text type
        link_node = TextNode("Click here", TextType.LINK, "https://example.com")
        link_html = link_node.to_html_node()
        self.assertIsInstance(link_html, LeafNode)
        self.assertEqual(link_html.tag, "a")
        self.assertEqual(link_html.value, "Click here")
        self.assertEqual(link_html.props, {"href": "https://example.com"})
        
        # Test IMAGE text type
        image_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        image_html = image_node.to_html_node()
        self.assertIsInstance(image_html, LeafNode)
        self.assertEqual(image_html.tag, "img")
        self.assertEqual(image_html.value, "")
        self.assertEqual(image_html.props, {"src": "https://example.com/image.png", "alt": "Alt text"})
        
        # Test invalid text type error handling
        # Create a node with an invalid text type by manually setting the text_type
        invalid_node = TextNode("test", TextType.PLAIN)
        invalid_node.text_type = "invalid_type"  # Set to invalid value
        with self.assertRaises(ValueError):
            invalid_node.to_html_node()




if __name__ == "__main__":
    unittest.main()