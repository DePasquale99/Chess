import pygame, os, sys


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

PIECE_FOLDER   = "Chess\Game\Pieces"          # where you saved white_rook.png etc.
SQUARE_SIZE    = 60                # must match your board squares
FEN_TO_FILE = {                    # maps a single FEN char → filename
    "K": "white_king.png",
    "Q": "white_queen.png",
    "R": "white_rook.png",
    "B": "white_bishop.png",
    "N": "white_knight.png",
    "P": "white_pawn.png",
    "k": "black_king.png",
    "q": "black_queen.png",
    "r": "black_rook.png",
    "b": "black_bishop.png",
    "n": "black_knight.png",
    "p": "black_pawn.png",
}

def load_piece_images():
    """Load every required PNG once and keep them in a dict keyed by the FEN char."""
    images = {}
    for fen_char, filename in FEN_TO_FILE.items():
        path   = os.path.join(PIECE_FOLDER, filename)
        img    = pygame.image.load(path).convert_alpha()
        images[fen_char] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
    return images

def draw_pieces(win, board, images):
    """Blit every non-empty square’s image to the correct pixel position."""
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            if piece:
                win.blit(images[piece], (col_idx * SQUARE_SIZE, row_idx * SQUARE_SIZE))


def parse_fen(fen: str):
    """
    Returns a list[list[str | None]] where each inner list is a rank (row) from 0 (top, Black side)
    to 7 (bottom, White side). Empty squares are None. Only the first field of the FEN
    (the piece placement) is needed for drawing.
    """
    piece_part = fen.split()[0]      # we ignore the move/clock fields for now
    board = []
    for rank in piece_part.split("/"):
        row = []
        for ch in rank:
            if ch.isdigit():                 # a run of empty squares
                row.extend([None] * int(ch))
            else:                            # a piece letter
                row.append(ch)
        board.append(row)
    return board

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# once, at program start
piece_images = load_piece_images()
board        = parse_fen(START_FEN)

# inside your game loop, after draw_board(WIN)
def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board(WIN)
        draw_pieces(WIN, board, piece_images)

        pygame.display.update()

    pygame.quit()
    sys.exit()





if __name__ == "__main__":
    main()