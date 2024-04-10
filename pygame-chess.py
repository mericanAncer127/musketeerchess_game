import musketeerchess
import pygame
from pygame.locals import *
import random
import time
from stockfish import Stockfish
import math
from utils import Utils


# Intialize Pygame instances
pygame.init()
pygame.display.set_caption('pygame-musketeerchess')

board = musketeerchess.Board()
board_color = [(118,150,86), (238,238,210), (188, 203, 74), (245, 245, 138),  (238, 120, 74), (200, 245, 68)]
board_size = 60 * 8
buffer = []
square_size = board_size / 8
screen = pygame.display.set_mode((board_size, board_size * 10 / 8))
game_clock = pygame.time.Clock()
menu_showed = False # flag select muskteerpieces menu
position_selected = False # flag select places
selected_musketeer = None

def get_coordinate_from_index(board_index) -> (int, int): 
   row = math.ceil(board_index / 8)
   col = board_index - ((row - 1) * 8) 
   return (row - 1, col - 1)

def show_piece(current_piece, row, col):
   current_piece_path = "resources/pieces/"
   if current_piece.symbol().islower(): current_piece_path = current_piece_path + current_piece.symbol()
   else: current_piece_path = current_piece_path + 'w' + current_piece.symbol().lower()
   current_piece_path = current_piece_path + ".png"
   current_piece_png = pygame.image.load(current_piece_path)
   current_piece_png = pygame.transform.scale(current_piece_png, (square_size, square_size))
   screen.blit(current_piece_png, (col * square_size, (row + 1) * square_size))

def place_musketeer_pieces():
   if board.musketeer_unlaunched['whitew'] and board.musketeer_pieces['white']:
      piece = musketeerchess.Piece(board.musketeer_pieces['white'], musketeerchess.WHITE)
      if board.musketeer_columns['whitew']:
         current_square = get_coordinate_from_index(board.musketeer_columns['whitew'] + 1)
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)
      else:
         current_square = get_coordinate_from_index(40) # h4
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)

   if board.musketeer_unlaunched['whiteb'] and board.musketeer_pieces['black']:
      piece = musketeerchess.Piece(board.musketeer_pieces['black'], musketeerchess.WHITE)
      if board.musketeer_columns['whiteb']:
         current_square = get_coordinate_from_index(board.musketeer_columns['whiteb'] + 1)
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)
      else:
         current_square = get_coordinate_from_index(32) # h3
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)

   if board.musketeer_unlaunched['blackw'] and board.musketeer_pieces['white']:
      piece = musketeerchess.Piece(board.musketeer_pieces['white'], musketeerchess.BLACK)
      if board.musketeer_columns['blackw']:
         current_square = get_coordinate_from_index(72 + board.musketeer_columns['blackw'] + 1)
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)
      else:
         current_square = get_coordinate_from_index(49) # a6
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)

   if board.musketeer_unlaunched['blackb'] and board.musketeer_pieces['black']:
      piece = musketeerchess.Piece(board.musketeer_pieces['black'], musketeerchess.BLACK)
      if board.musketeer_columns['blackb']:
         current_square = get_coordinate_from_index(72 + board.musketeer_columns['blackb'] + 1)
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)
      else:
         current_square = get_coordinate_from_index(41) # a5
         row, col = current_square[0] - 1, current_square[1]
         if (piece != None): show_piece(piece, 7-row, col)

def render_piece():
   place_musketeer_pieces()
   for board_index in range(0, 64):
      current_piece = board.piece_at(board_index)
      current_square = get_coordinate_from_index(board_index + 1)
      row, col = current_square[0], current_square[1]
      if (current_piece != None): show_piece(current_piece, 7-row, col)
      
def highlight_header_square(row, col):
   pygame.draw.rect(screen, board_color[((row + col) % 2 == 0)+ 2], 
   pygame.Rect(col * square_size, (row) * square_size, square_size, square_size))
   place_musketeer_pieces()

def highlight_square(row, col): 
   pygame.draw.rect(screen, board_color[((row + col) % 2 == 0)+ 2], 
   pygame.Rect(col * square_size, (row + 1) * square_size, square_size, square_size))
   # current_piece = board.piece_at((7 - row) * 8 + col)
   current_piece = board.piece_at((7-row) * 8 + col)
   if(current_piece != None): show_piece(current_piece, row, col) 

def make_move (move_uci):
   board.push_uci(move_uci)
   render_board()
   render_piece()


def computer_move():
   current_fen = str(board.fen())
   stockfish.set_fen_position(current_fen)
   top_moves = stockfish.get_top_moves(1)
   choose_move = random.choice(top_moves)
   make_move(choose_move['Move']) 
   if board.turn: print("White: ", end="")
   else: print("Black: ", end="")
   print(choose_move, "Evaluation:", end="")
   if(choose_move['Centipawn'] != None): print(choose_move['Centipawn'] / 100)
   else: print('-')

