from markdown_blocks import markdown_to_html_node
import os


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        entry_dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry_path) and entry_path.endswith(".md"):
            entry_dest_path = entry_dest_path.removesuffix(".md") + ".html"
            generate_page(entry_path, template_path, entry_dest_path, basepath)
        else:
            generate_pages_recursive(
                entry_path, template_path, entry_dest_path, basepath
            )


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = read_file(from_path)
    template_content = read_file(template_path)
    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    html_content = (
        template_content.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_string)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)
    write_file(dest_path, html_content)


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except Exception as e:
        print(f"An error occured: {e}")
        raise e


def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line.lstrip("# ")
    raise ValueError("markdown doesn't contain a h1 heading")
