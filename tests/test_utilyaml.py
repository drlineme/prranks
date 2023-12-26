import os
import pytest
from ..utils.yaml import find_yaml_files, get_yaml_content, save_yaml_content


def test_find_get_save_yaml_files():
    alist = find_yaml_files('.')
    assert len(alist) > 0
    content = None
    for x in alist:
        print(x)
        content = get_yaml_content(x)
    save_yaml_content('test.yaml', content, testing=True)
    save_yaml_content('test.yaml', content, testing=False)
    os.remove('test.yaml')
