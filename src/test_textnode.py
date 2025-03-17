import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC, "balls")
        node2 = TextNode("This is a text node", TextType.ITALIC, "balls")
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, "balls")
        node2 = TextNode("This is a text node", TextType.ITALIC, "http://www.url.com")
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("plain text", TextType.TEXT)
        element = text_node_to_html_node(node)
        assert element.tag == None
        assert element.value == "plain text"
        assert element.to_html() == "plain text"
    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        element = text_node_to_html_node(node)
        assert element.tag == "b"
        assert element.value == "bold text"
        assert element.to_html() == "<b>bold text</b>"
    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        element = text_node_to_html_node(node)
        assert element.tag == "i"
        assert element.value == "italic text"
        assert element.to_html() == "<i>italic text</i>"
    def test_code(self):
        node = TextNode("code snippet", TextType.CODE)
        element = text_node_to_html_node(node)
        assert element.tag == "code"
        assert element.value == "code snippet"
        assert element.to_html() == "<code>code snippet</code>"
    def test_link(self):
        node = TextNode("click here", TextType.LINK, "http://example.com")
        element = text_node_to_html_node(node)
        assert element.tag == "a"
        assert element.value == "click here"
        assert element.props["href"] == "http://example.com"
        assert element.to_html() == '<a href="http://example.com">click here</a>'
    def test_image(self):
        node = TextNode("image alt text", TextType.IMAGE, "http://example.com/image.png")
        element = text_node_to_html_node(node)
        assert element.tag == "img"
        assert element.value == ""
        assert element.props["src"] == "http://example.com/image.png"
        assert element.props["alt"] == "image alt text"
        assert element.to_html() == '<img src="http://example.com/image.png" alt="image alt text">'


if __name__ == "__main__":
    unittest.main()