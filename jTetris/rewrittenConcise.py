import pygame, random

pygame.init()

# Constants
SW, SH, BW, BH, CS, BW, FW = 500, 600, 300, 600, 30, 1, 'Arial'
LINE_COLOR, BLACK, D_GREY, WHITE, D_RED = (255, 165, 0), (0, 0, 0), (50, 50, 50), (255, 255, 255), (255, 50, 75)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]
SHAPES = [[[1, 1, 1, 1]], [[1, 1, 1], [0, 1, 0]], [[1, 1, 1], [1, 0, 0]], [[1, 1, 1], [0, 0, 1]], [[1, 1], [1, 1]], [[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]]]

# Screen setup
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption('Tetris')
background_img = pygame.image.load('background.jpg')
background_img = pygame.transform.scale(background_img, (SW, SH))
font, mfont, clock = pygame.font.SysFont(FW, 24), pygame.font.SysFont('Calibri', 24, bold=True), pygame.time.Clock()


class Tetromino:
    def __init__(self, x, y): self.x, self.y, self.shape, self.color = x, y, random.choice(SHAPES), random.choice(COLORS)
    def rotate(self): self.shape = [list(row) for row in zip(*self.shape[::-1])]
    def move(self, dx, dy): self.x, self.y = self.x + dx, self.y + dy


def create_board(): return [[0] * (BW // CS) for _ in range(BH // CS)]


def valid_move(board, tetro, dx, dy):
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = tetro.x + x + dx, tetro.y + y + dy
                if new_x < 0 or new_x >= len(board[0]) or new_y >= len(board) or board[new_y][new_x]: return False
    return True


def lock_tetromino(board, tetro):
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell: board[tetro.y + y][tetro.x + x] = tetro.color


def clear_lines(board):
    lines = [y for y, row in enumerate(board) if all(row)]
    if lines:
        for y in lines: board[y] = [LINE_COLOR] * len(board[0])
        draw_board(screen, board); pygame.display.flip(); pygame.time.delay(75)
        for y in lines: board[y] = [WHITE] * len(board[0])
        draw_board(screen, board); pygame.display.flip(); pygame.time.delay(95)
        board = [row for y, row in enumerate(board) if y not in lines]
        board = [[0] * len(board[0]) for _ in range(len(lines))] + board
    return board, len(lines)


def update_score(lines, score): return score + lines * 100, score // 1000 + 1


def draw_gradient_rect(screen, rect, color):
    dark, light = tuple(max(0, c - 50) for c in color), tuple(min(255, c + 50) for c in color)
    for i in range(CS):
        ratio = i / CS
        inter_color = [int(light[j] * (1 - ratio) + dark[j] * ratio) for j in range(3)]
        pygame.draw.line(screen, inter_color, (rect.left, rect.top + i), (rect.right, rect.top + i))


def draw_tetromino(screen, tetro):
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((tetro.x + x) * CS, (tetro.y + y) * CS, CS, CS)
                draw_gradient_rect(screen, rect, tetro.color)
                pygame.draw.rect(screen, D_RED, rect, BW)


def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CS, y * CS, CS, CS)
            pygame.draw.rect(screen, D_GREY, rect, 1)
            if cell: draw_gradient_rect(screen, rect, cell)


def draw_status(screen, score, level, lines, next_tetro):
    for i, text in enumerate([f'Score: {score}', f'Level: {level}', f'Lines: {lines}', 'Next:']):
        screen.blit(mfont.render(text, True, WHITE), (BW + 20, 20 + i * 30))
    for y, row in enumerate(next_tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(BW + 20 + x * CS, 140 + y * CS, CS, CS)
                draw_gradient_rect(screen, rect, next_tetro.color)
                pygame.draw.rect(screen, D_RED, rect, BW)


def draw_game_over(screen):
    for text, offset in [('GAME OVER', -50), ('Press spacebar to play again!', 10)]:
        rendered = font.render(text, True, (255, 0, 0) if 'OVER' in text else WHITE)
        screen.blit(rendered, (SW // 2 - rendered.get_width() // 2, SH // 2 + offset))
    pygame.display.flip()


def main():
    def reset(): return create_board(), Tetromino(BW // (2 * CS), 0), Tetromino(BW // (2 * CS), 0), 0, 1, 0
    board, curr_tetro, next_tetro, score, level, lines = reset()
    running, game_over, fall_time, fall_speed = True, False, 0, 500

    while running:
        screen.blit(background_img, (0, 0))
        fall_time += clock.get_rawtime(); clock.tick()

        if not game_over:
            if fall_time > fall_speed:
                fall_time = 0
                if not valid_move(board, curr_tetro, 0, 1):
                    lock_tetromino(board, curr_tetro)
                    board, cleared = clear_lines(board)
                    score, level = update_score(cleared, score); lines += cleared
                    curr_tetro, next_tetro = next_tetro, Tetromino(BW // (2 * CS), 0)
                    if not valid_move(board, curr_tetro, 0, 0): game_over = True
                else: curr_tetro.move(0, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and valid_move(board, curr_tetro, -1, 0): curr_tetro.move(-1, 0)
                    elif event.key == pygame.K_RIGHT and valid_move(board, curr_tetro, 1, 0): curr_tetro.move(1, 0)
                    elif event.key == pygame.K_DOWN and valid_move(board, curr_tetro, 0, 1): curr_tetro.move(0, 1)
                    elif event.key == pygame.K_UP:
                        curr_tetro.rotate()
                        if not valid_move(board, curr_tetro, 0, 0):
                            for _ in range(3): curr_tetro.rotate()
                    elif event.key == pygame.K_SPACE:
                        while valid_move(board, curr_tetro, 0, 1): curr_tetro.move(0, 1)
                        lock_tetromino(board, curr_tetro)
                        board, cleared = clear_lines(board)
                        score, level = update_score(cleared, score); lines += cleared
                        curr_tetro, next_tetro = next_tetro, Tetromino(BW // (2 * CS), 0)
                        if not valid_move(board, curr_tetro, 0, 0): game_over = True

            draw_board(screen, board)
            draw_tetromino(screen, curr_tetro)
            draw_status(screen, score, level, lines, next_tetro)
        else:
            draw_game_over(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    board, curr_tetro, next_tetro, score, level, lines = reset()
                    game_over = False

        pygame.display.flip()
    pygame.quit()


# Uncomment to run the game
main()
