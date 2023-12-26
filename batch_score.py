""" General scoring of topics for a given directory of YAML file """

import json
from .utils.yaml import get_yaml_content, find_yaml_files, save_yaml_content
from .utils.uio import multiple_choice


def score(meta, root_directory):
    topics = meta["topics"]
    yaml_files = find_yaml_files(root_directory)
    for cond, msg in [
        (not yaml_files, "No YAML files found in the specified directory."),
        (not topics, "No topics found in the specified JSON file."),]:
        if cond:
            print(msg)
            return

    # select topics to score
    print("Select topics to score:")
    topic_indices = multiple_choice(topics)
    print('Selected topics:', topic_indices)

    # select yamls to score
    print("Select YAMLs to score:")
    yaml_indices = multiple_choice(yaml_files)
    print('Selected YAMLs:', yaml_indices)

    # score
    score = input("Score to add (O, E, A, B, U or topic_name to copy score): ")
    if len(score) == 1:
        score = score.upper()  # O, E, A, B, U
    for yaml_file_path in yaml_indices:
        print(f"Processing {yaml_file_path} ...")
        try:
            profile = get_yaml_content(yaml_file_path)
            topics = profile if meta['flat'] else profile["topic"]
            for topic in topic_indices:
                if topic in topics:
                    if len(score) == 1:
                        topics[topic] = score
                    elif score in topics:
                        scoremap = meta['scoremap']
                        if scoremap[topics[score]] > scoremap[topics[topic]]:
                            topics[topic] = topics[score]
                    else:
                        print(f"Topic {score} not found in {yaml_file_path}.")
                else:
                    print(f"Topic {topic} not found in {yaml_file_path}.")
            save_yaml_content(yaml_file_path, profile)
        except Exception as e:
            print(f"*** error ***\n{e}\n***\n")
            continue


if __name__ == "__main__":
    fpath = input("Path to JSON config file (default: config): ") or 'config'
    with open(fpath + '.json', 'r') as f:
        metadata = json.load(f)
        print('Loaded metadata:', metadata.keys())

    score(metadata, "./")
