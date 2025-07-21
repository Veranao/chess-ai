#Github repo: https://github.com/Veranao/chess-ai

import pygame
from assets import *
from checkvalidmoves import *
import random
import time
import copy

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
player_select = True
human_player_white = False
human_player_black = True
turn_moved = False
ai_delay = 0.1
ai_waiting = False
ai_start_time = 0
play_with_minimax = False
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

#Check potential moves for the AI or human player, including preventing illegal moves
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    castling_moves = []
    king_pos = None

    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        enemy_locations = []
        legal_moves = []

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
        
        for move in moves_list:
            all_enemy_moves = []
            if turn == 'white':
                enemy_pieces = black_pieces[:]
                enemy_locations = black_locations[:]
                own_moves = white_moved[:]
                enemy_possible_moves = black_moved[:]

                for j in range(len(enemy_pieces)):
                    enemy_piece = enemy_pieces[j]
                    enemy_location = enemy_locations[j]
                    if enemy_piece == 'pawn':
                        enemy_moves = check_pawn(enemy_location, 'black', white_locations, black_locations, en_passant_target)
                    elif enemy_piece == 'rook':
                        enemy_moves = check_rook(enemy_location, 'black', white_locations, black_locations)
                    elif enemy_piece == 'bishop':
                        enemy_moves = check_bishop(enemy_location, 'black', white_locations, black_locations)
                    elif enemy_piece == 'knight':
                        enemy_moves = check_knight(enemy_location, 'black', white_locations, black_locations)
                    elif enemy_piece == 'queen':
                        enemy_moves = check_queen(enemy_location, 'black', white_locations, black_locations)
                    else:
                        enemy_moves, _ = check_king(enemy_location, 'black', white_pieces, black_pieces, white_locations, black_locations, white_moved, black_moved, white_options, black_options)

                    all_enemy_moves.extend(enemy_moves)
            else:
                enemy_pieces = white_pieces[:]
                enemy_locations = white_locations[:]
                own_moves = black_moved[:]
                enemy_possible_moves = white_moved[:]

                for j in range(len(enemy_pieces)):
                    enemy_piece = enemy_pieces[j]
                    enemy_location = enemy_locations[j]
                    if enemy_piece == 'pawn':
                        enemy_moves = check_pawn(enemy_location, 'white', white_locations, black_locations, en_passant_target)
                    elif enemy_piece == 'rook':
                        enemy_moves= check_rook(enemy_location, 'white', white_locations, black_locations)
                    elif enemy_piece == 'bishop':
                        enemy_moves = check_bishop(enemy_location, 'white', white_locations, black_locations)
                    elif enemy_piece == 'knight':
                        enemy_moves = check_knight(enemy_location, 'white', white_locations, black_locations)
                    elif enemy_piece == 'queen':
                        enemy_moves = check_queen(enemy_location, 'white', white_locations, black_locations)
                    else:
                        enemy_moves , _ = check_king(enemy_location, 'white', white_pieces, black_pieces, white_locations, black_locations, white_moved, black_moved, white_options, black_options)

                    all_enemy_moves.extend(enemy_moves)

            for j in range(len(pieces)):
                if pieces[j] == 'king':
                    current_king_position = locations[j]
                    break

            legal_moves = []

            for move in moves_list:
                temp_locations = locations[:]
                temp_locations[i] = move
                temp_enemy_locations = enemy_locations[:]
                temp_enemy_pieces = enemy_pieces[:]

                if move in temp_enemy_locations:
                    captured_index = temp_enemy_locations.index(move)
                    del temp_enemy_locations[captured_index]
                    del temp_enemy_pieces[captured_index]

                if turn == 'white':
                    temp_white_locations = temp_locations
                    temp_black_locations = temp_enemy_locations[:]
                else:
                    temp_white_locations = temp_enemy_locations[:]
                    temp_black_locations = temp_locations

                simulated_enemy_moves = []
                for j in range(len(temp_enemy_pieces)):
                    enemy_piece = temp_enemy_pieces[j]
                    enemy_location = temp_enemy_locations[j]
                    if turn == 'white':
                        wl, bl = temp_white_locations, temp_black_locations
                        enemy_color = 'black'
                    else:
                        wl, bl = temp_white_locations, temp_black_locations
                        enemy_color = 'white'

                    if enemy_piece == 'pawn':
                        enemy_moves = check_pawn(enemy_location, enemy_color, wl, bl, en_passant_target)
                    elif enemy_piece == 'rook':
                        enemy_moves = check_rook(enemy_location, enemy_color, wl, bl)
                    elif enemy_piece == 'bishop':
                        enemy_moves = check_bishop(enemy_location, enemy_color, wl, bl)
                    elif enemy_piece == 'knight':
                        enemy_moves = check_knight(enemy_location, enemy_color, wl, bl)
                    elif enemy_piece == 'queen':
                        enemy_moves = check_queen(enemy_location, enemy_color, wl, bl)
                    else:
                        enemy_moves, _ = check_king(enemy_location, enemy_color, white_pieces, black_pieces, wl, bl, white_moved, black_moved, white_options, black_options)

                    simulated_enemy_moves.extend(enemy_moves)

                for j in range(len(pieces)):
                    if pieces[j] == 'king':
                        king_pos = temp_locations[j]
                        break

                if king_pos is None or  king_pos not in simulated_enemy_moves:
                    legal_moves.append(move)

            #print("Current legal moves for this piece:", legal_moves)

        all_moves_list.append(legal_moves)

    return all_moves_list, castling_moves

