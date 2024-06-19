import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        same_node = TextNode("This is a text node", "bold")
        self.assertEqual(node, same_node)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        diff_node = TextNode("This is a different text node", "normal")
        self.assertNotEqual(node, diff_node)
    
    def test_to_html_node(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(str(text_node_to_html_node(node)), "HTMLNode('<b>', 'This is a text node')")

    def test_to_html_node_value_error(self):
        node = TextNode("This text has wrong type.", "something")
        self.assertRaises(ValueError, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()