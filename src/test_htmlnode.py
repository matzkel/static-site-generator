import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_type_error(self):
        node = HTMLNode()
        self.assertRaises(TypeError, node.props_to_html)

    def test_props_value_error(self):
        node = HTMLNode(props={})
        self.assertRaises(ValueError, node.props_to_html)

    def test_props(self):
        node = HTMLNode(props={
            "href": "https://google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), "href=\"https://google.com\" target=\"_blank\"")


class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode()
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("p")
        self.assertRaises(ValueError, node.to_html)

    def test_to_html(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text."),
            LeafNode(None, "Normal text."),
            LeafNode("i", "Italic text."),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text.</b>Normal text.<i>Italic text.</i></p>")

    def test_to_html_props(self):
        node = ParentNode("a", [
            LeafNode("p", "This paragraph points to google"),
            LeafNode("b", "and this bold text also points to google."),
        ], {"href": "https://google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://google.com\"><p>This paragraph points to google</p><b>and this bold text also points to google.</b></a>")

    def test_to_html_nested(self):
        node = ParentNode("p", [
            ParentNode("b", [
                ParentNode("i", [
                    LeafNode(None, "Like matryoshka!")
                ])
            ])
        ])
        self.assertEqual(node.to_html(), "<p><b><i>Like matryoshka!</i></b></p>")

    def test_to_html_nested_props(self):
        node = ParentNode("p", [
            ParentNode("a", [
                LeafNode(None, "This whole text points to the "),
                LeafNode("i", "blank page!"),
            ], {"href": "about:blank"}),
            LeafNode("b", "This bold text doesn't point to anything.")
        ])
        self.assertEqual(node.to_html(), "<p><a href=\"about:blank\">This whole text points to the <i>blank page!</i></a><b>This bold text doesn't point to anything.</b></p>")

class TestLeafNode(unittest.TestCase):
    def test_to_html_value_error(self):
        node = LeafNode()
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_no_props(self):
        node = LeafNode(tag="p", value="Lorem ipsum dolor sit amet")
        self.assertEqual(node.to_html(), "<p>Lorem ipsum dolor sit amet</p>")

    def test_to_html_props(self):
        node = LeafNode(tag="a", value="Google link", props={
            "href": "https://google.com",
        })
        self.assertEqual(node.to_html(), "<a href=\"https://google.com\">Google link</a>")


if __name__ == "__main__":
    unittest.main()