import pygame
def check_valid_moves(turn_step, white_options, black_options, selection):
    if (turn_step < 2):
        options_list = white_options
    else :
        options_list = black_options
    
    valid_options = options_list[selection]

    return valid_options

def check_pawn(position, color, white_locations, black_locations):
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
    else:
        if (position[0], position[1] - 1) not in white_locations and (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        
        if (position[0], position[1] - 2) not in white_locations and (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
    
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))

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

#def check_bishop(locations, turn):

#def check_knight(locations, turn):

#def check_queen(locations, turn):

##def check_king(locations, turn):
