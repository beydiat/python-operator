from operations import add, sub, div, puis

def test_operations():
    assert add(1, 2) == 3
    assert sub(2, 1) == 1
    assert div(10, 2) == 5
    assert div(3, 0) == 0
    assert puis(2,4) == 16 
