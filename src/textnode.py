from enum import Enum
import re

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


def split_nodes_image(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes is required to be a list of TextNodes")

    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            return old_nodes

        image_tup = images[0]
        text = node.text.split(f"![{image_tup[0]}]({image_tup[1]})", maxsplit=1)
        result = []
        if text[0] != "":
            result.append(TextNode(text[0], node.text_type, node.url))
        result.append(TextNode(image_tup[0], TextType.IMAGE, image_tup[1]))
        if text[1] != "":
            result.extend(split_nodes_image(
                [TextNode(text[1], node.text_type, node.url)]
            ))
        new_nodes.extend(result)
    return new_nodes


def split_nodes_link(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes is required to be a list of TextNodes")

    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            return old_nodes

        link_tup = links[0]
        text = node.text.split(f"[{link_tup[0]}]({link_tup[1]})", maxsplit=1)
        result = []
        if text[0] != "":
            result.append(TextNode(text[0], node.text_type, node.url))
        result.append(TextNode(link_tup[0], TextType.LINK, link_tup[1]))
        if text[1] != "":
            result.extend(split_nodes_link(
                [TextNode(text[1], node.text_type, node.url)]
            ))
        new_nodes.extend(result)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


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