#Greedy algorithm that moves based on material and a greedy capture heuristic
def chess_ai_greedy_algorithm(pieces, locations, turn, options, white_pieces, black_pieces, white_locations, black_locations):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop' : 3.2, 'rook' : 5, 'queen' : 9, 'king': 200}
    best_score = None
    best_moves = []
    piece_index = None
    captured_value = 0
    
    #Simulate a move
    for i in range(len(pieces)):
        for move in options[i]:
            new_locations = locations[:]
            new_locations[i] = move
            new_pieces = pieces[:]

            if turn == 'white':
                opponent_pieces = black_pieces[:]
                opponent_locations = black_locations[:]
                opponent_options, _ = check_options(opponent_pieces, opponent_locations, 'black')

                if move in opponent_locations:
                    capture_index = opponent_locations.index(move)
                    captured_piece = opponent_pieces[capture_index]
                    captured_value = piece_values[captured_piece]
                    del opponent_pieces[capture_index]
                    del opponent_locations[capture_index]
            else:
                opponent_pieces = white_pieces[:]
                opponent_locations = white_locations[:]
                opponent_options, _ = check_options(opponent_pieces, opponent_locations, 'white')

                if move in opponent_locations:
                    capture_index = opponent_locations.index(move)
                    captured_piece = opponent_pieces[capture_index]
                    captured_value = piece_values[captured_piece]
                    del opponent_pieces[capture_index]
                    del opponent_locations[capture_index]
                    opponent_options, _ = check_options(opponent_pieces, opponent_locations, 'white')

            simulated_piece = new_pieces[i]
            if simulated_piece == 'pawn':
                if (turn == 'white' and new_locations[i][1] == 7) or (turn == 'black' and new_locations[i][1] == 0):
                    new_pieces[i] = 'queen'
            
            score = evaluate_greedy(new_pieces, new_locations, opponent_pieces, opponent_options, captured_value)

            print("Best Score: ", best_score)
            if best_score is None or (turn == 'white' and score > best_score) or (turn == 'black' and score < best_score):
                best_score = score
                best_moves = [(i, move)]
            elif score == best_score:
                best_moves.append((i, move))

    if best_moves:
        selected_move = random.choice(best_moves)
        return selected_move
    else:
        return None, None

#evaluator for greedy algorithm
def evaluate_greedy(pieces, locations, opponent_pieces, opponent_options, captured_value=0):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop' : 3.2, 'rook' : 5, 'queen' : 9, 'king': 200}
    score = 0
    opponent_score = 0

    for piece in pieces:
        score += piece_values[piece]
    
    for piece in opponent_pieces:
        opponent_score += piece_values[piece]

    for location_index, location in enumerate(locations):
        piece = pieces[location_index]
        piece_value = piece_values[piece]

        for option_index , option_list in enumerate(opponent_options):
            for move in option_list:
                if location == move:
                    opponent_piece = opponent_pieces[option_index]
                    opponent_value = piece_values[opponent_piece]
                
                    if piece_value > opponent_value:
                        score -= (piece_value - opponent_value) * (random.uniform(0.9, 2.0))
                    else:
                        score -= piece_value * (random.uniform(0.5, 1.5))
                    break
    
    score += captured_value * 1.1

    return score - opponent_score

