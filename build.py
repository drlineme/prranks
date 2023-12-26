""" This py build summary md from yaml files """

import os

import pandas as pd
from .utils.constants import TOPICS, SCORE_STANDARD
from .utils.yaml import get_yaml_content, find_yaml_files, save_yaml_content


def normalize_keys(profile):
    return {k.lower(): v for k, v in profile.items()}


def main(root_directory):
    """main"""
    score_data = {}
    yaml_files = find_yaml_files(root_directory)

    print(yaml_files)

    if not yaml_files:
        print("No YAML files found in the specified directory.")
        return

    for yaml_file_path in yaml_files:
        print(f"Processing {yaml_file_path} ...")
        student_id = yaml_file_path.replace("./", "").split(".")[0].upper()
        try:
            profile = normalize_keys(get_yaml_content(yaml_file_path))
            skillfound = False
            topicNOTfound = False
            for key in ["skills", "skill"]:
                if key in profile:
                    skillfound = True
                    print("Deleting outdated skill/skills ...")
                    del profile[key]
            if "topic" not in profile:
                topicNOTfound = True
                print("Adding missing topic ...")
                profile["topic"] = {topic: "A" if topic == "Learning about threat actors" else "B" for topic in TOPICS}
            if skillfound or topicNOTfound:
                save_yaml_content(yaml_file_path, profile)
        except Exception as e:
            with open(yaml_file_path, "r", encoding="utf-8") as yaml_file:
                print(f"\n*** data ***\n{yaml_file.read()}")
            print(f"*** error ***\n{e}")
            exit(1)
        score_data[student_id] = {
            "Student ID": student_id,
            **profile['topic'],
        }

    rows = []
    for key, value in score_data.items():
        row = {"Student ID": key}
        for score_item in value:
            if (
                score_item != "Student ID"
                and value[score_item] not in SCORE_STANDARD.keys()
            ):
                value[score_item] = "X"
        row.update(value)
        rows.append(row)

    df = pd.DataFrame(rows)
    df.sort_values(by=["Student ID"], inplace=True)

    # Write Score Summary
    with open("./README.md", "w+", encoding="utf-8") as markdownFile:
        markdownFile.write("### ThreatHunting202309\n")
        for item in SCORE_STANDARD:
            markdownFile.write("- {}: {}\n".format(item, SCORE_STANDARD[item]))
        markdownFile.write("\n")
        markdownFile.writelines(df.to_markdown(index=False))


if __name__ == "__main__":
    main("./")