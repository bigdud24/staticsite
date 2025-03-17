from textnode import TextNode, TextType
from regex import *

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        remaining_text = text
        while delimiter in remaining_text:
            start_idx = remaining_text.find(delimiter)
            text_before = remaining_text[:start_idx]
            end_idx = remaining_text.find(delimiter, start_idx + len(delimiter))
            if end_idx == -1:
                raise Exception(f"No closing delimiter found for {delimiter}")
            text_between = remaining_text[start_idx + len(delimiter):end_idx]
            remaining_text = remaining_text[end_idx + len(delimiter):]
            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            new_nodes.append(TextNode(text_between, text_type))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link_text, url in links:
            link_markdown = f"[{link_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes