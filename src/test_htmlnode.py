import unittest

from htmlnode import (
    BlockType,
    HTMLNode,
    ParentNode,
    LeafNode,
    markdown_to_html_node,
    block_to_block_type,
    markdown_to_blocks,
)


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
    
    def markdown_to_html_node(self):
        markdown = '''
        #### This is heading
        This is **bolded** paragraph
        \n
        This is another paragraph with *italic* text and `code` here\n
        This is the same paragraph on a new line\n
        ```This is a code block```\n
        >This is a quote from someone\n
        ```This is actually just a paragraph\n
        \n
        * This is a list
        * with items
        '''
        self.assertEqual(markdown_to_html_node(markdown), ParentNode("div", [
            LeafNode("h4", "This is heading"),
            LeafNode("p", "This is **bolded** paragraph"),
            LeafNode("p", "This is another paragraph with *italic* text and `code` here"),
            LeafNode("p", "This is the same paragraph on a new line"),
            ParentNode("pre", [
                LeafNode("code", "This is a code block"),
            ]),
            LeafNode("quoteblock", "This is a quote from someone"),
            LeafNode("p", "```this is actually just a paragraph"),
            ParentNode("ul", [
                LeafNode("li", "This is a list"),
                LeafNode("li", "with items")
            ])
        ]))

    def test_block_to_block_type_heading(self):
        block = "#### Heading!"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_invalid(self):
        block = "```not a code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_to_blocks(self):
        markdown = '''
        This is **bolded** paragraph
        \n
        This is another paragraph with *italic* text and `code` here\n
        This is the same paragraph on a new line\n
        \n
        * This is a list
        * with items
        '''
        
        result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here",
            "This is the same paragraph on a new line",
            "* This is a list",
            "* with items",
        ]
        self.assertEqual(markdown_to_blocks(markdown), result)


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