from enum import Enum

from textnode import TextType, text_to_text_nodes


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # Without a tag will render as raw text
        self.value = value # Without a value will be assumed to have children
        self.children = children # Without children will be assumed to have value
        self.props = props # Without props simply won't have any attributes
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not isinstance(self.props, dict):
            raise TypeError("props is required to be a dictionary")
        if not self.props:
            raise ValueError("props is required to be populated")

        result = ""
        for key, value in self.props.items():
            result += f"{key}=\"{value}\" "
        return result.rstrip()

    def __repr__(self):
        result = ""
        if self.tag:
            result += f"'<{self.tag}>', "
        if self.value:
            result += f"'{self.value}', "
        if self.children:
            result += f"{self.children}, "
        if self.props:
            result += f"{self.props_to_html()}"
        result = result.rstrip()

        if result[-1] == ",":
            result = result[:-1]

        return f"HTMLNode({result})"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children:
            raise ValueError("children is required to be populated")

        result = ""
        for child in self.children:
            result += child.to_html()

        if not self.props:
            return f"<{self.tag}>{result}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{result}</{self.tag}>"
            

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("value is required")
            
        if not self.tag:
            return self.value

        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # Might have bugs if count excedes 6
        if BlockType.HEADING:
            count = 0
            for ch in block:
                if ch == "#":
                    count += 1
                elif ch == " ":
                    break
            if count > 6:
                count = 6

            text_nodes = text_to_text_nodes(block[count + 1:])
            heading = ParentNode(f"h{count}", [])
            for text_node in text_nodes:
                heading.children.append(text_node_to_html_node(text_node))
            children.append(heading)

        elif BlockType.CODE:
            text_nodes = text_to_text_nodes(block[3:-3])
            code_block = ParentNode("pre", [
                ParentNode("code", [])
            ])
            for text_node in text_nodes:
                code_block.children[0].children.append(text_node_to_html_node(text_node))
            children.append(code_block)

        elif BlockType.QUOTE:
            text_nodes = text_to_text_nodes(block[1:])
            quote = ParentNode("blockquote", [])
            for text_node in text_nodes:
                quote.children.append(text_node_to_html_node(text_node))
            children.append(quote)
            
        elif BlockType.UNORDERED_LIST:
            text_nodes = text_to_text_nodes(block[2:])
            if children[-1].tag == "ul":
                point = ParentNode("li", [])
                for text_node in text_nodes:
                    point.children.append(text_node_to_html_node(text_node))
                children[-1].children.append(point)
            else:
                point = ParentNode("ul", [
                    ParentNode("li", [])
                ])
                for text_node in text_nodes:
                    point.children.children(text_node_to_html_node(text_node))
                children.append(point)
                
        # Won't work if ordered list goes beyond single digits
        elif BlockType.ORDERED_LIST:
            text_nodes = text_to_text_nodes(block[2:])
            if children[-1].tag == "ol":
                point = ParentNode("li", [])
                for text_node in text_nodes:
                    point.children.append(text_node_to_html_node(text_node))
                children[-1].children.append(point)
            else:
                point = ParentNode("ul", [
                    ParentNode("li", [])
                ])
                for text_node in text_nodes:
                    point.children.children(text_node_to_html_node(text_node))
                children.append(point)

        elif BlockType.PARAGRAPH:
            text_nodes = text_to_text_nodes(block)
            paragraph = ParentNode("p", [])
            for text_node in text_nodes:
                paragraph.children.append(text_node_to_html_node(text_node))
            children.append(paragraph)
    return ParentNode("div", children)


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("* ") or block.startswith("- "):
        return BlockType.UNORDERED_LIST
    # Won't work if ordered list goes beyond single digits
    elif block[0].isdigit() and block[1].startswith("."):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    result = [x.strip() for x in markdown.split("\n")]
    return [x for x in filter(lambda x: x != "", result)]


def extract_title(markdown):
    title = markdown_to_blocks(markdown)[0]
    if title.startswith("# "):
        return title[2:]
    else:
        raise Exception("h1 header is required")


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