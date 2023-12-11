from collections import defaultdict
from .utilyaml import find_yaml_files, get_yaml_content

def topics_to_review():
    ranks = defaultdict(int)
    for fn in find_yaml_files('.'):
        info: dict = get_yaml_content(fn)
        for k, v in info['topic'].items():
            if v in ['B', 'b']:
                ranks[k] += 1

    return sorted(ranks.items(), key=lambda x: x[1])
