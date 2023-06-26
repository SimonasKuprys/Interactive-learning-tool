from interactive_learning_tool import percentage_counter,Reader

def test_button():
    button = Button("2")
    button.number("3")
    assert button.number == "3"
    

def test_percentage_counter():
    assert percentage_counter(10, 0) == 100
    assert percentage_counter(0, 10) == 0
    assert percentage_counter(7, 3) == 70
    assert percentage_counter(0, 0) == 0
    assert percentage_counter(1, 0) == 100
    assert percentage_counter(0, 1) == 0
    assert percentage_counter(1000000, 500000) == 67
    
def test_read_file():
    try:
        all_info = Reader.read_file()
        assert isinstance(all_info, list)
        assert len(all_info) > 0
        assert all(isinstance(row, dict) for row in all_info)
    except FileNotFoundError:
        print("File does not exist.")