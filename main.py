# main.py
# Blake Caldwell
# March 30, 2021
# This is the game of Reversi using pygame

import pygame

# Pygame initialization
pygame.init()

# Screen setup
screen = pygame.display.set_mode((1100, 1000))

# Window setup
pygame.display.set_caption("Reversi")
icon = pygame.image.load("r.png")
pygame.display.set_icon(icon)

# RGB Color Definitions
black = (0, 0, 0)
white = (255, 255, 255)

# Game information
board = []
for i in range(0, 64):
    board.append(' ')
board[27] = 'W'
board[28] = 'B'
board[35] = 'B'
board[36] = 'W'

available_moves = []
black_pieces = 2
white_pieces = 2

# True = Black
# False = White
turn = True

# Piece locations to board coordinates
board_to_coord = []
for i in range(0, 8):
    for j in range(0, 8):
        board_to_coord.append([(i*8)+j, [(150+(j*100)), (150+(i*100))]])


# Precondition: 0 <= board_position <= 63
def board_to_coord_function(board_position):
    return board_to_coord[board_position][1]


# Background of Board
def board_background():
    # Green
    pygame.draw.rect(screen, (26, 186, 15), (100, 100, 800, 800))
    pygame.draw.rect(screen, black, (100, 100, 800, 800), width=2)

    # Vertical Lines
    pygame.draw.line(screen, black, (200, 100), (200, 900), width=2)
    pygame.draw.line(screen, black, (300, 100), (300, 900), width=2)
    pygame.draw.line(screen, black, (400, 100), (400, 900), width=2)
    pygame.draw.line(screen, black, (500, 100), (500, 900), width=2)
    pygame.draw.line(screen, black, (600, 100), (600, 900), width=2)
    pygame.draw.line(screen, black, (700, 100), (700, 900), width=2)
    pygame.draw.line(screen, black, (800, 100), (800, 900), width=2)

    # Horizontal Lines
    pygame.draw.line(screen, black, (100, 200), (900, 200), width=2)
    pygame.draw.line(screen, black, (100, 300), (900, 300), width=2)
    pygame.draw.line(screen, black, (100, 400), (900, 400), width=2)
    pygame.draw.line(screen, black, (100, 500), (900, 500), width=2)
    pygame.draw.line(screen, black, (100, 600), (900, 600), width=2)
    pygame.draw.line(screen, black, (100, 700), (900, 700), width=2)
    pygame.draw.line(screen, black, (100, 800), (900, 800), width=2)


# Print the pieces to the board
def board_pieces():
    for index in range(len(board)):
        if board[index] == 'W':
            pygame.draw.circle(screen, white, board_to_coord_function(index), 35)
        elif board[index] == 'B':
            pygame.draw.circle(screen, black, board_to_coord_function(index), 35)


def board_info():
    font = pygame.font.SysFont('arial', 32)
    pieces_image = font.render("Piece Count:", True, black)
    black_info_image = font.render(f"Black: {black_pieces}", True, black)
    white_info_image = font.render(f"White: {white_pieces}", True, black)

    turn_image = font.render("Turn: ", True, black)

    screen.blit(pieces_image, (920, 100))
    screen.blit(black_info_image, (920, 140))
    screen.blit(white_info_image, (920, 180))

    screen.blit(turn_image, (920, 300))
    if turn:
        pygame.draw.circle(screen, black, (980, 375), 35)
    else:
        pygame.draw.circle(screen, white, (980, 375), 35)


