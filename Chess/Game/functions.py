import pygame
import sys
import os

# Constants
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)

# Constants
PIECE_FOLDER = "Chess\Game\Pieces"
PIECE_SIZE = 60  # Original size doesn't matter much if we scale
PIECES = ['K', 'Q', 'R', 'B', 'N', 'P']
SQUARE_SIZE = 60  # Should match your board square size

def draw_pieces(win, board, piece_images):
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row][col]
            if piece:
                win.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))


# Mapping codes like 'wP' → 'white_pawn.png'
def load_piece_images():
    piece_images = {}
    for color in ['white', 'black']:
        for piece in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']:
            code = color + '_' + piece
            print(piece[0])
            path = os.path.join(PIECE_FOLDER, f"{color}_{piece}.png")
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
            piece_images[code] = image
    return piece_images



def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
