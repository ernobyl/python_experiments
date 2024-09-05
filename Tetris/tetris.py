import pygame
import random

pygame.init()

# screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
COLS = SCREEN_WIDTH // BLOCK_SIZE

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# block shapes
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],  # T-shape

    [[0, 1, 1],
     [1, 1, 0]],  # Z-shape

    [[1, 1, 0],
     [0, 1, 1]],  # S-shape

    [[1, 1, 1, 1]],  # I-shape

    [[1, 1],
     [1, 1]],  # O-shape

    [[1, 1, 1],
     [1, 0, 0]],  # L-shape

    [[1, 1, 1],
     [0, 0, 1]]   # J-shape
]

SHAPE_COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE]

# game grid
grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]


class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def can_move(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or grid[new_y][new_x] != BLACK:
                        return False
        return True

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color


def draw_grid(screen):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def clear_rows():
    global grid
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    cleared_rows = ROWS - len(new_grid)
    grid = [[BLACK for _ in range(COLS)] for _ in range(cleared_rows)] + new_grid
    return cleared_rows


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    current_piece = Piece()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            if current_piece.can_move(0, 1):
                current_piece.y += 1
            else:
                current_piece.lock()
                score += clear_rows()
                current_piece = Piece()
                if not current_piece.can_move(0, 0):
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_piece.can_move(-1, 0):
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT and current_piece.can_move(1, 0):
                    current_piece.x += 1
                if event.key == pygame.K_DOWN and current_piece.can_move(0, 1):
                    current_piece.y += 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not current_piece.can_move(0, 0):
                        current_piece.rotate()  # Undo rotation if invalid

        draw_grid(screen)

        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece.color,
                                     ((current_piece.x + x) * BLOCK_SIZE, (current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE,
                                      BLOCK_SIZE), 0)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