#minimax algorithm
def minimax_ai_algorithm(pieces, locations, turn, options, depth, white_pieces, black_pieces, white_locations, black_locations, ai_is_white, maximizing_player, alpha=float('-inf'), beta=float('inf')):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop' : 3.2, 'rook' : 5, 'queen' : 9, 'king': 200}
    
    #base case
    if depth == 0:
        if turn == 'white':
            opponent_pieces = black_pieces
            opponent_locations = black_locations
            opponent_color = 'black'
        else:
            opponent_pieces = white_pieces
            opponent_locations = white_locations
            opponent_color = 'white'
        
        opponent_options, _ = check_options(opponent_pieces, opponent_locations, opponent_color)
        evaluation_score = evaluate_minimax(pieces, locations, opponent_pieces, opponent_options, ai_is_white)

        #print("BASE CASE EVALUATION SCORE: ", evaluation_score)
        return evaluation_score, None
    
    #maximizing player = white
    if maximizing_player:
        best_score = float('-inf')
    else:
        best_score = float('inf')
    best_move = None
    assert best_score == float('-inf') if maximizing_player else float('inf'), "best_score initialized incorrectly"

    #copy pieces and recursive step
    for i in range(len(pieces)):
        print(f"\n==== Checking moves for piece index {i} ({pieces[i]} at {locations[i]}) ====")
        for move in options[i]:
            new_pieces = copy.deepcopy(pieces)
            new_locations = copy.deepcopy(locations)
            new_locations[i] = move

            if new_pieces[i] == 'pawn':
                if (turn == 'white' and move[1] == 7) or (turn =='black' and move[1] == 0):
                    new_pieces[i] = 'queen'

            if turn == 'white':
                next_turn = 'black'
                next_white_pieces = copy.deepcopy(new_pieces)
                next_white_locations = copy.deepcopy(new_locations)
                next_black_pieces = copy.deepcopy(black_pieces)
                next_black_locations = copy.deepcopy(black_locations)

                if move in next_black_locations:
                    capture_index = next_black_locations.index(move)
                    del next_black_pieces[capture_index]
                    del next_black_locations[capture_index]
            else:
                next_turn = 'white'
                next_black_pieces = new_pieces
                next_black_locations = new_locations
                next_white_pieces = copy.deepcopy(white_pieces)
                next_white_locations = copy.deepcopy(white_locations)
                
                if move in next_white_locations:
                    capture_index = next_white_locations.index(move)
                    del next_white_pieces[capture_index]
                    del next_white_locations[capture_index]

            next_options, _ = check_options(next_white_pieces if next_turn == 'white' else next_black_pieces, next_white_locations if next_turn == 'white' else next_black_locations, next_turn)
            score, _ = minimax_ai_algorithm(next_white_pieces if next_turn == 'white' else next_black_pieces, next_white_locations if next_turn == 'white' else next_black_locations, next_turn, next_options, depth - 1, next_white_pieces, next_black_pieces, next_white_locations, next_black_locations, ai_is_white, not maximizing_player, alpha=alpha, beta=beta)


            #evaluate and update best score and best move if it is evaluated to be better
            if maximizing_player:
                if score > best_score:
                    print(f"Updating best_score: {score} > {best_score}")
                    best_score = score
                    best_move = (i, move)
                alpha = max(alpha, best_score)
                if beta <= alpha:

                    return best_score, best_move
            else:
                if score < best_score:
                    print(f"Updating best_score: {score} < {best_score}")
                    best_score = score
                    best_move = (i, move)
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score, best_move

            print(f"After comparing: best_score = {best_score}, best_move = {best_move}")
        
        if depth == 2:
            print(f"RETURNING FINAL MOVE: {best_move} with score: {best_score}", maximizing_player and True)
    
    return best_score, best_move

