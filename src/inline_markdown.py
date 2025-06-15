from textnode import TextType, TextNode
from typing import List, Tuple
import re
  
def split_nodes_delimiter(old_nodes : List[TextNode], delimiter : str, text_type : TextType) -> List[TextNode]:
    new_nodes = []
            
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:               
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Invalid Markdown Syntax")
            for i in range(len(split_text)):
                if not split_text[i]:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                elif i % 2 == 1:
                    new_nodes.append(TextNode(split_text[i], text_type))
            
    return new_nodes

def extract_markdown_images(text : str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text : str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes : List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_images(node.text)
            
            node_text = node.text
            for image_alt, image_link in extracted:
                sections = node_text.split(f"![{image_alt}]({image_link})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                node_text = sections[1]
            if node_text:
                new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes
    

def split_nodes_link(old_nodes : List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_links(node.text)
            
            node_text = node.text
            for link_anchor, link_url in extracted:
                sections = node_text.split(f"[{link_anchor}]({link_url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
                node_text = sections[1]
            if node_text:
                new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> List[TextNode]:
      node = TextNode(text, TextType.TEXT)
      text_nodes = [node]
      text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)  
      text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
      text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
      text_nodes = split_nodes_image(text_nodes)
      text_nodes = split_nodes_link(text_nodes)
      return text_nodes  
    
