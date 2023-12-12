import os
import json
import webbrowser
from collections import defaultdict
from github import Github, Auth
from .config import REPO_TOBE_REVIEWED
from .utilyaml import find_yaml_files, get_yaml_content, save_yaml_content
from .progress import topics_to_review
from .idnames import fidmap

# exit condition
conds = [
    (not REPO_TOBE_REVIEWED, "No repo to be reviewed, please set REPO_TOBE_REVIEWED in config.py"),
    (not os.environ.get("GITHUB_KEY"), "No GITHUB_KEY found in env, please set it first"),
]
for cond, msg in conds:
    if cond:
        print(msg)
        exit(1)

# using an access token
auth = Auth.Token(os.environ.get("GITHUB_KEY"))
g = Github(auth=auth)

# load idmap
with open(fidmap, 'r') as fr:
    student_file = json.load(fr)

# Setting review topic and criteria
rev_criteria_file = 'revcrt.json'
coauthor_file = 'coauthors.json'
topicskips_file = 'topicsk.json'
revcrt = {}
if os.path.exists(rev_criteria_file):
    with open(rev_criteria_file, 'r') as frev:
        revcrt = json.load(frev)
topicskips = {}
if os.path.exists(topicskips_file):
    with open(topicskips_file, 'r') as fskip:
        topicskips = json.load(fskip)

print('Topics with number of students below expectation:')
topics = topics_to_review()
for key, value in topics:
    print(f"{key}: {value}")

topic = input('Topic to review: ')
if topic not in revcrt:
    criteria = []
    for i in range(3):
        criteria.append(input(f'Level {i+3} critieria: '))
    revcrt[topic] = criteria
    with open(rev_criteria_file, 'w') as frev:
        json.dump(revcrt, frev, indent=2)
else:
    criteria = revcrt[topic]

# shared func
def ask(prompt, ans='yn'):
    while True:
        if ans:  # input must be in ans
            a = input(prompt).lower()
            if a in ans:
                return a
        else:  # return any input
            return input(prompt)

def sprint(body, indent=0):
    """ smart print, can indent, skip empty line, skip entire checks """
    if body:
        lines = body.split('\n')
        for i in range(len(lines)):
            line = lines[i].strip()
            if line:
                if line.startswith('###'):
                    break  # we dont want checks info
                print(f"{' '*indent}{lines[i]}")

def fprint(line, fp=None):
    """ file print """
    print(line)
    if fp:
        fp.write(line + '\n')
        fp.flush()

def save_rank(name, rank):
    sid = student_file[name]
    print(f'Searching file startswith: {sid}')
    for fn in find_yaml_files('.'):
        print(fn[2:])
        if fn[2:].upper().startswith(sid):
            studentinfo = get_yaml_content(fn)
            rankinfo = studentinfo['topic']
            if topic in rankinfo:
                rankinfo[topic] = rank
                save_yaml_content(fn, studentinfo)
                return True
    return False

# Then play with Github objects:
reviewer = g.get_user()
print('Reviewer Name:', reviewer.name)
for repo in reviewer.get_repos():
    # print(repo.name)
    if repo.name == REPO_TOBE_REVIEWED:
        # build author dict for review
        author_prs = defaultdict(list)
        coauthors = defaultdict(list)
        saved_coa = None
        if os.path.exists(coauthor_file):
            print('Loading saved coauthors ...')
            with open(coauthor_file, 'r') as fcoa:
                saved_coa = json.load(fcoa)
        if saved_coa:  # loading saved coauthors
            for k in saved_coa:
                coauthors[k] = saved_coa[k]
        for pull in repo.get_pulls(sort="updated"):
            author = pull.user.login
            author_prs[author].append(pull)
            if pull.comments:
                for c in pull.get_issue_comments():
                    coauthor = c.user.login
                    if coauthor not in [author, reviewer.login]:
                        if coauthor not in coauthors[author]:
                            coauthors[author].append(coauthor)
                #     print(f"  --- {coauthor}")
                #     sprint(c.body, indent=2)
                # print('---')
        # review loop
        print('\n\n*** Start Reviewing ***\n')
        with open('review_history.txt', 'a') as fp:
            fprint(f'*** Target topic to review [{topic}] ***', fp)
            for a in author_prs:
                for pull in author_prs[a]:
                    print('\n')
                    fprint(f'PR from author: {a}', fp)
                    print('coauthors:', coauthors[a])
                    fprint(f'#{pull.number} created at: {pull.created_at}', fp)
                    print(pull.title)
                    fprint(f'url: {pull.url}', fp)
                    print('changed:', pull.changed_files, 'comments:', pull.comments)
                    print('--- desc ---')
                    sprint(pull.body)
                    if pull.comments:
                        print('--- comments ---')
                        for c in pull.get_issue_comments():
                            coauthor = c.user.login
                            print(f"  --- {coauthor}")
                            sprint(c.body, indent=2)
                        print('---')
                    print('Eval topic=', topic)
                    print('Eval criteria:')
                    print('\n'.join(criteria))
                    webbrowser.open(pull.html_url)
                    if topic not in topicskips:
                        topicskips[topic] = []
                    if pull.number in topicskips[topic]:
                        continue
                    tbr = ask('To be reviewed? (y/n/w) ', ans='ynw')
                    if tbr == 'y':
                        rank = ask(f'Perf. Rank for author: {a} =', ans='baeo').upper()
                        comment = ask(f'Reason for rank {rank}: ', ans=None)
                        fprint(f'Saving rank[{topic}]={rank} for author: {a}, because: {comment}', fp)
                        fprint('Success!' if save_rank(a, rank) else 'Fail due to "topic" not found!', fp)
                        if coauthors[a] is None:
                            coauthors[a] = []
                        print(f'Coauthors found/loaded: {coauthors[a]}')
                        if ask('Use this list? (y/n) ') == 'n':
                            coauthors[a] = []
                        if not coauthors[a]:
                            tbe = ask('No coauthors found, manually adding them? (y/n) ')
                            if tbe.lower() == 'y':
                                while True:
                                    name = ask('Coauthor github ID (enter to exit): ', ans=None)
                                    if name:
                                        coauthors[a].append(name)
                                    else:
                                        break
                        if coauthors[a]:
                            with open(coauthor_file, 'w') as fj:
                                json.dump(coauthors, fj, indent=2)
                            for b in coauthors[a]:
                                fprint(f'Saving rank[{topic}]={rank} for coauthor: {b}, because: {comment}', fp)
                                fprint('Success!' if save_rank(b, rank) else 'Fail due to "topic" not found!', fp)
                    elif tbr == 'n':
                        fprint('SKIPPED (not the intended topic for review)', fp)
                        topicskips[topic].append(pull.number)
                        with open(topicskips_file, 'w') as fw:
                            json.dump(topicskips, fw, indent=2)
                    else:  # tbr == 'w'
                        fprint('WAIT (not ready for review)', fp)

print('\n')

# To close connections after use
g.close()
