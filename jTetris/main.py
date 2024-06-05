import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 1010
BOARD_WIDTH = 500
BOARD_HEIGHT = 1000
CELL_SIZE = 50

# Width of border on tetromino cells
BORDER_WIDTH = 1

# Define colors
LINE_CLEAR_COLOR = (255, 165, 0)
BLACK = (0, 0, 0)
DARK_GREY = (50, 50, 50)
WHITE = (255, 255, 255)
DARK_RED = (255, 50, 75)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Load background image
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Define fonts
font = pygame.font.SysFont('Arial', 24)
modern_font = pygame.font.SysFont('Calibri', 24, bold=True)

# Clock for controlling the frame rate
clock = pygame.time.Clock()


class Tetromino:
    """
    Class defining the layouts and behavior of the tetromino pieces
    """
    SHAPES = [
        [[1, 1, 1, 1]],  # I shape
        [[1, 1, 1], [0, 1, 0]],  # T shape
        [[1, 1, 1], [1, 0, 0]],  # L shape
        [[1, 1, 1], [0, 0, 1]],  # J shape
        [[1, 1], [1, 1]],  # O shape
        [[1, 1, 0], [0, 1, 1]],  # S shape
        [[0, 1, 1], [1, 1, 0]]   # Z shape
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(self.SHAPES)
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def create_board():
    return [[0] * (BOARD_WIDTH // CELL_SIZE) for _ in range(BOARD_HEIGHT // CELL_SIZE)]


def is_valid_move(board, tetromino, dx, dy):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetromino.x + x + dx
                new_y = tetromino.y + y + dy
                if new_x < 0 or new_x >= len(board[0]) or new_y >= len(board) or board[new_y][new_x]:
                    return False
    return True


def lock_tetromino(board, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                board[tetromino.y + y][tetromino.x + x] = tetromino.color


def clear_lines(board):
    lines_to_clear = [y for y, row in enumerate(board) if all(row)]
    if lines_to_clear:
        for y in lines_to_clear:
            board[y] = [LINE_CLEAR_COLOR] * len(board[0])
        draw_board(screen, board)
        pygame.display.flip()
        pygame.time.delay(75)  # Short delay to show the line clear effect

        for y in lines_to_clear:
            board[y] = [(255, 255, 255)] * len(board[0])
        draw_board(screen, board)
        pygame.display.flip()
        pygame.time.delay(95)  # Short delay to show the line clear effect

        board = [row for y, row in enumerate(board) if y not in lines_to_clear]
        new_board = [[0] * len(board[0]) for _ in range(len(lines_to_clear))]
        board = new_board + board
    return board, len(lines_to_clear)


def update_level_and_score(lines, score, level):
    score += lines * 100
    level = score // 1000 + 1
    return score, level


def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, DARK_GREY, rect, 1)
            if cell:
                draw_gradient_rect(screen, rect, cell)


def draw_gradient_rect(screen, rect, color):
    """Draw a rectangle with a gradient effect."""
    color_dark = tuple(max(0, c - 50) for c in color)
    color_light = tuple(min(255, c + 50) for c in color)

    for i in range(CELL_SIZE):
        ratio = i / CELL_SIZE
        intermediate_color = (
            int(color_light[0] * (1 - ratio) + color_dark[0] * ratio),
            int(color_light[1] * (1 - ratio) + color_dark[1] * ratio),
            int(color_light[2] * (1 - ratio) + color_dark[2] * ratio)
        )
        pygame.draw.line(screen, intermediate_color, (rect.left, rect.top + i), (rect.right, rect.top + i))


def draw_tetromino(screen, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((tetromino.x + x) * CELL_SIZE, (tetromino.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                draw_gradient_rect(screen, rect, tetromino.color)
                pygame.draw.rect(screen, DARK_RED, rect, BORDER_WIDTH)


def draw_status(screen, score, level, lines, next_tetromino):
    score_text = modern_font.render(f'Score: {score}', True, WHITE)
    level_text = modern_font.render(f'Level: {level}', True, WHITE)
    lines_text = modern_font.render(f'Lines: {lines}', True, WHITE)
    next_text = modern_font.render('Next:', True, WHITE)

    screen.blit(score_text, (BOARD_WIDTH + 20, 20))
    screen.blit(level_text, (BOARD_WIDTH + 20, 50))
    screen.blit(lines_text, (BOARD_WIDTH + 20, 80))
    screen.blit(next_text, (BOARD_WIDTH + 20, 110))

    for y, row in enumerate(next_tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(BOARD_WIDTH + 20 + x * CELL_SIZE, 140 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                draw_gradient_rect(screen, rect, next_tetromino.color)
                pygame.draw.rect(screen, DARK_RED, rect, BORDER_WIDTH)


def draw_game_over_screen(screen, font):
    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    restart_text = font.render('Press spacebar to play again!', True, (255, 255, 255))
    ctrl_text = font.render('Arrow keys to move. Space to drop!', True, (255, 255, 255))

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(ctrl_text, (SCREEN_WIDTH // 2 - ctrl_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
    pygame.display.flip()


def main():
    def reset_game():
        return create_board(), Tetromino(BOARD_WIDTH // (2 * CELL_SIZE), 0), Tetromino(BOARD_WIDTH // (2 * CELL_SIZE), 0), 0, 1, 0

    board, current_tetromino, next_tetromino, score, level, lines_cleared = reset_game()

    running = True
    game_over = False
    fall_time = 0
    fall_speed = 500

    while running:
        screen.blit(background_image, (0, 0))
        fall_time += clock.get_rawtime()
        clock.tick()

        if not game_over:
            if fall_time > fall_speed:
                fall_time = 0
                if not is_valid_move(board, current_tetromino, 0, 1):
                    lock_tetromino(board, current_tetromino)
                    board, lines = clear_lines(board)
                    score, level = update_level_and_score(lines, score, level)
                    lines_cleared += lines
                    current_tetromino = next_tetromino
                    next_tetromino = Tetromino(BOARD_WIDTH // (2 * CELL_SIZE), 0)
                    if not is_valid_move(board, current_tetromino, 0, 0):
                        game_over = True
                else:
                    current_tetromino.move(0, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and is_valid_move(board, current_tetromino, -1, 0):
                        current_tetromino.move(-1, 0)
                    elif event.key == pygame.K_RIGHT and is_valid_move(board, current_tetromino, 1, 0):
                        current_tetromino.move(1, 0)
                    elif event.key == pygame.K_DOWN and is_valid_move(board, current_tetromino, 0, 1):
                        current_tetromino.move(0, 1)
                    elif event.key == pygame.K_UP:
                        current_tetromino.rotate()
                        if not is_valid_move(board, current_tetromino, 0, 0):
                            current_tetromino.rotate()
                            current_tetromino.rotate()
                            current_tetromino.rotate()
                    elif event.key == pygame.K_SPACE:
                        while is_valid_move(board, current_tetromino, 0, 1):
                            current_tetromino.move(0, 1)
                        lock_tetromino(board, current_tetromino)
                        board, lines = clear_lines(board)
                        score, level = update_level_and_score(lines, score, level)
                        lines_cleared += lines
                        current_tetromino = next_tetromino
                        next_tetromino = Tetromino(BOARD_WIDTH // (2 * CELL_SIZE), 0)
                        if not is_valid_move(board, current_tetromino, 0, 0):
                            game_over = True

            draw_board(screen, board)
            draw_tetromino(screen, current_tetromino)
            draw_status(screen, score, level, lines_cleared, next_tetromino)
        else:
            draw_game_over_screen(screen, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    board, current_tetromino, next_tetromino, score, level, lines_cleared = reset_game()
                    game_over = False

        pygame.display.flip()

    pygame.quit()


# Uncomment the following line to run the game
main()
