# main.py
# Blake Caldwell
# March 30, 2021
# This is the game of Reversi using pygame

import pygame
import time

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
grey = (82, 82, 82)
light_grey = (122, 122, 122)
cyan = (50, 176, 201)
green = (26, 186, 15)
yellow = (200, 200, 30)
red = (255, 0, 0)

# Game information
board = []
for i in range(0, 64):
    board.append(' ')
board[27] = 'W'
board[28] = 'B'
board[35] = 'B'
board[36] = 'W'
stuck = False

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
        board_to_coord.append([(i * 8) + j, [(150 + (j * 100)), (150 + (i * 100))]])


# Precondition: 0 <= board_position <= 63
def board_to_coord_function(board_position):
    return board_to_coord[board_position][1]


# Background of Board
def board_background():
    # Green
    pygame.draw.rect(screen, green, (100, 100, 800, 800))
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
        n = False
        s = False
        e = False
        w = False
        ne = False
        nw = False
        se = False
        sw = False

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
                            n = True
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
                            s = True
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
                            e = True
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
                            w = True
                            flag = True
                            break

            # North West test
            if (col - 1) >= 0 and (row - 1) >= 0:
                piece = board[((row - 1) * 8) + (col - 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for NW in range(1, 8):
                        if ((col - NW) >= 0) and ((row - NW) >= 0):
                            if (board[((row - NW) * 8) + (col - NW)] == 'W' and turn) or \
                                    (board[((row - NW) * 8) + (col - NW)] == 'B' and not turn):
                                continue
                            elif board[((row - NW) * 8) + (col - NW)] == ' ':
                                break
                            else:
                                nw = True
                                flag = True
                                break
                        else:
                            break

            # North East test
            if (col + 1) <= 7 and (row - 1) >= 0:
                piece = board[((row - 1) * 8) + (col + 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for NE in range(1, 8):
                        if ((col + NE) <= 7) and ((row - NE) >= 0):
                            if (board[((row - NE) * 8) + (col + NE)] == 'W' and turn) or \
                                    (board[((row - NE) * 8) + (col + NE)] == 'B' and not turn):
                                continue
                            elif board[((row - NE) * 8) + (col + NE)] == ' ':
                                break
                            else:
                                ne = True
                                flag = True
                                break
                        else:
                            break

            # South West test
            if (col - 1) >= 0 and (row + 1) <= 7:
                piece = board[((row + 1) * 8) + (col - 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for SW in range(1, 8):
                        if ((col - SW) >= 0) and ((row + SW) <= 7):
                            if (board[((row + SW) * 8) + (col - SW)] == 'W' and turn) or \
                                    (board[((row + SW) * 8) + (col - SW)] == 'B' and not turn):
                                continue
                            elif board[((row + SW) * 8) + (col - SW)] == ' ':
                                break
                            else:
                                sw = True
                                flag = True
                                break
                        else:
                            break

            # South East test
            if (col + 1) <= 7 and (row + 1) <= 7:
                piece = board[((row + 1) * 8) + (col + 1)]
                if (piece == 'W' and turn) or (piece == 'B' and not turn):
                    for SE in range(1, 8):
                        if ((col + SE) <= 7) and ((row + SE) <= 7):
                            if (board[((row + SE) * 8) + (col + SE)] == 'W' and turn) or \
                                    (board[((row + SE) * 8) + (col + SE)] == 'B' and not turn):
                                continue
                            elif board[((row + SE) * 8) + (col + SE)] == ' ':
                                break
                            else:
                                se = True
                                flag = True
                                break
                        else:
                            break

        if n or s or e or w or ne or nw or se or sw:
            available_moves.append([spot, [n, e, s, w, ne, se, sw, nw]])

    return flag


def draw_available():
    for index in available_moves:
        pygame.draw.circle(screen, yellow, board_to_coord_function(index[0]), 35)


def move_check(position):
    global available_moves
    col = position[0] // 100 - 1
    row = position[1] // 100 - 1
    if 0 <= row <= 7 and 0 <= col <= 7:
        index = row * 8 + col
        for a in range(len(available_moves)):
            if index == available_moves[a][0]:
                board_update(available_moves[a])
                break


def board_update(index):
    global turn
    global available_moves
    global board
    global white_pieces
    global black_pieces

    row = index[0] // 8
    col = index[0] % 8

    if turn:
        end_piece = 'B'
    else:
        end_piece = 'W'

    board[index[0]] = end_piece

    counter = 1
    # North
    if index[1][0]:
        while True:
            if board[(row - counter) * 8 + col] == end_piece:
                break
            else:
                board[(row - counter) * 8 + col] = end_piece
            counter += 1

    counter = 1
    # East
    if index[1][1]:
        while True:
            if board[row * 8 + col + counter] == end_piece:
                break
            else:
                board[row * 8 + col + counter] = end_piece
            counter += 1

    counter = 1
    # South
    if index[1][2]:
        while True:
            if board[(row + counter) * 8 + col] == end_piece:
                break
            else:
                board[(row + counter) * 8 + col] = end_piece
            counter += 1

    counter = 1
    # West
    if index[1][3]:
        while True:
            if board[row * 8 + col - counter] == end_piece:
                break
            else:
                board[row * 8 + col - counter] = end_piece
            counter += 1

    counter = 1
    # North East
    if index[1][4]:
        while True:
            if board[(row - counter) * 8 + col + counter] == end_piece:
                break
            else:
                board[(row - counter) * 8 + col + counter] = end_piece
            counter += 1

    counter = 1
    # South East
    if index[1][5]:
        while True:
            if board[(row + counter) * 8 + col + counter] == end_piece:
                break
            else:
                board[(row + counter) * 8 + col + counter] = end_piece
            counter += 1

    counter = 1
    # South West
    if index[1][6]:
        while True:
            if board[(row + counter) * 8 + col - counter] == end_piece:
                break
            else:
                board[(row + counter) * 8 + col - counter] = end_piece
            counter += 1

    counter = 1
    # North West
    if index[1][7]:
        while True:
            if board[(row - counter) * 8 + col - counter] == end_piece:
                break
            else:
                board[(row - counter) * 8 + col - counter] = end_piece
            counter += 1

    turn = not turn
    available_moves = []
    white_pieces = 0
    black_pieces = 0
    for a in range(len(board)):
        if board[a] == 'W':
            white_pieces += 1
        elif board[a] == 'B':
            black_pieces += 1


def board_full():
    if ' ' in board:
        return False
    else:
        return True


def end_of_game():
    end_running = True
    while end_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                end_click = pygame.mouse.get_pos()
                if 445 <= end_click[0] <= 605 and 485 <= end_click[1] <= 525:
                    end_running = False

        board_background()
        board_pieces()
        board_info()

        pygame.draw.rect(screen, grey, (390, 425, 270, 120))
        pygame.draw.rect(screen, black, (390, 425, 270, 120), width=2)

        mouse_end = pygame.mouse.get_pos()
        if 445 <= mouse_end[0] <= 605 and 485 <= mouse_end[1] <= 525:
            pygame.draw.rect(screen, light_grey, (445, 485, 160, 40))

        pygame.draw.rect(screen, black, (445, 485, 160, 40), width=2)

        if black_pieces > white_pieces:
            win_color = 'BLACK'
        else:
            win_color = 'WHITE'

        font_bold = pygame.font.SysFont('arial', 42, bold=True)
        win = font_bold.render(f"{win_color} WINS!!!", True, red)
        font_button = pygame.font.SysFont('arial', 36)
        text_menu = font_button.render("Main Menu", True, black)

        screen.blit(text_menu, (455, 485))
        screen.blit(win, (400, 425))

        pygame.display.update()


def player_vs_player():
    global turn
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                move_check(pos)

        # Draw board
        screen.fill(cyan)

        board_background()
        board_pieces()
        board_info()
        global stuck
        stuck = False
        if len(available_moves) == 0:
            if not calculate_moves():
                if board_full():
                    end_of_game()
                    running = False
                else:
                    if turn:
                        color = 'Black'
                    else:
                        color = 'White'

                    font = pygame.font.SysFont('arial', 42, bold=True)
                    forfeit_message = font.render(f"{color}'s turn was forfeited because they could not play.",
                                                  True, red)
                    screen.blit(forfeit_message, (80, 475))
                    pygame.display.update()
                    time.sleep(3)
                    turn = not turn
                    if stuck:
                        end_of_game()
                        running = False
                    else:
                        stuck = True
                    continue
            else:
                stuck = False
        draw_available()

        pygame.display.update()


def player_vs_bot():
    print('player vs bot')


def bot_vs_bot():
    print('bot vs bot')


def rules():
    rules_running = True
    while rules_running:
        for event_rules in pygame.event.get():
            if event_rules.type == pygame.QUIT:
                quit()
            if event_rules.type == pygame.MOUSEBUTTONUP:
                rules_position = pygame.mouse.get_pos()
                if 520 <= rules_position[0] <= 580 and 750 <= rules_position[1] <= 780:
                    rules_running = False

        screen.fill(cyan)

        mouse_pos = pygame.mouse.get_pos()

        if 520 <= mouse_pos[0] <= 580 and 750 <= mouse_pos[1] <= 780:
            pygame.draw.rect(screen, light_grey, (520, 750, 60, 30))
        else:
            pygame.draw.rect(screen, grey, (520, 750, 60, 30))

        pygame.draw.rect(screen, black, (520, 750, 60, 30), width=2)

        pygame.draw.rect(screen, grey, (70, 190, 970, 510))
        pygame.draw.rect(screen, black, (70, 190, 970, 510), width=2)

        header = pygame.font.SysFont('arial', 60, bold=True)
        rules_text = header.render("RULES", True, black)
        rules_font = pygame.font.SysFont('arial', 24)
        button_back = rules_font.render("Back", True, black)
        rules_line1 = rules_font.render("This is the game of Reversi otherwise know as Othello, the rules are as follows:", True, black)
        rules_line1_2 = rules_font.render("(The game takes care of most of these rules)", True, black)
        rules_line2 = rules_font.render("1. Black always goes first, in the player vs bot mode the player is black.", True, black)
        rules_line3 = rules_font.render("2. If you do not have an available move, your turn is forfeited. The yellow pieces indicate your potential moves.", True, black)
        rules_line4 = rules_font.render("3. To place a piece you must be able to 'outflank' at least one of the opponents piece(s) (example below).", True, black)
        rules_line5 = rules_font.render("4. You can not outflank your own piece(s).", True, black)
        rules_line6 = rules_font.render("5. Pieces can only be outflanked by the newly placed piece. Flipped pieces do not outflank other pieces.", True, black)
        rules_line7 = rules_font.render("6. All outflanked pieces MUST be flipped even if it leaves you at a disadvantage.", True, black)
        rules_line8 = rules_font.render("7. When neither person can play, the game is over and the person with the most pieces on the board", True, black)
        rules_line8_2 = rules_font.render("    is declared winner.", True, black)

        screen.blit(rules_text, (460, 100))
        screen.blit(rules_line1, (80, 200))
        screen.blit(rules_line1_2, (80, 230))
        screen.blit(rules_line2, (80, 280))
        screen.blit(rules_line3, (80, 310))
        screen.blit(rules_line4, (80, 340))

        pygame.draw.rect(screen, green, (300, 380, 140, 140))
        pygame.draw.rect(screen, black, (300, 380, 140, 140), width=2)
        pygame.draw.line(screen, black, (335, 380), (335, 520), width=2)
        pygame.draw.line(screen, black, (370, 380), (370, 520), width=2)
        pygame.draw.line(screen, black, (405, 380), (405, 520), width=2)
        pygame.draw.line(screen, black, (300, 415), (440, 415), width=2)
        pygame.draw.line(screen, black, (300, 450), (440, 450), width=2)
        pygame.draw.line(screen, black, (300, 485), (440, 485), width=2)

        pygame.draw.circle(screen, white, (318, 397), 12)
        pygame.draw.circle(screen, white, (423, 397), 12)
        pygame.draw.circle(screen, white, (388, 502), 12)
        pygame.draw.circle(screen, black, (318, 467), 12)
        pygame.draw.circle(screen, black, (318, 432), 12)
        pygame.draw.circle(screen, black, (353, 467), 12)
        pygame.draw.circle(screen, black, (388, 432), 12)
        pygame.draw.circle(screen, black, (353, 502), 12)

        pygame.draw.circle(screen, yellow, (318, 502), 12)

        pygame.draw.rect(screen, green, (660, 380, 140, 140))
        pygame.draw.rect(screen, black, (660, 380, 140, 140), width=2)
        pygame.draw.line(screen, black, (695, 380), (695, 520), width=2)
        pygame.draw.line(screen, black, (730, 380), (730, 520), width=2)
        pygame.draw.line(screen, black, (765, 380), (765, 520), width=2)
        pygame.draw.line(screen, black, (660, 415), (800, 415), width=2)
        pygame.draw.line(screen, black, (660, 450), (800, 450), width=2)
        pygame.draw.line(screen, black, (660, 485), (800, 485), width=2)

        pygame.draw.circle(screen, white, (678, 397), 12)
        pygame.draw.circle(screen, white, (783, 397), 12)
        pygame.draw.circle(screen, white, (748, 502), 12)
        pygame.draw.circle(screen, white, (678, 467), 12)
        pygame.draw.circle(screen, white, (678, 432), 12)
        pygame.draw.circle(screen, white, (713, 467), 12)
        pygame.draw.circle(screen, white, (748, 432), 12)
        pygame.draw.circle(screen, white, (713, 502), 12)

        pygame.draw.circle(screen, white, (678, 502), 12)

        screen.blit(rules_line5, (80, 540))
        screen.blit(rules_line6, (80, 570))
        screen.blit(rules_line7, (80, 600))
        screen.blit(rules_line8, (80, 630))
        screen.blit(rules_line8_2, (80, 660))
        screen.blit(button_back, (530, 750))

        pygame.display.update()


if __name__ == "__main__":
    menu_running = True
    while menu_running:
        for event_menu in pygame.event.get():
            if event_menu.type == pygame.QUIT:
                quit()
            if event_menu.type == pygame.MOUSEBUTTONUP:
                menu_pos = pygame.mouse.get_pos()
                if 410 <= menu_pos[0] <= 690 and 400 <= menu_pos[1] <= 450:
                    player_vs_player()
                elif 410 <= menu_pos[0] <= 690 and 460 <= menu_pos[1] <= 510:
                    player_vs_bot()
                elif 410 <= menu_pos[0] <= 690 and 520 <= menu_pos[1] <= 570:
                    bot_vs_bot()
                elif 410 <= menu_pos[0] <= 690 and 580 <= menu_pos[1] <= 630:
                    rules()
                elif 410 <= menu_pos[0] <= 690 and 640 <= menu_pos[1] <= 690:
                    quit()

        screen.fill(cyan)

        mouse = pygame.mouse.get_pos()

        if 410 <= mouse[0] <= 690 and 400 <= mouse[1] <= 450:
            pygame.draw.rect(screen, light_grey, (410, 400, 280, 50))
        else:
            pygame.draw.rect(screen, grey, (410, 400, 280, 50))

        if 410 <= mouse[0] <= 690 and 460 <= mouse[1] <= 510:
            pygame.draw.rect(screen, light_grey, (410, 460, 280, 50))
        else:
            pygame.draw.rect(screen, grey, (410, 460, 280, 50))

        if 410 <= mouse[0] <= 690 and 520 <= mouse[1] <= 570:
            pygame.draw.rect(screen, light_grey, (410, 520, 280, 50))
        else:
            pygame.draw.rect(screen, grey, (410, 520, 280, 50))

        if 410 <= mouse[0] <= 690 and 580 <= mouse[1] <= 630:
            pygame.draw.rect(screen, light_grey, (410, 580, 280, 50))
        else:
            pygame.draw.rect(screen, grey, (410, 580, 280, 50))

        if 410 <= mouse[0] <= 690 and 640 <= mouse[1] <= 690:
            pygame.draw.rect(screen, light_grey, (410, 640, 280, 50))
        else:
            pygame.draw.rect(screen, grey, (410, 640, 280, 50))

        pygame.draw.rect(screen, black, (410, 400, 280, 50), width=2)
        pygame.draw.rect(screen, black, (410, 460, 280, 50), width=2)
        pygame.draw.rect(screen, black, (410, 520, 280, 50), width=2)
        pygame.draw.rect(screen, black, (410, 580, 280, 50), width=2)
        pygame.draw.rect(screen, black, (410, 640, 280, 50), width=2)

        title = pygame.font.SysFont('arial', 60, bold=True)
        reversi = title.render("REVERSI", True, black)

        button_font = pygame.font.SysFont('arial', 42)
        button_pvp = button_font.render("Player vs. Player", True, black)
        button_pvb = button_font.render("Player vs. Bot", True, black)
        button_bvb = button_font.render("Bot vs. Bot", True, black)
        button_rules = button_font.render("Rules", True, black)
        button_quit = button_font.render("Quit", True, black)

        screen.blit(reversi, (440, 100))
        screen.blit(button_pvp, (420, 400))
        screen.blit(button_pvb, (440, 460))
        screen.blit(button_bvb, (470, 520))
        screen.blit(button_rules, (505, 580))
        screen.blit(button_quit, (515, 640))

        pygame.display.update()
