import pygame, os, sys


#
#Added castling and en passant
#

# Constants
WIDTH, HEIGHT = 960, 960
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT // COLS
piece_values = {
    "k" : 0,
    "q" : 9,
    "r" : 5,
    "n" : 3,
    "b" : 3,
    "p" : 1

}

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)


# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

def to_chess_coords(row, col):
    """
    Convert internal board coordinates (row, col) to standard chess notation.
    row: 0 (top, rank 8) to 7 (bottom, rank 1)
    col: 0 (left, file 'a') to 7 (right, file 'h')
    Returns: a string like 'e4'
    """
    file = chr(ord('a') + col)
    rank = str(8 - row)
    return file + rank


def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = BEIGE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

PIECE_FOLDER   = "Chess\Game\Pieces"          # where you saved white_rook.png etc.
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
    if fen.split()[1] == 'w':
        white_turn =True
    else:
        white_turn = False
    
    castling_rights = []
    en_passant = fen.split()[3]
    rule_50 = int(fen.split()[4])
    turn = int(fen.split()[5])

    for char in ['K','Q','k','q']:
        if char in fen.split()[2]:
            castling_rights.append(True)
        else:
            castling_rights.append(False)


    board = []
    for rank in piece_part.split("/"):
        row = []
        for ch in rank:
            if ch.isdigit():                 # a run of empty squares
                row.extend([None] * int(ch))
            else:                            # a piece letter
                row.append(ch)
        board.append(row)
    return board, white_turn, castling_rights, en_passant, rule_50, turn


def is_white(piece): return piece.isupper()
def is_black(piece): return piece.islower()
def is_opponent(piece1, piece2):
    if piece1 is None or piece2 is None:
        return False
    return is_white(piece1) != is_white(piece2)

def generate_fen(board, white_turn, castling_rights, en_passant, rule_50, turn):
    # Piece placement
    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for cell in row:
            if cell is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    piece_placement = "/".join(fen_rows)

    # Active color
    active_color = "w" if white_turn else "b"

    # Castling rights
    castling_chars = ['K', 'Q', 'k', 'q']
    castling_part = "".join([c for c, allowed in zip(castling_chars, castling_rights) if allowed])
    if castling_part == "":
        castling_part = "-"

    # En passant target
    en_passant_part = en_passant if en_passant else "-"

    # Full FEN
    return f"{piece_placement} {active_color} {castling_part} {en_passant_part} {rule_50} {turn}"


def get_legal_moves(board,  castling_rights, en_passant,  row, col):

    piece = board[row][col]

    if is_white(piece):
        castling_check = castling_rights[:2]
    else:
        castling_check = castling_rights[2:]

    if piece is None:
        return []

    color = 'white' if is_white(piece) else 'black'
    directions = []
    moves = []

    def add_move(r, c):
        if 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target is None or is_opponent(piece, target):
                moves.append((r, c))

    # PAWN
    if piece.upper() == 'P':
        dir = -1 if color == 'white' else 1
        start_row = 6 if color == 'white' else 1

        # forward
        if board[row + dir][col] is None:
            moves.append((row + dir, col))
            if row == start_row and board[row + 2 * dir][col] is None:
                moves.append((row + 2 * dir, col))

        # captures
        for dc in [-1, 1]:
            r, c = row + dir, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] and is_opponent(piece, board[r][c]):
                moves.append((r, c))
        
        # En passant written by chat!
        print(en_passant)
        if en_passant != '-':
            ep_col = ord(en_passant[0]) - ord('a')
            ep_row = 8 - int(en_passant[1])

            if ep_row == row + dir and abs(ep_col - col) == 1:
                moves.append((ep_row, ep_col))
               

    # KNIGHT
    elif piece.upper() == 'N':
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            r, c = row + dr, col + dc
            add_move(r, c)

    # KING
    elif piece.upper() == 'K':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    add_move(row + dr, col + dc)

        if is_white(piece):
            castling_dir = -2
            castling_row = 7
        else:
            castling_dir = -2
            castling_row = 0
        
        if castling_check[0] and board[castling_row][5] == None and board[castling_row][6] == None:
            print('you can castle!')
            add_move(row, col-castling_dir)
        if castling_check[1] and board[castling_row][1] == None and board[castling_row][2] == None and board[castling_row][3] == None:
            add_move(row, col+castling_dir)
            
            print('you can castle!')

    # SLIDING PIECES
    elif piece.upper() in ['R', 'B', 'Q']:
        if piece.upper() in ['R', 'Q']:
            directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Rook
        if piece.upper() in ['B', 'Q']:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Bishop

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif is_opponent(piece, board[r][c]):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    return moves

