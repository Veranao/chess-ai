import pygame
from assets import load_pieces
from assets import draw_board
from assets import draw_pieces

pygame.init()
# Declaring global varables for board setup
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 48)
timer = pygame.time.Clock()
frames_per_second = 60
pygame.display.set_caption('Chess in Python')


#chess pieces, locations, and piece capturing arrays
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn' ]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn' ]

white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_white_pieces = []
captured_black_pieces = []

#0 - white turn, no selection
#1 - white turn, piece selected
#2 - black turn, no selection
#3 - black turn, piece selected
turn_step = 0
selection = 100
valid_moves = []

#load in game piece images
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

white_images = []
small_white_images = []

black_images = []
small_black_images = []

load_pieces("b", black_images, small_black_images, piece_list)
load_pieces("w", white_images, small_white_images, piece_list)

turn_prompt = ['White: Select a piece to move!', 'White: Select where to go!', 'Black: Select a piece to move!', 'Black: Select where to go!']

def check_options(pieces, locations, turn):
    pass
    #Implement to check the move list of all the pieces in the game and their valid moves at a given state of the game (depending on what turn with one turn of look-ahead)

black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True

while run:
    timer.tick(frames_per_second)
    screen.fill((153, 80, 0))
    draw_board(screen, WIDTH, HEIGHT, turn_step, big_font, turn_prompt)
    draw_pieces(piece_list, white_pieces, black_pieces, white_images, black_images, white_locations, black_locations, screen, turn_step, selection)

    #event handling for quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            chess_coordinate = (event.pos[0] // 100, event.pos[1] // 100)

            if turn_step < 2:
                if chess_coordinate in white_locations:
                    selection = white_locations.index(chess_coordinate)
                    if turn_step == 0:
                        turn_step = 1
                if chess_coordinate in valid_moves and selection != 100:
                    white_locations[selection] = chess_coordinate
                    if chess_coordinate in black_locations:
                        black_piece = black_locations.index(chess_coordinate)
                        captured_white_pieces.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            if turn_step > 1:
                if chess_coordinate in black_locations:
                    selection = black_locations.index(chess_coordinate)
                    if turn_step == 2:
                        turn_step = 3
                if chess_coordinate in valid_moves and selection != 100:
                    black_locations[selection] = chess_coordinate
                    if chess_coordinate in white_locations:
                        white_piece = white_locations.index(chess_coordinate)
                        captured_black_pieces.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
    
    pygame.display.flip()
pygame.quit()

