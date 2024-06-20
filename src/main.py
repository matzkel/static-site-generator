import os
import shutil


def main():
    copy_r("./static")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as file:
        markdown = file.read()
    template = ""
    with open(template_path) as file:
        template = file.read()
    



def copy_r(directory):
    if not os.path.exists(directory):
        raise ValueError("directory doesn't exist")
    
    if directory == "/static":
        if not os.path.exists("./public"):
            os.mkdir("./public")
        else:
            shutil.rmtree("./public")
            os.mkdir("./public")

    files = os.listdir(directory)
    for file in files:
        path = os.path.join(directory, file)
        if os.path.isfile(path):
            shutil.copy(path, "./public")
        else:
            copy_r(path)


if __name__ == "__main__":
    main()