def render_board(): 
   for header_index in range(0, 8):
      current_square = get_coordinate_from_index(header_index + 1)
      row, col = current_square[0], current_square[1]
      pygame.draw.rect(screen, board_color[(row + col) % 2 + 4], 
                       pygame.Rect(col * square_size, row * square_size, square_size, square_size)) 
      
   for board_index in range(0, 64):
      current_square = get_coordinate_from_index(board_index + 1)
      row, col = current_square[0], current_square[1]
      pygame.draw.rect(screen, board_color[(row + col) % 2 == 0], 
                       pygame.Rect(col * square_size, (row + 1) * square_size, square_size, square_size)) 
   for footer_index in range(0, 8):
      current_square = get_coordinate_from_index(footer_index + 1)
      row, col = 9, current_square[1]
      pygame.draw.rect(screen, board_color[(row + col) % 2 + 4], 
                       pygame.Rect(col * square_size, row * square_size, square_size, square_size)) 
def main():
   game_running = True
   global position_selected
   global selected_musketeer
   pygame.display.flip()  # Update the display
   render_board()
   render_piece()
   while game_running == True:
      # random_move() 
      pygame.display.flip()  
      pos = pygame.mouse.get_pos()
      row, col = math.floor(pos[1] / square_size), math.floor(pos[0] / square_size)
      piece = None
      basic_row = row
      if row > 0 and row < 9: row -= 1
      square_uci = chr(col+ord('a'))+chr((8-row)+ord('0'))
      piece = board.piece_at((7 - row) * 8 + col)
      if basic_row is 0 or basic_row is 9:
         piece = None
      if not position_selected :
         piece = None
      if piece != None: 
         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
         # Highlight the square
      else: pygame.mouse.set_cursor()

      for event in pygame.event.get(): 
         if event.type == pygame.QUIT: 
            game_running = False
         if event.type == pygame.MOUSEBUTTONDOWN:
            print(square_uci, row, col)
            if selected_musketeer is not None:
               print('selected row, col ', row, col)
               if row is 0 or row is 9:
                  board.place_musketeer_piece(selected_musketeer, musketeerchess.FILE_NAMES[col])
               render_board()
               render_piece()
               selected_musketeer = None
               position_selected = board.is_all_musketeer_placed()

            if square_uci == 'a6' or square_uci == 'a5':
               if square_uci == 'a6' : selected_musketeer = 'blackw'
               if square_uci == 'a5' : selected_musketeer = 'blackb'
               highlight_square(row, col)
               place_musketeer_pieces()
               for i in range(8):
                  highlight_header_square(0, i)
            if square_uci == 'h3' or square_uci == 'h4':
               if square_uci == 'h3' : selected_musketeer = 'whiteb'
               if square_uci == 'h4' : selected_musketeer = 'whitew'
               highlight_square(row, col)
               place_musketeer_pieces()
               for i in range(8):
                  highlight_header_square(9, i)
            if piece != None:
               highlight_square(row, col)
               # We also want to highlight all possible moves the piece can make
               for move in board.legal_moves: 
                  query = move.uci()[0:2:1]
                  if square_uci == query: 
                     # print(move.uci()[2:4:1])
                     good_square = move.uci()[2:4:1]
                     r = ord(good_square[1]) - ord('1')
                     c = ord(good_square[0]) - ord('a')
                     # pygame.draw.rect(screen, board_color[((r + c) % 2 == 0) + 2], 
                     # pygame.Rect(c * square_size, (7-r) * square_size, square_size, square_size))
                     highlight_square(7-r, c)
            if piece or len(buffer) >= 1: buffer.append(square_uci)
            # print(buffer)
            if(len(buffer) >= 2): 
               try: 
                  make_move(buffer[0]+buffer[1])
                  pygame.display.flip()
                  computer_move()
               except: 
                  print("Illegal Move")
                  render_board()
                  render_piece()
                  pygame.display.flip()
               buffer.clear()
      if board.outcome() != None: 
         board.set_fen(musketeerchess.STARTING_FEN)
         time.sleep(3)
      game_clock.tick(60)
   pygame.quit()
render_board() 
render_piece() 

# Initialize Stockfish
try:
   stockfish = Stockfish(path="C:\Python312\Lib\site-packages\stockfish")
   stockfish_elo = 800
   stockfish_elo = input("Input Stockfish ELO (Default is 800): ")
   # stockfish.update_engine_parameters({"Minimum Thinking Time": 0})
   stockfish.set_elo_rating(stockfish_elo)
except: 
   print("Stockfish path is incorrect")

