import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up the display size
WIDTH, HEIGHT = 600, 700  # Define window size (height includes space for score and button)

# Set the available height for the game grid (leave space for score and button)
GRID_SIZE = min(WIDTH, HEIGHT - 150)  # Subtract 150 to make space for score and button

# Define constants based on grid size
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = GRID_SIZE // BOARD_COLS
CROSS_WIDTH = 25
CIRCLE_WIDTH = 15
RADIUS = SQUARE_SIZE // 3
OFFSET = 50

# Set height to include score and button area
GAME_HEIGHT = GRID_SIZE

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)

# Define smaller font for score and button
FONT = pygame.font.SysFont('Arial', 20)  # Reduced from 30 to 20 for the score
BUTTON_FONT = pygame.font.SysFont('Arial', 15)  # Reduced from 20 to 15 for the button

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set window size
pygame.display.set_caption('Tic Tac Toe')

# Initialize board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Initialize players
player = 1  # Player 1 starts (Red crosses)
game_over = False
player1_score, player2_score = 0, 0

# Countdown timer setup
PLAYER_TIME_LIMIT = 10000  # 10 seconds in milliseconds
current_time = pygame.time.get_ticks()
time_left = PLAYER_TIME_LIMIT
timer_running = True

# Confetti animation setup
confetti_fall_time = 0.75  # Time in seconds for confetti to fall
confetti_positions = []
confetti_colors = []

# Draw lines on the board
def draw_lines():
    screen.fill(BG_COLOR)
    # Horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (GRID_SIZE, i * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, GRID_SIZE), LINE_WIDTH)

# Draw the cross
def draw_cross(row, col):
    start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
    end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
    pygame.draw.line(screen, RED, start_desc, end_desc, CROSS_WIDTH)
    start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
    end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
    pygame.draw.line(screen, RED, start_asc, end_asc, CROSS_WIDTH)

# Draw the circle (nought)
def draw_circle(row, col):
    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.circle(screen, BLUE, center, RADIUS, CIRCLE_WIDTH)

# Mark the square with the current player's symbol
def mark_square(row, col, player):
    board[row][col] = player

# Check if a square is available
def is_available_square(row, col):
    return board[row][col] is None

# Check if the board is full (draw)
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

