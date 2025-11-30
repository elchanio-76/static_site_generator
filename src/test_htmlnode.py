# Test suite for HTMLNode class
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_props(self):
        node = HTMLNode("div", "Hello, world!", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_constructor_all_params(self):
        node = HTMLNode("p", "Hello", ["child1", "child2"], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"class": "text"})

    def test_constructor_minimal(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_constructor_partial_params(self):
        node = HTMLNode("span", "text")
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode("div", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting"})
        expected = 'HTMLNode(div, Hello, world!, children:None, props: {\'class\': \'greeting\'})'
        self.assertEqual(repr(node), expected)

    def test_str(self):
        node = HTMLNode("span", "text", ["child"], {"id": "test"})
        expected = 'HTMLNode(span, text, children:[\'child\'], props: {\'id\': \'test\'})'
        self.assertEqual(str(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")

    def test_str(self):
        node = LeafNode("span", "text", {"id": "test"})
        self.assertEqual(str(node), "LeafNode(span, text, {'id': 'test'})")


class TestParentNode(unittest.TestCase):
    def test_constructor_all_params(self):
        children = [LeafNode("span", "child1"), LeafNode("p", "child2")]
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)
        self.assertIsNone(node.value)

    def test_constructor_minimal(self):
        node = ParentNode("div", [LeafNode("span", "child")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertIsNone(node.props)
        self.assertIsNone(node.value)

    def test_constructor_with_props_only(self):
        props = {"class": "wrapper"}
        node = ParentNode("section", [LeafNode("p", "text")], props)
        self.assertEqual(node.tag, "section")
        self.assertEqual(node.props, props)

    def test_constructor_tag_only(self):
        node = ParentNode("article", [])
        self.assertEqual(node.tag, "article")
        self.assertEqual(node.children, [])

    def test_to_html(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        children = [
            LeafNode("h1", "Title"),
            LeafNode("p", "First paragraph"),
            LeafNode("p", "Second paragraph")
        ]
        parent_node = ParentNode("div", children)
        expected = "<div><h1>Title</h1><p>First paragraph</p><p>Second paragraph</p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_nested_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [ParentNode("p", [child_node])])
        self.assertEqual(parent_node.to_html(), "<div><p><span>child</span></p></div>")

    def test_to_html_with_mixed_children_types(self):
        leaf_child = LeafNode("b", "bold text")
        parent_child = ParentNode("span", [LeafNode("i", "italic text")])
        grandparent_node = ParentNode("div", [leaf_child, parent_child])
        expected = "<div><b>bold text</b><span><i>italic text</i></span></div>"
        self.assertEqual(grandparent_node.to_html(), expected)

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "text"})
        self.assertEqual(parent_node.to_html(), '<div class="text"><span>child</span></div>')

    def test_to_html_with_multiple_props(self):
        child_node = LeafNode("a", "link")
        props = {"href": "https://example.com", "class": "external", "target": "_blank"}
        parent_node = ParentNode("div", [child_node], props)
        expected = '<div href="https://example.com" class="external" target="_blank"><a>link</a></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node]).to_html()

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

    def test_to_html_deeply_nested_structure(self):
        # Create a 4-level deep nesting
        great_grandchild = LeafNode("code", "deep code")
        great_grandparent = ParentNode("pre", [great_grandchild])
        grandparent = ParentNode("div", [great_grandparent])
        parent = ParentNode("section", [grandparent])
        root = ParentNode("body", [parent])
        
        expected = "<body><section><div><pre><code>deep code</code></pre></div></section></body>"
        self.assertEqual(root.to_html(), expected)

    def test_to_html_sibling_parent_nodes(self):
        # Test multiple parent nodes at the same level
        left_parent = ParentNode("div", [LeafNode("p", "Left content")], {"class": "left"})
        right_parent = ParentNode("div", [LeafNode("p", "Right content")], {"class": "right"})
        container = ParentNode("main", [left_parent, right_parent])
        
        expected = '<main><div class="left"><p>Left content</p></div><div class="right"><p>Right content</p></div></main>'
        self.assertEqual(container.to_html(), expected)

    def test_repr(self):
        children = [LeafNode("span", "child")]
        props = {"class": "container"}
        node = ParentNode("div", children, props)
        expected = "ParentNode(div, children: [LeafNode(span, child, None)], {'class': 'container'})"
        self.assertEqual(repr(node), expected)

    def test_repr_minimal(self):
        node = ParentNode("article", [])
        expected = "ParentNode(article, children: [], None)"
        self.assertEqual(repr(node), expected)

    def test_repr_no_props(self):
        children = [LeafNode("p", "text")]
        node = ParentNode("section", children)
        expected = "ParentNode(section, children: [LeafNode(p, text, None)], None)"
        self.assertEqual(repr(node), expected)

    def test_str(self):
        children = [LeafNode("span", "child")]
        props = {"id": "main"}
        node = ParentNode("div", children, props)
        expected = "ParentNode(div, children: [LeafNode(span, child, None)], {'id': 'main'})"
        self.assertEqual(str(node), expected)

