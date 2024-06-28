import os
import shutil

from htmlnode import markdown_to_html_node, extract_title

def main():
    copy_r("./static")
    generate_pages_r("./static", "./static/template.html", "./public")


def generate_pages_r(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError("dir_path_content doesn't exist")
    if not os.path.exists(template_path):
        raise ValueError("template_path doesn't exist")
    if not os.path.exists(dest_dir_path):
        raise ValueError("dest_dir_path doesn't exist")

    files = os.listdir(dir_path_content)
    for file in files:
        path = os.path.join(dir_path_content, file)
        if os.path.isfile(path) and file.endswith(".md"):
            generate_page(path, template_path, dest_dir_path)
        elif os.path.isdir(path):
            if "content" not in path:
                dest_path = os.path.join(dest_dir_path, file)
                generate_pages_r(path, template_path, dest_path)
            else:
                generate_pages_r(path, template_path, dest_dir_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as file:
        markdown = file.read()
    template = ""
    with open(template_path) as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    file_name = from_path.split("/")[-1][:-3] + ".html"
    with open(os.path.join(dest_path, file_name), "w") as file:
        file.write(result)


def copy_r(directory):
    if not os.path.exists(directory):
        raise ValueError("directory doesn't exist")
    
    if directory == "./static":
        if not os.path.exists("./public"):
            os.mkdir("./public")
        else:
            shutil.rmtree("./public")
            os.mkdir("./public")
    else:
        temp = directory.replace("static", "public")
        if not os.path.exists(temp):
            os.mkdir(temp)

    files = os.listdir(directory)
    for file in files:
        path = os.path.join(directory, file)
        if os.path.isfile(path):
            shutil.copy(path, path.replace("static", "public"))
        else:
            copy_r(path)


if __name__ == "__main__":
    main()