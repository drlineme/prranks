from collections import defaultdict
from .utils.yaml import find_yaml_files, get_yaml_content

def topics_to_review(meta, root_directory):
    ranks = defaultdict(int)
    for fn in find_yaml_files('.'):
        info: dict = get_yaml_content(fn)
        topic = info if meta['flat'] else info['topic']
        # print(fn, topic)
        for k, v in topic.items():
            # print(k, v)
            if v in ['B', 'b']:
                ranks[k] += 1

    return sorted(ranks.items(), key=lambda x: x[1])


if __name__ == "__main__":
    import json
    fpath = input("Path to JSON config file (default: config): ") or 'config'
    with open(fpath + '.json', 'r') as f:
        metadata = json.load(f)
        print('Loaded metadata:', metadata.keys())

    for k, v in topics_to_review(metadata, "./"):
        print(k, 'missing', v, 'submission(s)')
