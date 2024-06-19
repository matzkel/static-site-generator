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