import pygame as py
import ChessEngine

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}

def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']

    for piece in pieces:
        IMAGES[piece] = py.transform.scale(py.image.load("VS Code/Python/Chess/images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))

def main():
    py.init()

    win = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    win.fill(py.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False #Flag variable for moves
    run = True
    sq_select = ()
    player_click = []

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

                if sq_select == (row, col):
                    sq_select = ()
                    player_click = []
                else:
                    sq_select = (row, col)
                    player_click.append(sq_select)
                if len(player_click) == 2:
                    move = ChessEngine.Move(player_click[0], player_click[1], gs.board)
                    print(move.get_notation())

                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True
                            #Reset
                            sq_select = ()
                            player_click = []
                    if not move_made:
                        player_click = [sq_select]
            #Key
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r: #Undo move when 'R' is pressed
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(win, gs)
        clock.tick(FPS)
        py.display.flip()

def draw_game_state(win, gs):
    draw_board(win)
    draw_pieces(win, gs.board)

def draw_board(win):
    WHITE = (255, 255, 255)
    BLACK = (100, 100, 100)
    colors = [py.Color(WHITE), py.Color(BLACK)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            py.draw.rect(win, color, py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(win, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                win.blit(IMAGES[piece], py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()