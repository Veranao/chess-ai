import pygame

_CHESSPIECESPATH = "./images/chess-pieces-basic/"

def load_pieces(side, image_arr, image_arr_small, piece_list):
    for image in piece_list:
        piece = pygame.image.load(_CHESSPIECESPATH + image + "-" + side + ".svg")
        piece = pygame.transform.scale(piece, (250, 250))
        image_arr.append(piece)

        small_piece = pygame.transform.scale(piece, (150, 150))
        image_arr_small.append(small_piece)

def draw_board(screen, width, height, turn_step, big_font, turn_prompt):
    for i in range(32):
        row = i // 4
        column = i % 4

        if row % 2 == 0:
            pygame.draw.rect(screen, (245, 197, 155), [600 - (column * 200), row * 100, 100, 100])
        else: 
            pygame.draw.rect(screen , (245, 197, 155), [700 - (column * 200), row * 100, 100, 100])

    pygame.draw.rect(screen, (0, 153, 0), [0, 800, width, 100])
    pygame.draw.rect(screen, (0, 153, 0), [800, 0, height, 800])
    pygame.draw.rect(screen, (0, 53, 0), [0, 800, width, 100], 5)
    pygame.draw.rect(screen, (0, 53, 0), [800, 0, 200, height], 5)

    screen.blit(big_font.render(turn_prompt[turn_step], True, 'black'), (20, 820))

    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 5)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 5)

def draw_pieces(piece_list, white_pieces, black_pieces, white_images, black_images, white_locations, black_locations, screen, turn_step, selection):
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_locations[i][0] * 100 + 7, white_locations[i][1] * 100 + 5))

        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 3)


    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_locations[i][0] * 100 + 7, black_locations[i][1] * 100 + 5))

        if turn_step > 1:
            if selection == i:
                pygame.draw.rect(screen, 'red', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 3)

def draw_valid(moves, turn_step, screen):
    for i in range(len(moves)):
        pygame.draw.circle(screen, 'red', (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

def draw_captured(captured_white_pieces, captured_black_pieces, small_white_images, small_black_images, piece_list, screen):
    
    for i in range(len(captured_white_pieces)):
        captured_piece = captured_white_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    
    for i in range(len(captured_black_pieces)):
        captured_piece = captured_black_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))