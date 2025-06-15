from textnode import TextNode, TextType
from file_utils import copy_to_dir
from generate_page import generate_pages_recursive
import os

def main():
    current_dir = os.getcwd()
    static_path = os.path.join(current_dir, "static")
    public_path = os.path.join(current_dir, "public")

    copy_to_dir(static_path, public_path)
    content_path = os.path.join(current_dir, "content")
    template_path = os.path.join(current_dir, "template.html")
    public_path = os.path.join(current_dir, 'public')
    generate_pages_recursive(content_path, template_path, public_path)

main()