# Check if a player has won
def check_win(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_winning_line(col, 'vertical', player)
            return True

    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_winning_line(row, 'horizontal', player)
            return True

    # Ascending diagonal win check
    if board[0][2] == board[1][1] == board[2][0] == player:
        draw_winning_line(None, 'ascending', player)
        return True

    # Descending diagonal win check
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_winning_line(None, 'descending', player)
        return True

    return False

# Draw the winning line
def draw_winning_line(index, direction, player):
    color = RED if player == 1 else BLUE
    if direction == 'vertical':
        pygame.draw.line(screen, color, 
                         (index * SQUARE_SIZE + SQUARE_SIZE // 2, 15), 
                         (index * SQUARE_SIZE + SQUARE_SIZE // 2, GRID_SIZE - 15), WIN_LINE_WIDTH)
    elif direction == 'horizontal':
        pygame.draw.line(screen, color, 
                         (15, index * SQUARE_SIZE + SQUARE_SIZE // 2), 
                         (GRID_SIZE - 15, index * SQUARE_SIZE + SQUARE_SIZE // 2), WIN_LINE_WIDTH)
    elif direction == 'ascending':
        pygame.draw.line(screen, color, (15, GRID_SIZE - 15), (GRID_SIZE - 15, 15), WIN_LINE_WIDTH)
    elif direction == 'descending':
        pygame.draw.line(screen, color, (15, 15), (GRID_SIZE - 15, GRID_SIZE - 15), WIN_LINE_WIDTH)

# Reset the game for a new round
def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    global board, game_over, player, time_left, current_time, confetti_positions, confetti_colors
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player = 1
    time_left = PLAYER_TIME_LIMIT  # Reset timer
    current_time = pygame.time.get_ticks()  # Reset timer start
    confetti_positions.clear()  # Clear previous confetti
    confetti_colors.clear()  # Clear previous confetti colors

# Clear the score area before drawing the updated score
def clear_score_area():
    score_area_rect = pygame.Rect(0, GAME_HEIGHT, WIDTH, 100)
    pygame.draw.rect(screen, BG_COLOR, score_area_rect)

# Draw the current score
def draw_score():
    clear_score_area()  # Clear the score area before updating the score
    score_text = f"Player 1 (Red Crosses): {player1_score} | Player 2 (Blue Noughts): {player2_score}"
    score_surface = FONT.render(score_text, True, LINE_COLOR)
    screen.blit(score_surface, (20, GAME_HEIGHT + 10))

# Draw the "Close" button
def draw_button():
    button_text = BUTTON_FONT.render('Close', True, (0, 0, 0))
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 80, 100, 50)
    
    # Change button color on hover
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    screen.blit(button_text, (button_rect.x + 15, button_rect.y + 10))
    return button_rect

# Draw animated confetti
def draw_confetti(winner):
    global confetti_positions, confetti_colors
    confetti_color = RED if winner == 1 else BLUE
    # Generate confetti positions and colors
    for _ in range(100):  # Generate 100 confetti pieces
        x = random.randint(0, WIDTH)
        y = 0  # Start from the top
        confetti_positions.append([x, y])
        confetti_colors.append(confetti_color)

    # Animate confetti falling
    for i in range(int(confetti_fall_time * 60)):  # 60 FPS
        screen.fill(BG_COLOR)
        draw_lines()  # Redraw the grid

        for j in range(len(confetti_positions)):
            confetti_positions[j][1] += (GRID_SIZE / (confetti_fall_time * 60))  # Update Y position

            # Draw each confetti piece
            pygame.draw.rect(screen, confetti_colors[j], (confetti_positions[j][0], confetti_positions[j][1], 5, 5))

        pygame.display.update()
        pygame.time.delay(16)  # Delay to create a frame rate of ~60 FPS

# Draw dynamic lighting borders around squares
def draw_dynamic_lighting():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is not None:  # Only draw if the square is occupied
                color = RED if board[row][col] == 1 else BLUE
                # Draw a border around the square
                border_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, border_rect, 5)  # Border width of 5

# Move to the next round automatically after a short delay
def auto_restart_game():
    pygame.display.update()
    time.sleep(2)  # Wait for 2 seconds
    restart_game()  # Move to next round automatically

# Draw the timer for the current player
def draw_timer(time_left):
    timer_text = f"Time Left: {time_left // 1000} seconds"
    timer_surface = FONT.render(timer_text, True, LINE_COLOR)
    screen.blit(timer_surface, (WIDTH // 2 - timer_surface.get_width() // 2, GAME_HEIGHT + 50))

# Main game loop
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if timer_running:
            elapsed_time = pygame.time.get_ticks() - current_time
            time_left = PLAYER_TIME_LIMIT - elapsed_time
            if time_left <= 0:
                player = 2 if player == 1 else 1
                current_time = pygame.time.get_ticks()  # Reset timer for new player

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # Check if the "Close" button is clicked
            if draw_button().collidepoint(mouseX, mouseY):
                pygame.quit()
                sys.exit()

            if not game_over:
                if mouseY < GAME_HEIGHT:  # Make sure the click is on the board
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE

                    if is_available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)

                        if player == 1:
                            draw_cross(clicked_row, clicked_col)
                        else:
                            draw_circle(clicked_row, clicked_col)

                        if check_win(player):
                            game_over = True
                            if player == 1:
                                player1_score += 1
                            else:
                                player2_score += 1
                            draw_score()  # Redraw the updated score immediately
                            draw_confetti(player)  # Draw animated confetti for the winner
                            draw_dynamic_lighting()  # Draw lighting borders for occupied squares
                            pygame.display.update()
                            time.sleep(2)  # Show effects for a while
                            auto_restart_game()  # Move to next round automatically

                        player = 2 if player == 1 else 1
                        current_time = pygame.time.get_ticks()  # Reset timer for new player

    draw_timer(time_left)  # Draw the timer for the current player
    draw_score()  # Ensure the score is continuously updated
    draw_button()
    draw_dynamic_lighting()  # Draw dynamic lighting for the board
    pygame.display.update()
