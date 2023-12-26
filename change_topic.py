""" This py build summary md from yaml files """

import os

import pandas as pd
from .utils.yaml import get_yaml_content, find_yaml_files, save_yaml_content
from .build import TOPICS, normalize_keys


def main(root_directory):
    """main"""
    for i, key in enumerate(TOPICS):
        print(i, key)
    ti = input("Topic index to change: ")
    tt = TOPICS[int(ti)]
    nn = input("New topic name: ")
    yaml_files = find_yaml_files(root_directory)

    print(yaml_files)

    if not yaml_files:
        print("No YAML files found in the specified directory.")
        return

    for yaml_file_path in yaml_files:
        print(f"Processing {yaml_file_path} ...")
        try:
            profile = normalize_keys(get_yaml_content(yaml_file_path))
            topicChanged = False
            if tt in profile["topic"]:
                if nn:
                    profile["topic"][nn] = profile["topic"][tt]
                    del profile["topic"][tt]
                else:
                    del profile["topic"][tt]
                topicChanged = True
            if topicChanged:
                save_yaml_content(yaml_file_path, profile)
        except Exception as e:
            with open(yaml_file_path, "r", encoding="utf-8") as yaml_file:
                print(f"\n*** data ***\n{yaml_file.read()}")
            print(f"*** error ***\n{e}")
            exit(1)


if __name__ == "__main__":
    main("./")