import os
import json
from collections import defaultdict
from github import Github, Auth
from .utilyaml import find_yaml_files

faname = 'authorfs.json'
fidmap = 'idmap.json'
if not os.path.exists(faname):
    auth = Auth.Token(os.environ.get("GITHUB_KEY"))
    g = Github(auth=auth)

    author_files = defaultdict(list)
    user = g.get_user()
    print(f'User: {user.login}')
    for repo in user.get_repos():
        if repo.name == "threathunting202309":
            commits = repo.get_commits()
            for commit in commits:
                author = commit.author
                for f in commit.files:
                    if author.login not in [user.login, 'github-actions[bot]']:
                        print(f.filename, author.login)
                        author_files[author.login].append(f.filename)

    with open(faname, 'w') as fw:
        json.dump(dict(author_files), fw, indent=2)
else:
    with open(faname, 'r') as fr:
            author_files = json.load(fr)

if not os.path.exists(fidmap):
    idfname = {}
    for k in author_files:
        fs = author_files[k]
        ids = [f.split('.')[0].upper() for f in fs]
        idfname[k] = list(set(ids))[0]
        if ',' in idfname[k]:
            idfname[k] = idfname[k].split(',')[0]

    # TODO: check if idfname[k] is unique
    with open(fidmap, 'w') as fw:
        json.dump(idfname, fw, indent=2)
