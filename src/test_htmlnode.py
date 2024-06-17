import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()