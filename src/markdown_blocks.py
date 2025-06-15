from enum import Enum
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
import textwrap
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return [s.strip() for s in markdown.split("\n\n") if s.strip()]

def block_to_block_type(block):
    if bool(re.fullmatch(r'^#{1,6} .+$', block)):
        return BlockType.HEADING
    elif bool(re.fullmatch(r'^```(?!`).*?(?<!`)```$', block, re.DOTALL)):
        return BlockType.CODE
    elif all(re.fullmatch(r'^>.*$', line.strip()) for line in block.splitlines()):
        return BlockType.QUOTE
    elif all(re.fullmatch(r'^- .*$', line.strip()) for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif all(re.fullmatch(fr'^{index+1}\. .*$', line.strip()) for index, line in enumerate(block.splitlines())):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH 

def markdown_to_html_node(markdown):
    markdown = textwrap.dedent(markdown)
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in markdown_blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
       
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return children

def block_to_oneline(block):
    return re.sub(r'\n\s*', ' ', block)

def count_leading_hashes(string):
    return len(string) - len(string.lstrip('#'))

def paragraph_to_html_node(block):
    block = block_to_oneline(block)
    children = text_to_children(block)
    return ParentNode("p", children)

def heading_to_html_node(block):
    n_hashes = count_leading_hashes(block)
    block = block[n_hashes + 1:]
    children = text_to_children(block)
    return ParentNode(f"h{n_hashes}", children)

def code_to_html_node(block):
    code_text = block.lstrip('`').rstrip('`')
    code_text = code_text.lstrip()
    return ParentNode('pre', [LeafNode('code', code_text)])

def quote_to_html_node(block):
    block = block_to_oneline(block)
    quote_text = block.replace('> ', '')
    children = text_to_children(quote_text)
    return ParentNode('blockquote', children)

def ulist_to_html_node(block):
    list_items = block.replace('- ', '').split('\n')
    children = []
    for item in list_items:
        inner_children = text_to_children(item)
        children.append(ParentNode('li', inner_children))
    return ParentNode('ul', children)

def olist_to_html_node(block):
    list_items = re.sub(r'\d+\.\s', '', block).split('\n')
    children = []
    for item in list_items:
        inner_children = text_to_children(item)
        children.append(ParentNode('li', inner_children))
    return ParentNode('ol', children)