def calculate_moves():
    global available_moves

    flag = False
    available_moves = []

    # Check for available moves
    for spot in range(len(board)):
        row = spot // 8
        col = spot % 8
        piece = ' '
        if board[spot] == ' ':

            # North test
            if (row - 1) >= 0:
                piece = board[((row - 1) * 8) + col]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for N in range((row - 2), -1, -1):
                        if (board[N * 8 + col] == 'W' and turn) or (board[N * 8 + col] == 'B' and not turn):
                            continue
                        elif board[N * 8 + col] == ' ':
                            break
                        else:
                            available_moves.append(spot)
                            flag = True
                            break

            # South test
            if (row + 1) <= 7:
                piece = board[((row + 1) * 8) + col]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for S in range((row + 2), 8):
                        if (board[S * 8 + col] == 'W' and turn) or (board[S * 8 + col] == 'B' and not turn):
                            continue
                        elif board[S * 8 + col] == ' ':
                            break
                        else:
                            available_moves.append(spot)
                            flag = True
                            break

            # East test
            if (col + 1) <= 7:
                piece = board[(row * 8) + (col + 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for E in range((col + 2), 8):
                        if (board[(row * 8) + E] == 'W' and turn) or board[(row * 8) + E] == 'B' and not turn:
                            continue
                        elif board[row * 8 + E] == ' ':
                            break
                        else:
                            available_moves.append(spot)
                            flag = True
                            break

            # West test
            if (col - 1) >= 0:
                piece = board[(row * 8) + (col - 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for W in range((col - 2), -1, -1):
                        if (board[(row * 8) + W] == 'W' and turn) or board[(row * 8) + W] == 'B' and not turn:
                            continue
                        elif board[row * 8 + W] == ' ':
                            break
                        else:
                            available_moves.append(spot)
                            flag = True
                            break

            # North West test
            if (col - 1) >= 0 and (row - 1) >= 0:
                piece = board[((row - 1) * 8) + (col - 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for NW in range(0, 8):
                        if ((col - NW) >= 0) and ((row - NW) >= 0):
                            if (board[((row - NW) * 8) + (col - NW)] == 'W' and turn) or \
                                    (board[((row - NW) * 8) + (col - NW)] == 'B' and not turn):
                                continue
                            elif board[((row - NW) * 8) + (col - NW)] == ' ':
                                break
                            else:
                                available_moves.append(spot)
                                flag = True
                                break
                        else:
                            break

            # North East test
            if (col + 1) <= 7 and (row - 1) >= 0:
                piece = board[((row - 1) * 8) + (col + 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for NE in range(0, 8):
                        if ((col + NE) <= 7) and ((row - NE) >= 0):
                            if (board[((row - NE) * 8) + (col + NE)] == 'W' and turn) or \
                                    (board[((row - NE) * 8) + (col + NE)] == 'B' and not turn):
                                continue
                            elif board[((row - NE) * 8) + (col + NE)] == ' ':
                                break
                            else:
                                available_moves.append(spot)
                                flag = True
                                break
                        else:
                            break

            # South West test
            if (col - 1) >= 0 and (row + 1) <= 7:
                piece = board[((row + 1) * 8) + (col - 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for SW in range(0, 8):
                        if ((col - SW) >= 0) and ((row + SW) <= 7):
                            if (board[((row + SW) * 8) + (col - SW)] == 'W' and turn) or \
                                    (board[((row + SW) * 8) + (col - SW)] == 'B' and not turn):
                                continue
                            elif board[((row + SW) * 8) + (col - SW)] == ' ':
                                break
                            else:
                                available_moves.append(spot)
                                flag = True
                                break
                        else:
                            break

            # South East test
            if (col + 1) <= 7 and (row + 1) <= 7:
                piece = board[((row + 1) * 8) + (col + 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for SE in range(0, 8):
                        if ((col + SE) <= 7) and ((row + SE) <= 7):
                            if (board[((row + SE) * 8) + (col + SE)] == 'W' and turn) or \
                                    (board[((row + SE) * 8) + (col + SE)] == 'B' and not turn):
                                continue
                            elif board[((row + SE) * 8) + (col + SE)] == ' ':
                                break
                            else:
                                available_moves.append(spot)
                                flag = True
                                break
                        else:
                            break

    return flag


def draw_available():
    for index in available_moves:
        pygame.draw.circle(screen, (200, 200, 30), board_to_coord_function(index), 35)


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

    # Draw board
    screen.fill((50, 176, 201))

    board_background()
    board_pieces()
    board_info()
    if len(available_moves) == 0:
        print("calculate")
        if not calculate_moves():
            running = False
    draw_available()

    pygame.display.update()
