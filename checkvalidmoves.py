import pygame

def check_valid_moves(turn_step, white_options, black_options, selection):
    if (turn_step < 2):
        options_list = white_options
    else :
        options_list = black_options
    
    valid_options = options_list[selection]

    return valid_options

def check_pawn(position, color, white_locations, black_locations, en_passant_target):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        if en_passant_target == (position[0] + 1, position[1] + 1) and (position[0] + 1, position[1]) in black_locations:
            moves_list.append(en_passant_target)
        if en_passant_target == (position[0] - 1, position[1] + 1) and (position[0] - 1, position[1]) in black_locations:
            moves_list.append(en_passant_target)
    else:
        if (position[0], position[1] - 1) not in white_locations and (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
    
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        if en_passant_target == (position[0] + 1, position[1] - 1) and (position[0] + 1, position[1]) in white_locations:
            moves_list.append(en_passant_target)
        if en_passant_target == (position[0] - 1, position[1] - 1) and (position[0] - 1, position[1]) in white_locations:
            moves_list.append(en_passant_target)

    return moves_list

def check_rook(position, color, white_locations, black_locations):
    moves_list = []

    if color == 'white':
        opposing_pieces = black_locations
        friendly_pieces = white_locations
    else:
        opposing_pieces = white_locations
        friendly_pieces = black_locations

    for i in range(4):
        path = True
        chain_length = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else: 
            x = -1
            y = 0

        while path:
            if (position[0] + (chain_length * x), position[1] + (chain_length * y)) not in friendly_pieces and 0 <= position[0] + (chain_length * x) <= 7 and 0 <= position[1] + (chain_length * y) <= 7:
                moves_list.append((position[0] + chain_length * x, position[1] + (chain_length * y)))
                if (position[0] + (chain_length * x), position[1] + (chain_length * y)) in opposing_pieces:
                    path = False
                chain_length += 1
            else:
                path = False

    return moves_list

def check_bishop(position, color, white_locations, black_locations):
    moves_list = []

    if color == 'white':
        opposing_pieces = black_locations
        friendly_pieces = white_locations
    else:
        opposing_pieces = white_locations
        friendly_pieces = black_locations
    
    for i in range(4):
        path = True
        chain_length = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else: 
            x = -1
            y = 1

        while path:
            if (position[0] + (chain_length * x), position[1] + (chain_length * y)) not in friendly_pieces and 0 <= position[0] + (chain_length * x) <= 7 and 0 <= position[1] + (chain_length * y) <= 7:
                moves_list.append((position[0] + chain_length * x, position[1] + (chain_length * y)))
                if (position[0] + (chain_length * x), position[1] + (chain_length * y)) in opposing_pieces:
                    path = False
                chain_length += 1
            else:
                path = False
    
    return moves_list

def check_knight(position, color, white_locations, black_locations):
    moves_list = []

    if color == 'white':
        friendly_pieces = white_locations
    else:
        friendly_pieces = black_locations

    valid_knight_moves = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, -2), (-1, 2), (-2, 1), (-2, -1)]
    
    for i in range(8):
        knight_move = (position[0] + valid_knight_moves[i][0], position[1] + valid_knight_moves[i][1])
        if knight_move not in friendly_pieces and 0 <= knight_move[0] <= 7 and 0 <= knight_move[1] <= 7:
            moves_list.append(knight_move)

    return moves_list

def check_queen(position, color, white_locations, black_locations):
    straight_move_list = check_rook(position, color, white_locations, black_locations)
    diagonal_move_list = check_bishop(position, color, white_locations, black_locations)

    for move in diagonal_move_list:
        straight_move_list.append(move)

    return straight_move_list

def check_king(position, color, white_locations, black_locations):
    moves_list = []

    if color == 'white':
        opposing_pieces = black_locations
        friendly_pieces = white_locations
    else:
        opposing_pieces = white_locations
        friendly_pieces = black_locations

    valid_king_moves = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    
    for i in range(8):
        king_move = (position[0] + valid_king_moves[i][0], position[1] + valid_king_moves[i][1])
        if king_move not in friendly_pieces and 0 <= king_move[0] <= 7 and 0 <= king_move[1] <= 7:
            moves_list.append(king_move)

    return moves_list

def check_promotion(white_pieces, black_pieces, white_locations, black_locations):
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = -1

    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)

    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    
    pawn_indexes = []
        
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)

    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]

    return white_promotion, black_promotion, promote_index

def check_promotion_select(white_promote, black_promote, promo_index, white_pieces, black_pieces, white_promotions, black_promotions):
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100

    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = white_promotions[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = black_promotions[y_pos]
