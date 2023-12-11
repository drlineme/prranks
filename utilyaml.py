import os
import yaml

def get_yaml_content(file_path):
    with open(file_path, "r", encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)


def save_yaml_content(file_path, content, testing=False):
    if testing:
        print(f"Testing {file_path}: {content}")
        return
    with open(file_path, "w+", encoding="utf-8") as yaml_file:
        yaml.safe_dump(content, yaml_file, encoding='utf-8', allow_unicode=True, default_flow_style=False, sort_keys=False)


def find_yaml_files(root_dir):
    """process all yamls"""
    yaml_files = []
    for item in os.listdir(root_dir):
        if os.path.isfile(os.path.join(root_dir, item)):
            if item.endswith(".yaml") or item.endswith(".yml"):
                yaml_files.append(os.path.join(root_dir, item))
    return yaml_files
