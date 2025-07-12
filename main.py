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

white_promotions = ['bishop', 'knight', 'rook', 'queen']
black_promotions = ['bishop', 'knight', 'rook', 'queen']

white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_white_pieces = []
captured_black_pieces = []

white_options = []
black_options = []

#0 - white turn, no selection
#1 - white turn, piece selected
#2 - black turn, no selection
#3 - black turn, piece selected
turn_step = 0
selection = 100
valid_moves = []
en_passant_target = None # (x, y)
white_king_moved = False
white_kingside_rook_moved = False
white_queenside_rook_moved = False
black_king_moved = False
black_kingside_rook_moved = False
black_queenside_rook_moved = False
white_promote = False
black_promote = False
promo_index = 100

#load in game piece images
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

white_images = []
small_white_images = []

black_images = []
small_black_images = []

white_moved = []
black_moved = []

in_check = False

# initialize move check to false for all pieces
for i in range(len(white_pieces)):
    white_moved.append(False)
    black_moved.append(False)

load_pieces("b", black_images, small_black_images, piece_list)
load_pieces("w", white_images, small_white_images, piece_list)

turn_prompt = ['White: Select a piece to move!', 'White: Select where to go!', 'Black: Select a piece to move!', 'Black: Select where to go!']

def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    castling_moves = []

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]

        if piece == 'pawn':
            moves_list = check_pawn(location, turn, white_locations, black_locations, en_passant_target)
        elif piece == 'rook':
            moves_list = check_rook(location, turn, white_locations, black_locations)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn, white_locations, black_locations)
        elif piece == 'knight':
            moves_list = check_knight(location, turn, white_locations, black_locations)
        elif piece == 'queen':
            moves_list = check_queen(location, turn, white_locations, black_locations)
        else:
            moves_list, castling_moves = check_king(location, turn, white_pieces, black_pieces, white_locations, black_locations, white_moved, black_moved, white_options, black_options)

        all_moves_list.append(moves_list)

    return all_moves_list, castling_moves

#def restart_game(game_over):

black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
run = True

while run:
    timer.tick(frames_per_second)
    screen.fill((153, 80, 0))
    if counter < 30:
        counter += 1
    else:
        counter = 0
    draw_board(screen, WIDTH, HEIGHT, turn_step, big_font, turn_prompt, white_promote, black_promote)
    draw_pieces(piece_list, white_pieces, black_pieces, white_images, black_images, white_locations, black_locations, screen, turn_step, selection)
    draw_captured(captured_white_pieces, captured_black_pieces, small_white_images, small_black_images, piece_list, screen)
    in_check = draw_check(turn_step, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, screen, counter) # draws check and also returns if in check
    
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion(white_pieces, black_pieces, white_locations, black_locations)
        if white_promote or black_promote:
            draw_promotion(screen, white_promote, black_promote, white_promotions, black_promotions, piece_list, white_images, black_images)
            check_promotion_select(white_promote, black_promote, promo_index, white_pieces, black_pieces, white_promotions, black_promotions)

    if selection != 100:
        valid_moves = check_valid_moves(turn_step, white_options, black_options, selection)
        draw_valid(valid_moves, turn_step, screen)
        if selected_piece == 'king':
            draw_castling(turn_step, white_castle_options, black_castle_options, screen, font)

    #event handling for quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over: 
            chess_coordinate = (event.pos[0] // 100, event.pos[1] // 100)

            # white move
            if turn_step < 2:
                if chess_coordinate == (8, 8) or chess_coordinate == (9, 9):
                    winner = 'Black'
                if chess_coordinate in white_locations:
                    selection = white_locations.index(chess_coordinate)
                    selected_piece = white_pieces[selection]

                    # if selected_piece == 'king':
                    #     draw_castling(turn_step, white_castle_options, black_castle_options, screen, font)
            
                    if turn_step == 0:
                        turn_step = 1
                if chess_coordinate in valid_moves and selection != 100:
                    start_y = white_locations[selection][1]
                    white_locations[selection] = chess_coordinate
                    white_moved[selection] = True # track if the piece has ever moved

                    if white_pieces[selection] == 'pawn' and chess_coordinate == en_passant_target:
                        captured_white_pieces.append('pawn')
                        captured_pos = (chess_coordinate[0], start_y)
                        if captured_pos in black_locations:
                            black_index = black_locations.index(captured_pos)
                            black_pieces.pop(black_index)
                            black_locations.pop(black_index)
                            black_moved.pop(black_index)

                    if white_pieces[selection] == 'pawn':
                        if abs(chess_coordinate[1] - start_y) == 2:
                            en_passant_target = (chess_coordinate[0], chess_coordinate[1] - 1)
                        else:
                            en_passant_target = None
                    else:
                        en_passant_target = None
                
                    if chess_coordinate in black_locations:
                        black_piece = black_locations.index(chess_coordinate)
                        captured_white_pieces.append(black_pieces[black_piece])
                        if (black_pieces[black_piece] == 'king'):
                            winner = 'White'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)

                    black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
                    white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            # black move
            if turn_step > 1:
                if chess_coordinate == (8, 8) or chess_coordinate == (9, 9):
                    winner = 'White'
                if chess_coordinate in black_locations:
                    selection = black_locations.index(chess_coordinate)
                    selected_piece = black_pieces[selection]

                    # if selected_piece == 'king':
                    #     draw_castling(turn_step, white_castle_options, black_castle_options, screen, font)
                    
                    if turn_step == 2:
                        turn_step = 3
                if chess_coordinate in valid_moves and selection != 100:
                    start_y = black_locations[selection][1]
                    black_locations[selection] = chess_coordinate
                    black_moved[selection] = True # track if the piece has ever moved

                    if black_pieces[selection] == 'pawn' and chess_coordinate == en_passant_target:
                        captured_black_pieces.append('pawn')
                        captured_pos = (chess_coordinate[0], start_y)
                        if captured_pos in white_locations:
                            white_index = white_locations.index(captured_pos)
                            white_pieces.pop(white_index)
                            white_locations.pop(white_index)

                    if black_pieces[selection] == 'pawn':
                        if abs(chess_coordinate[1] - start_y) == 2:
                            en_passant_target = (chess_coordinate[0], chess_coordinate[1] + 1)
                        else:
                            en_passant_target = None
                    else:
                        en_passant_target = None

                    if chess_coordinate in white_locations:
                        white_piece = white_locations.index(chess_coordinate)
                        captured_black_pieces.append(white_pieces[white_piece])
                        if (white_pieces[white_piece] == 'king'):
                            winner = 'Black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)

                    black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
                    white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over: 

            # reset all parts
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
                
                # initialize move check to false for all pieces
                for i in range(len(white_pieces)):
                    white_moved[i] = False
                    black_moved[i] = False

                in_check = False

                captured_white_pieces = []
                captured_black_pieces = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
                white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')



    if winner != '':
        game_over = True
        draw_game_over(screen, font, winner)
    
    pygame.display.flip()
pygame.quit()

