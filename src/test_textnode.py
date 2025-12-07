import unittest

from textnode import TextNode, TextType, BlockType
from htmlnode import LeafNode, HTMLNode, ParentNode
from helper import *


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

    def test_split_nodes_image_basic(self):
        node = TextNode("Here is an ![alt](url.jpg) image", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url.jpg"),
            TextNode(" image", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode("![img1](url1.jpg) and ![img2](url2.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("Just text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_split_nodes_image_non_text(self):
        node = TextNode("bold", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_split_nodes_image_at_start(self):
        node = TextNode("![alt](url.jpg) text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "url.jpg"),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_at_end(self):
        node = TextNode("text ![alt](url.jpg)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url.jpg")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_basic(self):
        node = TextNode("Here is a [link](url.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode("[link1](url1) and [link2](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("Just text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_split_nodes_link_non_text(self):
        node = TextNode("bold", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_split_nodes_link_at_start(self):
        node = TextNode("[link](url.com) text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_at_end(self):
        node = TextNode("text [link](url.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "Just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_italic(self):
        text = "This is *italic* text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_image(self):
        text = "Here is an ![alt](url.jpg) image"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url.jpg"),
            TextNode(" image", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_link(self):
        text = "Here is a [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_bold_italic(self):
        text = "This is **bold** and *italic* text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_all_delimiters(self):
        text = "**Bold** and *italic* with `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_with_images_links(self):
        text = "Check this ![image](img.jpg) and [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_complex(self):
        text = "This is **bold**, *italic*, `code`, ![image](img.jpg) and [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com")
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_basic(self):
        markdown = "This is the first block\n\nThis is the second block\n\nThis is the third block"
        result = markdown_to_blocks(markdown)
        expected = ["This is the first block", "This is the second block", "This is the third block"]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_single_block(self):
        markdown = "This is a single block"
        result = markdown_to_blocks(markdown)
        expected = ["This is a single block"]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_whitespace_only(self):
        markdown = "   \n\n  \n\n   "
        result = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_strips_whitespace(self):
        markdown = "  First block  \n\n  Second block  \n\n  Third block  "
        result = markdown_to_blocks(markdown)
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_multiple_empty_lines(self):
        markdown = "First block\n\n\n\nSecond block\n\n\n\n\nThird block"
        result = markdown_to_blocks(markdown)
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_leading_trailing_empty(self):
        markdown = "\n\nFirst block\n\nSecond block\n\n"
        result = markdown_to_blocks(markdown)
        expected = ["First block", "Second block"]
        self.assertEqual(result, expected)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_no_space(self):
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```python\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_code_no_end(self):
        block = "```python\nprint('hello')"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_quote_no_space(self):
        block = ">This is not a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_dash(self):
        block = "- This is a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_asterisk(self):
        block = "* This is a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_no_space(self):
        block = "-This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_9(self):
        block = "9. This is a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_10(self):
        block = "10. This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_no_space(self):
        block = "1.This is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        block = "This is just a regular paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_markdown_to_html_node_single_paragraph(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "p")

    def test_markdown_to_html_node_multiple_paragraphs(self):
        markdown = "First paragraph.\n\nSecond paragraph."
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 2)
        for child in result.children:
            self.assertIsInstance(child, ParentNode)
            self.assertEqual(child.tag, "p")

    def test_markdown_to_html_node_heading(self):
        markdown = "# Main Heading"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "h1")

    def test_markdown_to_html_node_multiple_headings(self):
        markdown = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "h2")
        self.assertEqual(result.children[2].tag, "h3")

    def test_markdown_to_html_node_code_block(self):
        markdown = "```\ncode block\n```"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "pre")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertEqual(result.children[0].children[0].tag, "code")

    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "blockquote")

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "ul")
        self.assertEqual(len(result.children[0].children), 3)
        for item in result.children[0].children:
            self.assertEqual(item.tag, "li")

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "ol")
        self.assertEqual(len(result.children[0].children), 3)
        for item in result.children[0].children:
            self.assertEqual(item.tag, "li")

    def test_markdown_to_html_node_mixed_content(self):
        markdown = "# Title\n\nSome paragraph text.\n\n- List item 1\n- List item 2"
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "ul")

    def test_markdown_to_html_node_empty(self):
        markdown = ""
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 0)

    def test_markdown_to_html_node_complex_document(self):
        markdown = """# Welcome to My Site

This is an introduction paragraph with **bold** and *italic* text.

## Features

Here are some features:

- Feature 1
- Feature 2
- Feature 3

### Code Example

```
def hello():
    print("Hello, World!")
```

> This is a blockquote
> with multiple lines

1. First step
2. Second step
3. Third step

Final paragraph."""
        result = markdown_to_html_node(markdown)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 10)  # h1, p, h2, p, ul, h3, pre, blockquote, ol, p
        expected_tags = ["h1", "p", "h2", "p", "ul", "h3", "pre", "blockquote", "ol", "p"]
        for i, child in enumerate(result.children):
            self.assertEqual(child.tag, expected_tags[i])

    def test_extract_title_basic(self):
        markdown = "# Hello World\n\nThis is content."
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_with_whitespace(self):
        markdown = "#   Hello World   \n\nThis is content."
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_middle_of_document(self):
        markdown = "Some intro text\n\n# Main Title\n\nMore content\n\n## Subtitle"
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")

    def test_extract_title_special_characters(self):
        markdown = "# Title with 123 & Special !@# Characters"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with 123 & Special !@# Characters")

    def test_extract_title_no_title(self):
        markdown = "This is just content\n\nNo title here\n\n## This is not a title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")

    def test_extract_title_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")

    def test_extract_title_only_other_headings(self):
        markdown = "## Subtitle\n\n### Sub-subtitle\n\n#### Another heading"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")

    def test_extract_title_multiple_hash_not_title(self):
        markdown = "### Not a title\n\n# Real Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Real Title")

    def test_extract_title_hash_without_space(self):
        markdown = "#Not a title\n\n# Real Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Real Title")




if __name__ == "__main__":
    unittest.main()