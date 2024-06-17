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
            raise TypeError("props must be a dictionary")
        if not self.props:
            raise ValueError("props dictionary must be populated")

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