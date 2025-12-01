import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from helper import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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
        # Test TEXT text type
        TEXT_node = TextNode("Hello world", TextType.TEXT)
        TEXT_html = TEXT_node.to_html_node()
        self.assertIsInstance(TEXT_html, LeafNode)
        self.assertEqual(TEXT_html.tag, None)
        self.assertEqual(TEXT_html.value, "Hello world")
        self.assertEqual(TEXT_html.props, None)
        
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
        invalid_node = TextNode("test", TextType.TEXT)
        invalid_node.text_type = "invalid_type"  # Set to invalid value
        with self.assertRaises(ValueError):
            invalid_node.to_html_node()
            
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("Hello **bold** world", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("Hello **bold** and **italic** world", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.BOLD),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("Hello **bold world", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_non_text_node(self):
        node = TextNode("bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_split_nodes_delimiter_empty_sections(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("Hello world", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("Hello **bold**", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("**italic** world", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("link", TextType.LINK, "url"),
            TextNode("italic", TextType.BOLD),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    def test_split_nodes_delimiter_italics(self):
        node = TextNode("Hello _italic_ world", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("Hello `code` world", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_code_block(self):
        node = TextNode("Hello ```code block``` world", TextType.TEXT)
        result = split_nodes_delimiter([node], "```", TextType.CODE)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    def test_extract_markdown_images_basic(self):
        text = "![alt text](image.jpg)"
        result = extract_markdown_images(text)
        expected = [("alt text", "image.jpg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        text = "![img1](url1.jpg) and ![img2](url2.png)"
        result = extract_markdown_images(text)
        expected = [("img1", "url1.jpg"), ("img2", "url2.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_no_images(self):
        text = "Just some text without images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_empty_alt(self):
        text = "![](image.jpg)"
        result = extract_markdown_images(text)
        expected = [("", "image.jpg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_empty_url(self):
        text = "![alt]()"
        result = extract_markdown_images(text)
        expected = [("alt", "")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_special_chars(self):
        text = "![alt with spaces](url-with-dashes_and_underscores.jpg)"
        result = extract_markdown_images(text)
        expected = [("alt with spaces", "url-with-dashes_and_underscores.jpg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_malformed(self):
        text = "[not an image](url.jpg) ![missing bracket](url.png ![alt](url.jpg"
        result = extract_markdown_images(text)
        # Only properly formed images should match
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_links_basic(self):
        text = "[link text](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("link text", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        text = "[link1](url1) and [link2](url2)"
        result = extract_markdown_links(text)
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_links(self):
        text = "Just some text without links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_with_images(self):
        text = "![image](img.jpg) [link](url.com)"
        result = extract_markdown_links(text)
        expected = [("link", "url.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty_text(self):
        text = "[](url.com)"
        result = extract_markdown_links(text)
        expected = [("", "url.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty_url(self):
        text = "[text]()"
        result = extract_markdown_links(text)
        expected = [("text", "")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_special_chars(self):
        text = "[text with spaces](url-with-dashes_and_underscores.com)"
        result = extract_markdown_links(text)
        expected = [("text with spaces", "url-with-dashes_and_underscores.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_malformed(self):
        text = "(not a link) [missing bracket](url.com [text](url.com"
        result = extract_markdown_links(text)
        # Only properly formed links should match
        expected = []
        self.assertEqual(result, expected)




if __name__ == "__main__":
    unittest.main()