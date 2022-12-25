import pytest
from operations import add, subs

def test_operations():
    assert add(1, 2) == 3
    assert subs(2, 1) == 1