#evaluate function for minimax
def evaluate_minimax(pieces, locations, opponent_pieces, opponent_options, ai_is_white):
        piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 200}
        center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}
        white_score = 0
        black_score = 0

        #Encourage development to the center except for king
        for index, location in enumerate(locations):
            piece = pieces[index]
            if location in center_squares:
                if piece == 'pawn':
                    white_score += 0.3
                elif piece == 'knight':
                    white_score += 0.3
                elif piece == 'bishop':
                    white_score += 0.5
                elif piece == 'king':
                    white_score -= 1.0

        #penalize scenarios where valuable pieces are vulnerable
        for location_index, location in enumerate(locations):
            piece = pieces[location_index]
            piece_value = piece_values[piece]

            for option_index, option_list in enumerate(opponent_options):
                for move in option_list:
                    if location == move:
                        opponent_piece = opponent_pieces[option_index]
                        opponent_value = piece_values[opponent_piece]

                        if piece_value > opponent_value:
                            white_score -= (piece_value - opponent_value) * 1.5
                        else:
                            white_score -= piece_value * 1.2
                        break
        
        #encourage trades 
        for option_index, move_list in enumerate(opponent_options):
            for move in move_list:
                if move in locations:
                    target_index = locations.index(move)
                    attacker_piece = opponent_pieces[option_index]
                    target_piece = pieces[target_index]
                    attacker_value = piece_values[attacker_piece]
                    target_value = piece_values[target_piece]

                    trade_balance = target_value - attacker_value
                    white_score += trade_balance * 0.5

        # rewards position where the opponent has less options by either taking control of spaces away or outright encouraging captures (lowers options obviously)
        white_score -= len([move for moves in opponent_options for move in moves]) * 0.22
 
        for piece in pieces:
            white_score += piece_values[piece]
        
        for piece in opponent_pieces:
            black_score += piece_values[piece]

        if ai_is_white:
            return white_score - black_score
        else:
            return black_score - white_score

#depricated negamax algorithm
'''def negamax_ai_algorithm(pieces, locations, turn, options, depth, white_pieces, black_pieces, white_locations, black_locations, color):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 200}

    if depth == 0:
        if color == 1:
            opponent_pieces = black_pieces
            opponent_locations = black_locations
            opponent_color = 'black'
            opponent_options, _ = check_options(opponent_pieces, opponent_locations, opponent_color)
        else:
            opponent_pieces = white_pieces
            opponent_locations = white_locations
            opponent_color = 'white'
            opponent_options, _ = check_options(opponent_pieces, opponent_locations, opponent_color)
        return color * evaluate_minimax(pieces, locations, opponent_pieces, opponent_options), None
    
    best_score = float('-inf')
    best_move = None

    for i in range(len(pieces)):
        for move in options[i]:
            piece_index = i  # store original index
            new_pieces = pieces[:]
            new_locations = locations[:]
            new_locations[piece_index] = move
            piece_type = new_pieces[piece_index]

            if turn == 'white':
                new_white_pieces = new_pieces
                new_white_locations = new_locations
                new_black_pieces = black_pieces[:]
                new_black_locations = black_locations[:]
                opp_pieces = new_black_pieces
                opp_locations = new_black_locations
            else:
                new_black_pieces = new_pieces
                new_black_locations = new_locations
                new_white_pieces = white_pieces[:]
                new_white_locations = white_locations[:]
                opp_pieces = new_white_pieces
                opp_locations = new_white_locations

            if move in opp_locations:
                capture_index = opp_locations.index(move)
                del opp_pieces[capture_index]
                del opp_locations[capture_index]
                for j in range(len(new_locations)):
                    if j != piece_index and new_locations[j] == move:
                        del new_pieces[j]
                        del new_locations[j]
                        break

            # Promotion
            if piece_type == 'pawn':
                if (turn == 'white' and move[1] == 7) or (turn == 'black' and move[1] == 0):
                    piece_type = 'queen'

            next_turn = 'black' if turn == 'white' else 'white'
            next_options, _ = check_options(new_pieces, new_locations, next_turn)

            score, _ = negamax_ai_algorithm(new_pieces, new_locations, next_turn, next_options, depth - 1, new_white_pieces, new_black_pieces, new_white_locations, new_black_locations, -color)

            score = -score  # Negamax step

            if score > best_score:
                best_score = score
                best_move = (i, move)

    return best_score, best_move '''

