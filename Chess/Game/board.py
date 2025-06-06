import pygame
import sys

# Constants
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)


# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board(WIN)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()