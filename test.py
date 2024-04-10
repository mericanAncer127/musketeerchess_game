import musketeerchess

board = musketeerchess.Board()

board.select_white_musteer_piece('c')
board.select_black_musteer_piece('l')

board.place_musketeer_piece('whitew', 'b')
board.place_musketeer_piece('whiteb', 'd')
board.place_musketeer_piece('blackw', 'b')
board.place_musketeer_piece('blackb', 'e')

board.push_san('Na3')#white
board.push_san('b6')#black
board.push_san('d3')#white
# board.push_san('Na6')#black
# board.push_san('Qd2')#white
# board.push_san('e6')#black
# board.push_san('e3')#white
# board.push_san('Ke7')#black

print(board)