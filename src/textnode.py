from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        if self.url:
            return f"TextNode('{self.text}', {self.text_type}, '{self.url}')"
        return f"TextNode('{self.text}', {self.text_type})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes is required to be a list of TextNodes")
    if not isinstance(delimiter, str):
        raise TypeError("delimiter is required to be a string")
    if not delimiter:
        raise ValueError("delimiter is required")
    if not isinstance(text_type, TextType):
        raise TypeError("text_type is required to be of appropriate value")

    new_nodes = []
    for node in old_nodes:
        # TODO: Fix bug when bold symbol is being confused as italic sentence
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax, missing closing delimiter?")
        elif node.text.count(delimiter) == 0:
            return old_nodes

        text = node.text.split(delimiter, maxsplit=2)   
        result = []
        if text[0] != "":
            result.append(TextNode(text[0], node.text_type, node.url))
        result.append(TextNode(text[1], text_type, node.url))
        if text[2] != "":
            result.extend(split_nodes_delimiter(
                [TextNode(text[2], node.text_type, node.url)],
                delimiter,
                text_type
            ))
        new_nodes.extend(result)

    return new_nodes


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise TypeError("text_node.text_type is required to be of appropriate value")