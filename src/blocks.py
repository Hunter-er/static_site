from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode # type: ignore
from textnode import TextNode, TextType # type: ignore
from inline import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes # type: ignore


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    block_list = []
    
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            block_list.append(block)

    return block_list

def block_to_blocktype(block):
    block_types = []
    
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    
    lines = block.split("\n")
    i = 1
    for line in lines:
        if line.startswith(">"):
            block_types.append(BlockType.quote)
        elif line.startswith("- "):
            block_types.append(BlockType.unordered_list)
        elif line.startswith(f"{i}. ", ):
            block_types.append(BlockType.ordered_list)
        else:
            block_types.append(BlockType.paragraph)
        i += 1

    b_type = block_types[0]
    for type in block_types:
        if type != b_type:
           b_type = BlockType.paragraph
        
    return b_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_blocktype(block)
    if block_type == BlockType.paragraph:
        return paragraph_to_html_node(block)
    if block_type == BlockType.heading:
        return heading_to_html_node(block)
    if block_type == BlockType.code:
        return code_to_html_node(block)
    if block_type == BlockType.ordered_list:
        return olist_to_html_node(block)
    if block_type == BlockType.unordered_list:
        return ulist_to_html_node(block)
    if block_type == BlockType.quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.plain)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

