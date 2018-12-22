from .. import board

def test_marker():
    my_board = board.Board()
    assert my_board.has_open_position()
    assert len(list(my_board.list_open_positions())) == 9

def test_row_marker():
    my_board = board.Board()
    my_board.place_marker((0, 0), 'X')
    my_board.place_marker((0, 1), 'X')
    my_board.place_marker((0, 2), 'X')
    assert my_board.is_win('X')
    assert my_board.has_open_position()

    assert len(list(my_board.list_open_positions())) == 6

def test_clear_row_marker():
    my_board = board.Board()
    my_board.place_marker((0, 0), 'X')
    my_board.place_marker((0, 1), 'X')
    my_board.place_marker((0, 2), 'X')
    my_board.clear()
    assert len(list(my_board.list_open_positions())) == 9
    my_board.place_marker((0, 1), 'X')
    my_board.place_marker((0, 0), 'O')
    my_board.place_marker((0, 2), 'X')
    my_board.place_marker((1, 1), 'O')
    my_board.place_marker((1, 0), 'X')
    my_board.place_marker((2, 2), 'O')
    assert len(list(my_board.list_open_positions())) == 3
    assert my_board.is_win('O')

def test_no_open_spots():
    my_board = board.Board()
    my_board.place_marker((0, 0), 'O')
    my_board.place_marker((0, 1), 'X')
    my_board.place_marker((0, 2), 'X')
    my_board.place_marker((1, 0), 'X')
    my_board.place_marker((1, 1), 'O')
    my_board.place_marker((1, 2), 'O')
    my_board.place_marker((2, 0), 'X')
    my_board.place_marker((2, 1), 'O')
    my_board.place_marker((2, 2), 'O')
    assert not my_board.has_open_position()
    assert not list(my_board.list_open_positions())


def test_null_encode():
    my_board = board.Board()
    assert board.Board.encode(my_board.board, 'X') == 0
