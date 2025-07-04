import pygame

_CHESSPIECESPATH = "./images/chess-pieces-basic/"

def load_pieces(side, image_arr, image_arr_small, piece_list):
    for image in piece_list:
        piece = pygame.image.load(_CHESSPIECESPATH + image + "-" + side + ".svg")
        piece = pygame.transform.scale(piece, (250, 250))
        image_arr.append(piece)

        small_piece = pygame.transform.scale(piece, (150, 150))
        image_arr_small.append(small_piece)

def draw_board(screen, width, height, turn_step, big_font, turn_prompt, white_promote, black_promote):
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

    screen.blit(big_font.render(turn_prompt[turn_step], True, 'black'), (20, 835))

    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 5)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 5)
    
    screen.blit(big_font.render('RESIGN', True, 'black'), (837, 835))

    if white_promote or black_promote:
        pygame.draw.rect(screen, (0, 153, 0), [0, 800, width - 200, 100])
        pygame.draw.rect(screen, (0, 53, 0), [0, 800, width - 200, 100], 5)
        screen.blit(big_font.render('Select piece that you want to promote pawn to', True, 'black'), (20, 820))


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

def draw_check(turn_step, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, screen, counter):
    checked = False
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, (255, 51, 51), [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, (255, 51, 51), [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)
                        
def draw_promotion(screen, white_promote, black_promote, white_promotions, black_promotions, piece_list, white_images, black_images):
    pygame.draw.rect(screen, 'light gray', [800, 0, 200, 450])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (860, 5 + 100 * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (860, 5 + 100 * i))

    pygame.draw.rect(screen, color, [800, 0, 200, 450], 8)


def draw_game_over(screen, font, winner):
    pygame.draw.rect(screen, 'white', [200, 200, 500, 200])
    screen.blit(font.render(f'{winner} won the game!', True, 'black'), (210, 210))
    screen.blit(font.render(f'Press ENTER to begin another game!', True, 'black'), (210, 240))