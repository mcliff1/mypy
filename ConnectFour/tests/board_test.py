from .. import board

def test_marker():
    my_board = board.Board()
    assert my_board.has_open_position()
    assert len(list(my_board.list_open_positions())) == 64
