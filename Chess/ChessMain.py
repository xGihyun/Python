import pygame as py
import ChessEngine

WIDTH = 800
HEIGHT = 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 120
IMAGES = {}

WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
RED = (255, 0, 0)

#BOARD COLORS
COLORS = [py.Color(WHITE), py.Color(BLACK)]

def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']

    for piece in pieces:
        IMAGES[piece] = py.transform.smoothscale(py.image.load("VS Code/Python/Chess/piece/alpha/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

def main():
    py.init()

    win = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    win.fill(py.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False #Flag variable for moves
    animate = False #Flag variable for animations
    run = True
    sq_selected = ()
    player_click = []
    notation = []

    load_images()

    while run:
        for e in py.event.get():
            if e.type == py.QUIT:
                run = False
            #Mouse
            elif e.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sq_selected == (row, col):
                    sq_selected = ()
                    player_click = []
                else:
                    sq_selected = (row, col)
                    player_click.append(sq_selected)
                if len(player_click) == 2:
                    move = ChessEngine.Move(player_click[0], player_click[1], gs.board)

                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True
                            animate = True
                            #Reset
                            sq_selected = ()
                            player_click = []

                            notation.append(move.get_notation())
                            
                            if len(notation)%2 == 0:
                                print(notation[0] + ' ' + notation[1])
                                notation = []
                            
                    if not move_made:
                        player_click = [sq_selected]
            #Key
            elif e.type == py.KEYDOWN:
                if e.key == py.K_u: #Undo move when 'U' is pressed
                    gs.undo_move()
                    move_made = True
                    animate = False
                    if len(notation) > 0:
                        notation.pop()
                if e.key == py.K_r: #Reset board when 'R' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_click = []
                    notation = []
                    move_made = False
                    animate = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], win, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(win, gs, valid_moves, sq_selected)
        clock.tick(FPS)
        py.display.flip()

#Draw stuff
def draw_game_state(win, gs, valid_moves, sq_selected):
    draw_board(win)
    sq_highlights(win, gs, valid_moves, sq_selected)
    draw_pieces(win, gs.board)

def draw_board(win):

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = COLORS[((r+c)%2)]
            py.draw.rect(win, color, py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(win, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                win.blit(IMAGES[piece], py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#Square highlights
def sq_highlights(win, gs, valid_moves, sq_selected):
    s = py.Surface((SQ_SIZE, SQ_SIZE))

    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            #Highlight selected square
            s.set_alpha(100)
            s.fill(py.Color(BLUE))
            win.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

            #Highlight valid moves
            s.fill(py.Color(LIGHT_BLUE))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    win.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

    #Highlight if in check
    if gs.in_check:
        s.set_alpha(150)
        s.fill(py.Color(RED))
        king_row, king_col = (gs.w_king_loc if gs.white_to_move else gs.b_king_loc)
        win.blit(s, (king_col*SQ_SIZE, king_row*SQ_SIZE))

#Animation
def animate_move(move, win, board, clock):
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    fpsq = 10 #Frames per square
    frame_count = (abs(dR) + abs(dC)) * fpsq//(abs(dR) + abs(dC))

    for frame in range(frame_count+1):
        r, c = (move.start_row + dR * frame/frame_count, move.start_col + dC * frame/frame_count)
        draw_board(win)
        draw_pieces(win, board)

        color = COLORS[((move.end_row+move.end_col)%2)]
        end_square = py.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        py.draw.rect(win, color, end_square)

        #Draw captured piece
        if move.piece_captured != '--' and not move.enpass_move:
            win.blit(IMAGES[move.piece_captured], end_square)
        
        #Draw moving piece
        win.blit(IMAGES[move.piece_moved], py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        py.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()