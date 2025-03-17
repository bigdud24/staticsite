class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)
    def to_html(self):
        if self.tag == "img":
            html = f"<{self.tag}{self.props_to_html()}>"
            print(f"DEBUG: to_html() generated HTML: {html}")
            return html
        if not self.tag:
            return str(self.value)
        html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        print(f"DEBUG: to_html() generated HTML: {html}")
        return html
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if not self.tag:
            raise ValueError("no tag value")
        if not self.children:
            raise ValueError("no children value")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"