
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_list = []
        if not self.props:
            return ""
        for prop_key in self.props:
            prop_list.append(f'{prop_key}="{self.props[prop_key]}"')
        join_prop = " ".join(prop_list)
        return join_prop

    
    def __repr__(self):
        return f"HTMLNode( {self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leafnode must have value")
        if self.tag == None:
            return self.value
        else:
            props = self.props_to_html()
            if props: 
                open_tag = f"<{self.tag} {props}>"
            else:
                open_tag = f"<{self.tag}>"
            return f'{open_tag}{self.value}</{self.tag}>'
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parentnode must have tag")
            # elif self.children == None:
            # raise ValueError("Parentnode must have children")
        else:
            child_html_strings = [] # Create a list
            for child in self.children:
                child_html_strings.append(child.to_html()) # Add each child's HTML to the list
            html_string = "".join(child_html_strings)
            props = self.props_to_html()
            if props: 
                open_tag = f"<{self.tag} {props}>"
            else:
                open_tag = f"<{self.tag}>"
            
            return f'{open_tag}{html_string}</{self.tag}>'