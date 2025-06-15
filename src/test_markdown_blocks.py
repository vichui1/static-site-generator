import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is a paragraph






"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
            ],
        )
    
    def test_markdown_to_blocks_remove_whitespace(self):
        md = """
                           This is a paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)   
    
    def test_block_to_block_type_code(self):
        block = """``` this is code
        
        ```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
      
    def test_block_to_block_type_quote(self):
        block = """>This
        >is
        >a
        >quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- This
        - is
        - a
        - unordered_list"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = """1. This
        2. is
        3. a
        4. quote"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_md_to_html_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_md_to_html_heading(self):
        md = """
    # This is a heading
    
    #### This is also a heading
    
    ####### This is not a heading
    
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h4>This is also a heading</h4><p>####### This is not a heading</p></div>"
        )
        
    def test_md_to_html_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_md_to_html_quotes(self):
        md = """
    > This is part
    > of
    > a
    > **quote**
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is part of a <b>quote</b></blockquote></div>"
        )
    
    def test_md_to_html_ulist(self):
        md = """
        - this is an
        - unordered
        - list, with a **bold** word
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is an</li><li>unordered</li><li>list, with a <b>bold</b> word</li></ul></div>"
        )

    def test_md_to_html_plist(self):
        md = """
        1. this is an
        2. ordered
        3. list, with a **bold** word
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is an</li><li>ordered</li><li>list, with a <b>bold</b> word</li></ol></div>"
        )
    
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
if __name__ == "__main__":
    unittest.main()