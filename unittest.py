import os
import pytest

fpath = os.path.abspath(__file__)
dname = os.path.join(os.path.dirname(fpath), 'tests')
print('PATH of unit tests:', dname)
pytest.main(['--import-mode=importlib', '-sx', dname])
