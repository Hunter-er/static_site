from textnode import TextNode, TextType # type: ignore
from htmlnode import LeafNode # type: ignore
import re

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.plain:
        new_htmlNode = LeafNode(value=text_node.text)
        return new_htmlNode
    elif text_node.text_type == TextType.bold:
        new_htmlNode = LeafNode(tag="b", value=text_node.text)
        return new_htmlNode
    elif text_node.text_type == TextType.italic:
        new_htmlNode = LeafNode(tag="i", value=text_node.text)
        return new_htmlNode
    elif text_node.text_type == TextType.code:
        new_htmlNode = LeafNode(tag="code", value=text_node.text)
        return new_htmlNode 
    elif text_node.text_type == TextType.link:
        new_htmlNode = LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        return new_htmlNode  
    elif text_node.text_type == TextType.image:
        new_htmlNode = LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
        return new_htmlNode
    else:
        raise Exception("Type is not supported")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.plain:
            node_list = old_node.text.split(delimiter)
            if len(node_list) %2 == 0:
                raise Exception("Invalid markdown syntax: unmatched delimiter")
            node_index = 0
            while node_index < len(node_list):
                if node_index % 2 == 0:
                    if node_list[node_index] != "":
                        newest_node = TextNode(node_list[node_index], TextType.plain)
                        new_nodes.append(newest_node)

                else:
                    if node_list[node_index] != "":
                        newest_node = TextNode(node_list[node_index], text_type)
                        new_nodes.append(newest_node)
                
                node_index += 1

        else:
            new_nodes.append(old_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:

        # FIRST CHECK: Is this node NOT a plain text node?
        if old_node.text_type is not TextType.plain:
            # If it's not plain text, just add it to the new_nodes list (assuming its text is not empty)
            if old_node.text != "": # This check is good
                new_nodes.append(old_node)
            # Then, you're done with this old_node, move to the next one in the loop
            continue # This helps clarify flow

        # ELSE: If we reach here, it means old_node.text_type *IS* TextType.plain
        # NOW we apply the splitting logic for plain text nodes that might contain images.
        if old_node.text == "": # Handle empty string for plain text nodes
            continue # Skip to next old_node if text is empty

        extracted_values = extract_markdown_images(old_node.text)

        if not extracted_values: # Scenario 1: No images found in this plain text node
            new_nodes.append(old_node) # Append the original plain text node as is
            continue # Move to the next old_node in the main loop

        # Scenario 2: Images ARE found! Proceed with complex splitting logic.
        temp_nodes_for_this_node = []
        current_text_to_process = old_node.text # Start with the full text

        for alt_text, url in extracted_values:
            image_markdown_delimiter = f"![{alt_text}]({url})"
            parts = current_text_to_process.split(image_markdown_delimiter, 1)

            if parts[0]:
                temp_nodes_for_this_node.append(TextNode(parts[0], TextType.plain))

            temp_nodes_for_this_node.append(TextNode(alt_text, TextType.image, url))

            current_text_to_process = parts[1]

        if current_text_to_process:
            temp_nodes_for_this_node.append(TextNode(current_text_to_process, TextType.plain))

        new_nodes.extend(temp_nodes_for_this_node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:

        # FIRST CHECK: Is this node NOT a plain text node?
        if old_node.text_type is not TextType.plain:
            # If it's not plain text, just add it to the new_nodes list (assuming its text is not empty)
            if old_node.text != "": # This check is good
                new_nodes.append(old_node)
            # Then, you're done with this old_node, move to the next one in the loop
            continue # This helps clarify flow

        # ELSE: If we reach here, it means old_node.text_type *IS* TextType.plain
        # NOW we apply the splitting logic for plain text nodes that might contain images.
        if old_node.text == "": # Handle empty string for plain text nodes
            continue # Skip to next old_node if text is empty

        extracted_values = extract_markdown_links(old_node.text)

        if not extracted_values: # Scenario 1: No images found in this plain text node
            new_nodes.append(old_node) # Append the original plain text node as is
            continue # Move to the next old_node in the main loop

        # Scenario 2: Images ARE found! Proceed with complex splitting logic.
        temp_nodes_for_this_node = []
        current_text_to_process = old_node.text # Start with the full text

        for link_text, url in extracted_values:
            link_markdown_delimiter = f"[{link_text}]({url})"
            parts = current_text_to_process.split(link_markdown_delimiter, 1)

            if parts[0]:
                temp_nodes_for_this_node.append(TextNode(parts[0], TextType.plain))

            temp_nodes_for_this_node.append(TextNode(link_text, TextType.link, url))

            current_text_to_process = parts[1]

        if current_text_to_process:
            temp_nodes_for_this_node.append(TextNode(current_text_to_process, TextType.plain))

        new_nodes.extend(temp_nodes_for_this_node)

    return new_nodes

def text_to_textnodes(text):
    orig_node = TextNode(text,TextType.plain)
    textnodes_list = [orig_node]
    simple_text_type = [TextType.bold, TextType.italic, TextType.code]
    simple_text_delim = ["**", "_", "`"]
    i = 0
    # bold/italic/code
    for text_type in simple_text_type:
        temp_textnodes_list = []
        for textnode in textnodes_list:
            temp_textnodes_list.extend(split_nodes_delimiter([textnode], simple_text_delim[i], text_type))
        i += 1
        textnodes_list = (temp_textnodes_list)
    
    #link
    temp_textnodes_list = []
    for textnode in textnodes_list:
        temp_textnodes_list.extend(split_nodes_link([textnode]))
    textnodes_list = temp_textnodes_list
    #image
    temp_textnodes_list = []
    for textnode in textnodes_list:
        temp_textnodes_list.extend(split_nodes_image([textnode]))
    textnodes_list = temp_textnodes_list

    return textnodes_list
