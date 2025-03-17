import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_basic(self):
        # Test basic splitting with bold delimiters
        node = TextNode("This is text with a **bold word** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold word")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_multiple_occurrences(self):
        # Test splitting with multiple occurrences of the delimiter
        node = TextNode("This **bold** has **multiple** bold parts", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " has ")
        self.assertEqual(new_nodes[3].text, "multiple")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " bold parts")

    def test_split_with_code(self):
        # Test splitting with code delimiters
        node = TextNode("This is text with a `code block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_with_italic(self):
        # Test splitting with italic delimiters
        node = TextNode("This is text with an _italic phrase_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic phrase")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_no_delimiters(self):
        # Test when there are no delimiters in the text
        node = TextNode("This is regular text with no special formatting", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is regular text with no special formatting")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_delimiter_at_beginning(self):
        # Test with delimiter at the beginning of text
        node = TextNode("**Bold text** at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Bold text")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " at the beginning")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

    def test_delimiter_at_end(self):
        # Test with delimiter at the end of text
        node = TextNode("At the end is **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "At the end is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_multiple_nodes_input(self):
        # Test with multiple nodes in the input
        node1 = TextNode("First **bold** node", TextType.TEXT)
        node2 = TextNode("Already bold text", TextType.BOLD)
        node3 = TextNode("Second **bold** node", TextType.TEXT)
    
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
    
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "First ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " node")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "Already bold text")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, "Second ")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "bold")
        self.assertEqual(new_nodes[5].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[6].text, " node")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)

    def test_missing_closing_delimiter(self):
        # Test case where closing delimiter is missing
        node = TextNode("This has an **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_only_delimiters(self):
        # Test text that is only delimiters
        node = TextNode("**Bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_empty_content_between_delimiters(self):
        # Test empty content between delimiters
        node = TextNode("This has an empty **** bold section", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This has an empty ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " bold section")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_consecutive_delimiters(self):
        # Test consecutive delimited sections
        node = TextNode("**Bold**_Italic_", TextType.TEXT)
        # First split on bold
        intermediate_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split the result on italic
        final_nodes = split_nodes_delimiter(intermediate_nodes, "_", TextType.ITALIC)
    
        self.assertEqual(len(final_nodes), 2)
        self.assertEqual(final_nodes[0].text, "Bold")
        self.assertEqual(final_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[1].text, "Italic")
        self.assertEqual(final_nodes[1].text_type, TextType.ITALIC)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link to Google](https://www.google.com) and another [link to GitHub](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to Google", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link to GitHub", TextType.LINK, "https://github.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )