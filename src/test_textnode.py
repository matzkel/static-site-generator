import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        same_node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, same_node)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        diff_node = TextNode("This is a different text node", "normal")
        self.assertNotEqual(node, diff_node)
    
    def test_split_nodes_diff_delimiters(self):
        node = TextNode("This text has `code block` and **bold sentence**.", TextType.TEXT)
        result = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and **bold sentence**.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), result)

    def test_split_nodes_no_delimiters(self):
        node = TextNode("Just a **bold sentence**.", TextType.TEXT)
        result = [TextNode("Just a **bold sentence**.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.ITALIC), result)

    def test_split_nodes_single_node(self):
        node = TextNode("This is text with a `code block` word.", TextType.TEXT)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), result)

    def test_split_nodes_multiple_nodes(self):
        nodes = [
            TextNode("This is an *italic* text!", TextType.TEXT),
            TextNode("*This one is it's continuation!*", TextType.TEXT),
        ]
        result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text!", TextType.TEXT),
            TextNode("This one is it's continuation!", TextType.ITALIC),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.ITALIC), result)

    def test_split_nodes_missing_delimiter(self):
        node = TextNode("This one doesn't **have closing delimiter!", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_to_html_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(text_node_to_html_node(node)), "HTMLNode('<b>', 'This is a text node')")

    def test_to_html_node_value_error(self):
        node = TextNode("This text has wrong type.", "something")
        self.assertRaises(TypeError, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()