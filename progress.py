from collections import defaultdict
from .utilyaml import find_yaml_files, get_yaml_content
from .config import BELOW_STANDARD

def topics_to_review():
    ranks = defaultdict(int)
    for fn in find_yaml_files('.'):
        info: dict = get_yaml_content(fn)
        for k, v in info['topic'].items():
            if v.upper() in BELOW_STANDARD:
                ranks[k] += 1

    return sorted(ranks.items(), key=lambda x: x[1])
