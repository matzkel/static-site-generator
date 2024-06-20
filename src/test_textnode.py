import unittest

from textnode import (
    TextNode,
    TextType,
    text_to_text_nodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
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
    
    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and a [link](https://www.example.com)"
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com")
        ]
        self.assertEqual(text_to_text_nodes(text), result)

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

    def test_split_nodes_image_multiple(self):
        node = TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", TextType.TEXT)
        result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]
        self.assertEqual(split_nodes_image([node]), result)

    def test_split_nodes_image_single_node(self):
        node = TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", TextType.TEXT)
        result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_image([node]), result)

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png).", TextType.TEXT),
            TextNode("This one has ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", TextType.TEXT),
        ]
        result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(".", TextType.TEXT),
            TextNode("This one has ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), result)

    def test_split_nodes_link_multiple(self):
        node = TextNode("This is text with a [link](https://www.example.com) and [another link](https://www.google.com)", TextType.TEXT)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://www.google.com"),
        ]
        self.assertEqual(split_nodes_link([node]), result)

    def test_split_nodes_link_single_node(self):
        node = TextNode("This is text with a [link](https://www.example.com)", TextType.TEXT)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(split_nodes_link([node]), result)

    def test_split_nodes_link_multiple_nodes(self):
        nodes = [
            TextNode("This is text with a [link](https://www.example.com)", TextType.TEXT),
            TextNode("This is another text with [another link](https://www.google.com)", TextType.TEXT),
        ]
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode("This is another text with ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://www.google.com"),
        ]
        self.assertEqual(split_nodes_link(nodes), result)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com")])


if __name__ == "__main__":
    unittest.main()