def highlight_moves(win, moves):
    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    s.fill((255, 255, 0, 100))  # translucent yellow
    for r, c in moves:
        win.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))


#START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#START_FEN = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w kq - 0 1"
START_FEN = "r3k2r/ppp3pp/2nqbn2/2bppppp/2PPPPPP/2NBBN2/PP1Q2PP/R3K2R b KQkq - 0 9"

piece_images = load_piece_images()

def main():
    clock = pygame.time.Clock()
    run = True
    
    selected_square = None
    board, white_turn, castling_rights, en_passant, rule_50, turn  = parse_fen(START_FEN)

    while run:

        clock.tick(60)  # 60 FPS
        

        #Piece values calculation: (useless to keep them here tho)
            
        white_piece_count = 0
        black_piece_count = 0
        for row in board:
            for value in row:
                if value is not None:
                    if value.islower():
                        white_piece_count += piece_values[value]
                    else:
                        black_piece_count += piece_values[value.lower()]


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                print(row,col,x,y)

                if selected_square is None:
                    # First click – select the piece
                    if board[row][col] is not None:
                        if white_turn and board[row][col].isupper():
                            selected_square = (row, col)
                            available_moves = get_legal_moves(board, castling_rights, en_passant, row, col)
                        elif (not white_turn) and board[row][col].islower():
                            selected_square = (row, col)
                            available_moves = get_legal_moves(board, castling_rights, en_passant, row, col)

                    

                elif (row,col) in available_moves:
                    # Second click – try to move the piece
                    from_row, from_col = selected_square
                    piece = board[from_row][from_col]

                    new_en_pass = '-'
                    # King or rook moved? Update castling rights accordingly

                    # White king moves
                    if piece == 'K':

                        if col == 2 and castling_rights[0]:
                            board[7][0] = None
                            board[7][3] = 'R'
                        if col == 6 and castling_rights[1]:
                            board[7][7] = None
                            board[7][5] = 'R'
                        
                        castling_rights[0] = False  # White kingside
                        castling_rights[1] = False  # White queenside
                    # Black king moves
                    elif piece == 'k':

                        if col == 2 and castling_rights[2]:
                            board[0][0] = None
                            board[0][3] = 'r'
                        if col == 6 and castling_rights[3]:
                            board[0][7] = None
                            board[0][5] = 'r'
                            
                        castling_rights[2] = False  # Black kingside
                        castling_rights[3] = False  # Black queenside

                    # White rook moves
                    elif piece == 'R':
                        if from_row == 7 and from_col == 0:  # a1 rook
                            castling_rights[1] = False  # White queenside
                        elif from_row == 7 and from_col == 7:  # h1 rook
                            castling_rights[0] = False  # White kingside

                    # Black rook moves
                    elif piece == 'r':
                        if from_row == 0 and from_col == 0:  # a8 rook
                            castling_rights[3] = False  # Black queenside
                        elif from_row == 0 and from_col == 7:  # h8 rook
                            castling_rights[2] = False  # Black kingside
                    
                    elif piece == 'P':
                        if from_row == 6 and row == 4:
                            new_en_pass = to_chess_coords(row +1, col)
                        if to_chess_coords(row, col) == en_passant:
                            board[row+1][col] = None
                    elif piece == 'p':
                        if from_row == 1 and row == 3:
                            new_en_pass = to_chess_coords(row - 1, col)
                        if to_chess_coords(row, col) == en_passant:
                            board[row-1][col] = None


                    # Move the piece (without legality check)
                    board[from_row][from_col] = None
                    board[row][col] = piece

                    print('white score: ', white_piece_count, ', black score: ', black_piece_count)
                    if not white_turn:
                        print(turn)
                        turn +=1
                    white_turn = not white_turn
                    actual_fen = generate_fen(board, white_turn, castling_rights, new_en_pass, rule_50, turn)
                    en_passant = new_en_pass
                    selected_square = None  # reset selection
                    print(actual_fen)
                    available_moves = []

                else: 
                    selected_square = None  # reset selection
                    available_moves = []


        draw_board(WIN)
        draw_pieces(WIN, board, piece_images)
        if selected_square:
            r, c = selected_square
            highlight_color = (50, 100, 120, 100)  # light green
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(highlight_color)
            WIN.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            highlight_moves(WIN, available_moves)
        pygame.display.update()

    pygame.quit()
    sys.exit()





if __name__ == "__main__":
    main()