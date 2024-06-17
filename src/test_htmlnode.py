import unittest

from htmlnode import HTMLNode, LeafNode


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