import os

# shared func
def ask(prompt, ans='yn'):
    while True:
        if ans:  # input must be in ans
            a = input(prompt).lower()
            if a in ans:
                return a
        else:  # return any input
            return input(prompt)


def multiple_choice(choices: list):
    for i, key in enumerate(choices):
        print(i+1, key)
    targets = []
    while True:
        ti = input("Index number to choose (0 for all, enter to end): ")
        if ti == '':
            break
        if ti == '0':
            targets = choices
            break
        targets.append(choices[int(ti)-1])
    return targets


def sprint(body, indent=0, skip_empty=True, skip_mark="###"):
    """ smart print, with indent, skip empty line, skip all after skip_mark """
    if body:
        lines = body.split('\n')
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith(skip_mark):
                    break  # skip everything after
            if line or not skip_empty:
                print(f"{' '*indent}{lines[i]}")


def fprint(line, fp=None):
    """ file print """
    print(line)
    if fp:
        fp.write(line + '\n')
        fp.flush()


def uniq_file(prefix, suffix, mode='w'):
    """ create a unique file """
    i = 0
    while True:
        i += 1
        fname = f"{prefix}{i}{suffix}"
        if not os.path.exists(fname):
            return open(fname, mode)
