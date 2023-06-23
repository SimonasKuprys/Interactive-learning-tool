from interactive_learning_tool import percentage_counter

def test_percentage_counter():
    assert percentage_counter(10, 0) == 100
    assert percentage_counter(0, 10) == 0
    assert percentage_counter(7, 3) == 70
    assert percentage_counter(0, 0) == 0
    assert percentage_counter(1, 0) == 100
    assert percentage_counter(0, 1) == 0
    assert percentage_counter(1000000, 500000) == 67