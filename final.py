from .utils.yaml import get_yaml_content, find_yaml_files
from .utils.uio import uniq_file, fprint

tracking_id = ""  # tracking some student id? show debug info for that student


def score(meta, root_directory):
    def convert(score):
        return meta['scoremap'][score]

    topics = meta["topics"]
    flat = meta["flat"]
    yaml_files = find_yaml_files(root_directory)
    for cond, msg in [
        (not yaml_files, "No YAML files found in the specified directory."),
        (not topics, "No topics found in the specified JSON file."),]:
        if cond:
            print(msg)
            return

    scores = []
    for yaml_file_path in yaml_files:
        student_id = yaml_file_path.replace("./", "").split(".")[0].upper()
        profile = get_yaml_content(yaml_file_path)
        if flat:
            topic = profile
            name = student_id
        else:
            name = profile["name"]
            topic = profile["topic"]
        score_sum = 0
        for t in topic:
            score_sum += convert(topic[t])
            if student_id == tracking_id:
                print(t, convert(topic[t]))
        scores.append([student_id, name, score_sum/len(topic)])
        if student_id == tracking_id:
            print(len(topic), score_sum/len(topic))

    if not tracking_id:
        bonus = int(input("Bonus points? ") or "0")
        scores.sort(key=lambda x: x[0], reverse=True)
        prefix = meta.get("final",{}).get("prefix", "") or 'final'
        postfix = meta.get("final",{}).get("postfix", "") or '.txt'
        with uniq_file(prefix, postfix) as f:
            for id, name, score in scores:
                score += bonus
                # print(id, name, score)
                id = id.split(',')[0]
                if flat:
                    fprint("{:<10} {:.2f}".format(id, score), f)
                else:
                    fprint("{:<10} {:.2f} {:<40}".format(id, score, name), f)


if __name__ == "__main__":
    import json
    fpath = input("Path to JSON config file (default: config): ") or 'config'
    with open(fpath + '.json', 'r') as f:
        metadata = json.load(f)
        print('Loaded metadata:', metadata.keys())

    score(metadata, "./")
