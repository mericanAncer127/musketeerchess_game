import musketeerchess
import musketeerchess.pgn as pgn


board = musketeerchess.Board()
game = pgn.Game()

game.headers["Event"] = "Example Game"
game.headers["Date"] = "2024.04.18"
game.headers["White"] = "PlayerW"
game.headers["Black"] = "PlayerB"

game.setup(board)
board.select_white_musteer_piece('l')
board.select_black_musteer_piece('c')

board.place_musketeer_piece('whitew', 'd')
board.place_musketeer_piece('whiteb', 'f')
board.place_musketeer_piece('blackw', 'c')
board.place_musketeer_piece('blackb', 'f')

board.push_san('d4')#white
board.push_san('d6')#black

board.push_san('Qd3')#white
board.push_san('Bg4')#black

board.push_san('g3')#white
board.push_san('g5')#black

board.push_san('Bh3')#white
board.push_san('Bh6')#black

board.push_san('Cf5')#white
board.push_san('Cg6')#black

board.push_san('Lb3')#white
board.push_san('Lb6')#black

print(board)
pgn_string = game.accept_musketeer(pgn.StringExporter(headers=False), 'c', 'l', 'b', 'd', 'b', 'e')
# print(game)

print(game)
# print('pgn', pgn_string)