black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')

run = True

#setup game
while player_select:
        screen.fill((0, 153, 0))

        #select algo or human to play against. black is always human
        box_width = 600
        box_height = 150
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        pygame.draw.rect(screen, (50, 200, 50), [box_x, box_y, box_width, box_height])
        text = 'Press 1 to play against a human,\n2 to play against a greedy algo AI,\nor any other key to play against a minimax algo AI!'

        x_position = 245 + (600 - box_width) // 2
        y_position = 440 + (150 - box_height) // 2

        text_lines = text.split('\n')

        for i, line in enumerate(text_lines):
            screen.blit(font.render(line, True, 'black'), (x_position + 90, y_position + i * 17)) 

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    human_player_white = True
                    human_player_black = True
                elif event.key == pygame.K_2:
                    human_player_white = False
                    human_player_black = True
                else:
                    human_player_white = False
                    human_player_black = True
                    play_with_minimax = True

                player_select = False

#game loop
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
                if human_player_white:
                    turn_moved = False
                    if chess_coordinate == (8, 8) or chess_coordinate == (9, 9):
                        winner = 'Black'
                    if chess_coordinate in white_locations:
                        selection = white_locations.index(chess_coordinate)
                        selected_piece = white_pieces[selection]

                        if turn_step == 0:
                            turn_step = 1
                    if chess_coordinate in valid_moves and selection != 100:
                        start_y = white_locations[selection][1]
                        white_locations[selection] = chess_coordinate
                        white_moved[selection] = True 

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

                        turn_moved = True

                    elif selection != 100 and selected_piece == 'king': # check for castling
                        for q in range(len(white_castle_options)):
                            if chess_coordinate == white_castle_options[q][0]:
                                white_locations[selection] = chess_coordinate
                                white_moved[selection] = True

                                if chess_coordinate == (1, 0): 
                                    rook_coords = (0,0)
                                else:
                                    rook_coords = (7,0)
                                
                                rook_index = white_locations.index(rook_coords)
                                white_locations[rook_index] = white_castle_options[q][1]

                                turn_moved = True

                    if turn_moved:
                        black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
                        white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                        selection = 100
                        valid_moves = []
                        in_check = draw_check(turn_step, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, screen, counter) # draws check and also returns if in check


                    if turn_step == 0:
                        if in_check and all(len(m) == 0 for m in white_options):
                            winner = 'Black'
                            game_over = True
                    elif turn_step == 2:
                        if in_check and all(len(m) == 0 for m in black_options):
                            winner = 'White'
                            game_over = True

            # black move
            if turn_step > 1 and human_player_black:
                turn_moved = False

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

                    turn_moved = True

                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(black_castle_options)):
                        if chess_coordinate == black_castle_options[q][0]:
                            black_locations[selection] = chess_coordinate
                            black_moved[selection] = True

                            if chess_coordinate == (1, 7): 
                                rook_coords = (0, 7)
                            else:
                                rook_coords = (7, 7)
                            
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = black_castle_options[q][1]

                            turn_moved = True


            #if the game is not over then check for promotions
            if not game_over:
                white_promote, black_promote, promo_index = check_promotion(white_pieces, black_pieces, white_locations, black_locations)
                if white_promote or black_promote:
                    draw_promotion(screen, white_promote, black_promote, white_promotions, black_promotions, piece_list, white_images, black_images)
                    check_promotion_select(white_promote, black_promote, promo_index, white_pieces, black_pieces, white_promotions, black_promotions)
            
            # draws check and also returns if in check
            if turn_moved:
                black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
                white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []
                in_check = draw_check(turn_step, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, screen, counter)


            if turn_step == 0:
                if in_check and all(len(m) == 0 for m in white_options):
                    winner = 'Black'
                    game_over = True
            elif turn_step == 2:
                if in_check and all(len(m) == 0 for m in black_options):
                    winner = 'White'
                    game_over = True

    #AI
    if not human_player_white and turn_step < 2 and not game_over and human_player_black:
        if not ai_waiting:
            ai_start_time = time.time()
            ai_waiting = True
        elif time.time() - ai_start_time >= ai_delay:
            turn_moved = False
            possible_moves = []

            #1) find a piece to move from the valid list
            for i in range(len(white_options)):
                valid_moves = check_valid_moves(turn_step, white_options, black_options, i)
                for move in valid_moves:
                    possible_moves.append((i, move))

            #2) pick a piece to move form the valid list
            if possible_moves:
                if play_with_minimax: 
                    start_time = time.time()
                    _, best_move = minimax_ai_algorithm(white_pieces, white_locations, 'white', white_options, 2, white_pieces, black_pieces, white_locations, black_locations, True, maximizing_player=True)
                    end_time = time.time()
                    print(f"Minimax AI move time:  {round(end_time - start_time, 4)} seconds")
                    if best_move is None or best_move[0] is None or best_move[1] is None:
                        ai_waiting = False
                        continue
                    selection, ai_move = best_move
                    selection = int(selection)
                else:
                    start_time = time.time()
                    selection, ai_move = chess_ai_greedy_algorithm(white_pieces, white_locations, 'white', white_options, white_pieces, black_pieces, white_locations, black_locations)
                    end_time = time.time()
                    print(f"Minimax AI move time:  {round(end_time - start_time, 4)} seconds")
                    selection = int(selection)
                selected_piece = white_pieces[selection]
                #3) Make the move
                start_y = white_locations[selection][1]
                white_locations[selection] = ai_move
                white_moved[selection] = True

                if selected_piece == 'king':
                    for q in range(len(white_castle_options)):
                        if ai_move == white_castle_options[q][0]:
                            white_locations[selection] = ai_move
                            white_moved[selection] = True

                            if ai_move == (1, 0): 
                                rook_coords = (0, 0)
                            else:
                                rook_coords = (7, 0)
                            
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = white_castle_options[q][1]
                            break


                
                if white_pieces[selection] == 'pawn' and ai_move == en_passant_target:
                        captured_white_pieces.append('pawn')
                        captured_pos = (ai_move[0], start_y)
                        if captured_pos in black_locations:
                            black_index = black_locations.index(captured_pos)
                            black_pieces.pop(black_index)
                            black_locations.pop(black_index)
                            black_moved.pop(black_index)

                if ai_move in black_locations:
                    black_piece = black_locations.index(ai_move)
                    captured_white_pieces.append(black_pieces[black_piece])
                    if (black_pieces[black_piece] == 'king'):
                        winner = 'White'
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)
                    black_moved.pop(black_piece)
                
                if white_pieces[selection] == 'pawn' and ai_move[1] == 7:
                    white_pieces[selection] = random.choices(['queen', 'knight', 'bishop', 'rook'], weights=[8, 1, 1, 1], k=1)[0]

                
                if white_pieces[selection] == 'pawn':
                        if abs(ai_move[1] - start_y) == 2:
                            en_passant_target = (ai_move[0], ai_move[1] - 1)
                        else:
                            en_passant_target = None
                else:
                    en_passant_target = None

                turn_moved = True

            if turn_moved:
                black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
                white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 2
                selection = 100
                valid_moves = []
                ai_waiting = False
                in_check = draw_check(turn_step, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, screen, counter) # draws check and also returns if in check


            if turn_step == 0:
                if in_check and all(len(m) == 0 for m in white_options):
                    winner = 'Black'
                    game_over = True
            elif turn_step == 2:
                if in_check and all(len(m) == 0 for m in black_options):
                    winner = 'White'
                    game_over = True

    #surrender option
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
            white_moved = [False] * len(white_pieces)
            black_moved = [False] * len(black_pieces)

            in_check = False

            captured_white_pieces = []
            captured_black_pieces = []
            turn_step = 0
            selection = 100
            valid_moves = []
            black_options, black_castle_options = check_options(black_pieces, black_locations, 'black')
            white_options, white_castle_options = check_options(white_pieces, white_locations, 'white')
            player_select = True
            ai_waiting = False
            ai_start_time = 0

    #game over screen prompt
    if winner != '':
        game_over = True
        draw_game_over(screen, font, winner)
    

    pygame.display.flip()
pygame.quit()