def select_musketeer_pieces() :
   """method to show game menu"""
   global menu_showed
   # board.place_musketeer_piece('white', 'c')
   # board.place_musketeer_piece('black', 'e')
   # background color
   bg_color = (255, 255, 255)
   # set background color
   screen.fill(bg_color)
   # black color
   black_color = (0, 0, 0)
   # coordinates for "Play" button
   start_btn = pygame.Rect(270, 500, 100, 50)
   mw = 50
   mh = 50

   black_musketeer_pieces = [pygame.Rect(30 + (mw + 10) * math.floor(i % 5), 100 + (mh + 5) * math.floor(i / 5), mw, mh) for i in range(10)]
   white_musketeer_pieces = [pygame.Rect(100 + (mw + 10) * math.floor(i % 5), 260 + (mh + 5) * math.floor(i / 5), mw, mh) for i in range(10)]

   
   
   for i, rect in enumerate(black_musketeer_pieces):
      piece = musketeerchess.Piece(musketeerchess.KING + i, musketeerchess.BLACK)
      if piece is not None:
         current_piece_path = "resources/pieces/"
         if piece.symbol().islower(): current_piece_path = current_piece_path + piece.symbol()
         else: current_piece_path = current_piece_path + 'w' + piece.symbol().lower()
         current_piece_path = current_piece_path + ".png"
         current_piece_png = pygame.image.load(current_piece_path)
         current_piece_png = pygame.transform.scale(current_piece_png, (mw, mh))
         screen.blit(current_piece_png, rect)

   for i, rect in enumerate(white_musketeer_pieces):
      piece = musketeerchess.Piece(musketeerchess.KING + i, musketeerchess.WHITE)
      if piece is not None:
         current_piece_path = "resources/pieces/"
         if piece.symbol().islower(): current_piece_path = current_piece_path + piece.symbol()
         else: current_piece_path = current_piece_path + 'w' + piece.symbol().lower()
         current_piece_path = current_piece_path + ".png"
         current_piece_png = pygame.image.load(current_piece_path)
         current_piece_png = pygame.transform.scale(current_piece_png, (mw, mh))
         screen.blit(current_piece_png, rect)

   #show outline for selected muskteer pieces
   if board.musketeer_pieces['white']:
      draw_outline(screen, white_musketeer_pieces[board.musketeer_pieces['white'] - musketeerchess.KING])
   if board.musketeer_pieces['black']:
      draw_outline(screen, black_musketeer_pieces[board.musketeer_pieces['black'] - musketeerchess.KING])

   # show play button
   pygame.draw.rect(screen, black_color, start_btn)

   # white color
   white_color = (255, 255, 255)
   # create fonts for texts
   big_font = pygame.font.SysFont("comicsansms", 50)
   small_font = pygame.font.SysFont("comicsansms", 20)
   # create text to be shown on the game menu
   welcome_text = big_font.render("Chess", False, black_color)
   created_by = small_font.render("Created by David", True, black_color)
   start_btn_label = small_font.render("Play", True, white_color)
   
   # show welcome text
   screen.blit(welcome_text, 
                  ((screen.get_width() - welcome_text.get_width()) // 2, 
                  20))
   # show credit text
   screen.blit(created_by, 
                  ((screen.get_width() - created_by.get_width()) // 2, 
                  screen.get_height() - created_by.get_height() - 150))
   # show text on the Play button
   screen.blit(start_btn_label, 
                  ((start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2, 
                  start_btn.y + (start_btn.height - start_btn_label.get_height()) // 2)))

   # get pressed keys
   key_pressed = pygame.key.get_pressed()
   # 
   util = Utils()

   # check if left mouse button was clicked
   if util.left_click_event():
      # call function to get mouse event
      mouse_coords = util.get_mouse_event()

      # check if "Play" button was clicked
      if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
         # change button behavior as it is hovered
         pygame.draw.rect(screen, white_color, start_btn, 3)
         
         # change menu flag
         menu_showed = True
      # check if enter or return key was pressed


      elif key_pressed[K_RETURN]:
         menu_showed = True

      for i, rect in enumerate(black_musketeer_pieces):
         if rect.collidepoint(mouse_coords[0], mouse_coords[1]):
            board.select_black_musteer_piece(musketeerchess.PIECE_SYMBOLS[i + musketeerchess.KING])
            draw_outline(screen, rect)
            break
      for i, rect in enumerate(white_musketeer_pieces):
         if rect.collidepoint(mouse_coords[0], mouse_coords[1]):
            board.select_white_musteer_piece(musketeerchess.PIECE_SYMBOLS[i + musketeerchess.KING])
            draw_outline(screen, rect)
            break

def draw_outline(screen, rect):
   transparent_color = (0, 0, 255)
   outline_width = 3
   pygame.draw.rect(screen, transparent_color, rect, outline_width)


if __name__ == "__main__":
   while not menu_showed:
      select_musketeer_pieces()
      pygame.display.flip()  # Update the display
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()
   main()