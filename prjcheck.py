import os
import json
import webbrowser
from collections import defaultdict
from github import Github, Auth
from .utils.constants import PROJECTS_TOBE_REVIEWED, RETRO_KEYS, SECURITY_KEYS
from .utils.uio import sprint, fprint, ask
from .utils.yaml import find_yaml_files, get_yaml_content, save_yaml_content
from .utils import gitapi

# Exit condition
conds = [
    (not PROJECTS_TOBE_REVIEWED, "No projects to be reviewed, please set PROJECTS_TOBE_REVIEWED in config.py"),
    (not os.environ.get("GITHUB_KEY"), "No GITHUB_KEY found in env, please set it first"),
]
for cond, msg in conds:
    if cond:
        print(msg)
        exit(1)

# Using an access token
auth = Auth.Token(os.environ.get("GITHUB_KEY"))
g = Github(auth=auth)

for prj in PROJECTS_TOBE_REVIEWED:
    # Then play with Github objects:
    tname, trepo = prj.split('/')
    print(f"\nProcessing {tname}/{trepo} ...")
    tuser = g.get_user(tname)
    repo = tuser.get_repo(trepo)

    # Iterate through open pull requests
    if True:
        score = 0
        for pull_request in repo.get_pulls(state='closed'):
            # Check if the pull request has been reviewed
            reviews = pull_request.get_reviews()
            if reviews.totalCount > 1:
                score += 1
                print(f"Pull Request #{pull_request.number} has been peer-reviewed ({reviews.totalCount}).")
            else:
                print(f"Pull Request #{pull_request.number} is pending peer review ({reviews.totalCount}).")
        print('PR Review Score:', score)

    # Check if spikes
    if True:
        score = 0
        for issue in repo.get_issues(state='closed'):
            if 'spike' in issue.title.lower():
                score += 1
                print(f"Issue #{issue.number}: #{issue.title} is a spike.")
        print('Spike Score:', score)

    # Check if retro and security discussions
    if True:
        score = 0
        sscore = 0
        for title in gitapi.get_discussion_titles(tname, trepo, os.environ.get("GITHUB_KEY")):
            print(title)
            if any(x in title.upper() for x in RETRO_KEYS):
                score += 1
            if any(x in title.upper() for x in SECURITY_KEYS):
                sscore += 1
        print('Retro discussion Score:', score)
        print('Security discussion Score:', score)

    # check if SECURITY.md exists
    if True:
        if gitapi.check_file_existence(tname, trepo, 'SECURITY.md', os.environ.get("GITHUB_KEY")):
            print('SECURITY.md exists')
        else:
            print('SECURITY.md does not exist')

    # check if milestone exists
    if True:
        if repo.get_milestone(1):
            print('Milestone exists')
        else:
            print('Milestone does not exist')


# To close connections after use
g.close()
