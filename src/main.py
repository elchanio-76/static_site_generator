from helper import generate_page
import os


def copy_static_to_public(source_dir: str = None, target_dir: str = None):
    import shutil
    import os
    if not source_dir:
        source_dir = "./static"
    if not target_dir:
        target_dir = "./public"
    
    # check if paths are within project workspace
    if not os.path.abspath(source_dir).startswith(os.path.abspath(os.getcwd())):
        raise ValueError("Source directory is not within the project workspace")
    if not os.path.abspath(target_dir).startswith(os.path.abspath(os.getcwd())):
        raise ValueError("Target directory is not within the project workspace")
    
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    shutil.copytree(source_dir, target_dir)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    # Check that path is within workspace directory
    if not os.path.abspath(dir_path_content).startswith(os.path.abspath(os.getcwd())):
        raise ValueError("Source directory is not within the project workspace")
    if not os.path.abspath(dest_dir_path).startswith(os.path.abspath(os.getcwd())):
        raise ValueError("Destination directory is not within the project workspace")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for file in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, file)):
            # If the file is an .md file generate the page
            if file.endswith(".md"):
                html_file = file.replace(".md", ".html")
                generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, html_file))
        else:
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))

def main():
    copy_static_to_public()
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == '__main__':
    main()