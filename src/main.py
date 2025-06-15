from textnode import TextNode, TextType
from file_utils import copy_to_dir
from generate_page import generate_pages_recursive
import os
import sys

def main(args):
    if len(args) > 1:
        basepath = args[1]
    else:
        basepath = '/'
    current_dir = os.getcwd()
    static_path = os.path.join(current_dir, "static")
    docs_path = os.path.join(current_dir, "docs")

    copy_to_dir(static_path, docs_path)
    content_path = os.path.join(current_dir, "content")
    template_path = os.path.join(current_dir, "template.html")
    generate_pages_recursive(content_path, template_path, docs_path, basepath)

if __name__ == '__main__':
    main(sys.argv)