import pygame
from assets import *
from checkvalidmoves import *

pygame.init()
# Declaring global varables for board setup
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 48)
timer = pygame.time.Clock()
frames_per_second = 60
counter = 0
winner = ''
game_over = False
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
    moves_list = []
    all_moves_list = []

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]

        if piece == 'pawn':
            moves_list = check_pawn(location, turn, white_locations, black_locations)
        elif piece == 'rook':
            moves_list = check_rook(location, turn, white_locations, black_locations)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn, white_locations, black_locations)
        elif piece == 'knight':
            moves_list = check_knight(location, turn, white_locations, black_locations)
        elif piece == 'queen':
            moves_list = check_queen(location, turn, white_locations, black_locations)
        else:
            moves_list = check_king(location, turn, white_locations, black_locations)

        all_moves_list.append(moves_list)

    return all_moves_list

#def restart_game(game_over):

black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True

while run:
    timer.tick(frames_per_second)
    screen.fill((153, 80, 0))
    if counter < 30:
        counter += 1
    else:
        counter = 0
    draw_board(screen, WIDTH, HEIGHT, turn_step, big_font, turn_prompt)
    draw_pieces(piece_list, white_pieces, black_pieces, white_images, black_images, white_locations, black_locations, screen, turn_step, selection)
    draw_captured(captured_white_pieces, captured_black_pieces, small_white_images, small_black_images, piece_list, screen)
    draw_check(turn_step, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, screen, counter)

    if selection != 100:
        valid_moves = check_valid_moves(turn_step, white_options, black_options, selection)
        draw_valid(valid_moves, turn_step, screen)

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
                        if (black_pieces[black_piece] == 'king'):
                            winner = 'White'
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
                        if (white_pieces[white_piece] == 'king'):
                            winner = 'Black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over: 
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_white_pieces = []
                captured_black_pieces = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')



    if winner != '':
        game_over = True
        draw_game_over(screen, font, winner)
    
    pygame.display.flip()
pygame.quit()

