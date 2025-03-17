import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode(props=None)  
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
        
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "link"
            }
        )
        result = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertIn(' class="link"', result)
        self.assertEqual(len(result.split()), 3)

    def test_constructor_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr_method(self):
        node = HTMLNode("p", "Hello, world!", None, {"class": "text"})
        repr_result = repr(node)
        self.assertIn("HTMLNode", repr_result)
        self.assertIn("p", repr_result)
        self.assertIn("Hello, world!", repr_result)
        self.assertIn("class", repr_result)

def test_to_html_raises_error(self):
    node = HTMLNode()
    with self.assertRaises(NotImplementedError):
        node.to_html()


def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")