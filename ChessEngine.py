
from ctypes import cast
from importlib.machinery import all_suffixes


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.move_functions = {'p' : self.get_pawn_moves, 'R' : self.get_rook_moves, 'N' : self.get_knight_moves,
                               'B' : self.get_bishop_moves, 'Q' : self.get_queen_moves, 'K' : self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.w_king_loc = (7, 4)
        self.b_king_loc = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.enpass_possible = () #Enpassant coordinates
        self.cur_castle = Castle(True, True, True, True)
        self.castle_log = [Castle(self.cur_castle.wks, self.cur_castle.bks, self.cur_castle.wqs, self.cur_castle.bqs)]

    #Executes the move
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) #Append the move
        self.white_to_move = not self.white_to_move #Swap turns

        if move.piece_moved == 'wK':
            self.w_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.b_king_loc = (move.end_row, move.end_col)
        
        #Pawn promotion
        if move.pawn_promote:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

        #En passant
        if move.enpass_move:
            self.board[move.start_row][move.end_col] = '--'
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.enpass_possible = ((move.start_row + move.end_row)//2, move.start_col)
        else:
            self.enpass_possible = ()

        #Update castling
        if move.castle:
            if move.end_col - move.start_col == 2: #King side
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = '--'
            elif move.end_col - move.start_col == -2: #Queen side
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = '--'

        self.update_castle(move)
        self.castle_log.append(Castle(self.cur_castle.wks, self.cur_castle.bks, self.cur_castle.wqs, self.cur_castle.bqs))

    #Undo last move
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == 'wK':
                self.w_king_loc = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.b_king_loc = (move.start_row, move.start_col)
            
            #Undo en passant
            if move.enpass_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpass_possible = (move.end_row, move.end_col)
            
            #Undo 2 square pawn move
            if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.enpass_possible = ()

            #Undo castle
            self.castle_log.pop()
            self.cur_castle = self.castle_log[-1]

            if move.castle:
                if move.end_col - move.start_col == 2: #King side
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = '--'
                else: #Queen side
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = '--'
                    
    def update_castle(self, move):
        if move.piece_moved == 'wK':
            self.cur_castle.wks = False
            self.cur_castle.wqs = False
        elif move.piece_moved == 'bK':
            self.cur_castle.bks = False
            self.cur_castle.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0: #Left rook
                    self.cur_castle.wqs = False
                elif move.start_col == 7: #Right rook
                    self.cur_castle.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0: #Left rook
                    self.cur_castle.bqs = False
                elif move.start_col == 7: #Right rook
                    self.cur_castle.bks = False

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.pin_and_check()
        temp_castle = Castle(self.cur_castle.wks, self.cur_castle.bks, self.cur_castle.wqs, self.cur_castle.bqs)

        if self.white_to_move:
            king_row = self.w_king_loc[0]
            king_col = self.w_king_loc[1]
        else:
            king_row = self.b_king_loc[0]
            king_col = self.b_king_loc[1]
        
        if self.in_check:
            print("CHECK!")
            if len(self.checks) == 1: #Only one check
                moves = self.all_possible_moves()
                in_check = self.checks[0]
                check_row = in_check[0]
                check_col = in_check[1]
                piece_check = self.board[check_row][check_col] #Piece causing the check
                valid_squares = []

                #If checked by knight, it can't be blocked
                if piece_check[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_sq = (king_row + in_check[2] * i, king_col + in_check[3] * i)
                        valid_squares.append(valid_sq)
                        if valid_sq[0] == check_row and valid_sq[1] == check_col:
                            break
                
                #Remove moves that don't remove check
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else: #Double in_check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.all_possible_moves()

        self.cur_castle = temp_castle
        self.get_castle_moves(king_row, king_col, moves)

        return moves

    def all_possible_moves(self):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves) #Call move function
        
        return moves

    def get_pawn_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move: #White pawn moves
            if self.board[r-1][c] == "--":
                if not piece_pinned or pin_direction == (-1,0):
                    moves.append(Move((r,c), (r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0: #Left capture
                if self.board[r-1][c-1][0] == 'b': #Enemy piece to capture
                    if not piece_pinned or pin_direction == (-1,-1):
                        moves.append(Move((r,c), (r-1,c-1), self.board))
                elif (r-1,c-1) == self.enpass_possible:
                    moves.append(Move((r,c), (r-1,c-1), self.board, enpass_move=True))
            if c+1 <= 7: #Right capture
                if self.board[r-1][c+1][0] == 'b': #Enemy piece to capture
                    if not piece_pinned or pin_direction == (-1,1):
                        moves.append(Move((r,c), (r-1,c+1), self.board))
                elif (r-1,c+1) == self.enpass_possible:
                    moves.append(Move((r,c), (r-1,c+1), self.board, enpass_move=True))
        else: #Black pawn moves
            if self.board[r+1][c] == "--":
                if not piece_pinned or pin_direction == (1,0):
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >= 0: #Left capture
                if self.board[r+1][c-1][0] == 'w': #Enemy piece to capture
                    if not piece_pinned or pin_direction == (1,-1):
                        moves.append(Move((r,c), (r+1,c-1), self.board))
                elif (r+1,c-1) == self.enpass_possible:
                    moves.append(Move((r,c), (r+1,c-1), self.board, enpass_move=True))
            if c+1 <= 7: #Right capture
                if self.board[r+1][c+1][0] == 'w': #Enemy piece to capture
                    if not piece_pinned or pin_direction == (1,1):
                        moves.append(Move((r,c), (r+1,c+1), self.board))
                elif (r+1,c+1) == self.enpass_possible:
                    moves.append(Move((r,c), (r+1,c+1), self.board, enpass_move=True))

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        direction = ((-1,0), (0,-1), (1,0), (0,1)) #up, left, down, right
        enemy_color = 'b' if self.white_to_move else 'w'

        for d in direction:
            for i in range(1, 8):
                end_row = r+d[0]*i
                end_col = c+d[1]*i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": #Empty space valid
                            moves.append(Move((r,c), (end_row,end_col), self.board))
                        elif end_piece[0] == enemy_color: #Capture valid
                            moves.append(Move((r,c), (end_row,end_col), self.board))
                            break
                        else: #Not enemy piece
                            break
                else: #Out of bounds
                    break

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        direction = ((-1,-1), (1,-1), (-1,1), (1,1)) #diagonal directions
        enemy_color = 'b' if self.white_to_move else 'w'

        for d in direction:
            for i in range(1, 8):
                end_row = r+d[0]*i
                end_col = c+d[1]*i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": #Empty space valid
                            moves.append(Move((r,c), (end_row,end_col), self.board))
                        elif end_piece[0] == enemy_color: #Capture valid
                            moves.append(Move((r,c), (end_row,end_col), self.board))
                            break
                        else: #Not enemy piece
                            break
                else: #Out of bounds
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2,-1), (-2,1), (2,-1), (2,1), (-1,-2), (-1,2), (1,-2), (1,2))
        ally_color = 'w' if self.white_to_move else 'b'

        for m in knight_moves:
            end_row = r+m[0]
            end_col = c+m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color: #Empty space or enemy
                        moves.append(Move((r,c), (end_row,end_col), self.board))

    def get_king_moves(self, r, c, moves):
        direction = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        ally_color = 'w' if self.white_to_move else 'b'

        for i in range(8):
            end_row = r+direction[i][0]
            end_col = c+direction[i][1]
            
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color: #Empty space or enemy
                    if ally_color == 'w':
                        self.w_king_loc = (end_row, end_col)
                    else:
                        self.b_king_loc = (end_row, end_col)

                    in_check, pins, checks = self.pin_and_check()
                    
                    if not in_check:
                        moves.append(Move((r,c), (end_row,end_col), self.board))
                    
                    if ally_color == 'w':
                        self.w_king_loc = (r, c)
                    else:
                        self.b_king_loc = (r, c)

    def get_castle_moves(self, r, c, moves):
        in_check, pins, checks = self.pin_and_check()

        if in_check:
            return
        if (self.white_to_move and self.cur_castle.wks) or (not self.white_to_move and self.cur_castle.bks):
            if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                if (not (r, c+1) in checks) and (not (r, c+2) in checks):
                    moves.append(Move((r,c), (r,c+2), self.board, castle=True))
        if (self.white_to_move and self.cur_castle.wqs) or (not self.white_to_move and self.cur_castle.bqs):
            if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
                if (not (r, c-1) in checks) and (not (r, c-2) in checks):
                    moves.append(Move((r,c), (r,c-2), self.board, castle=True))
                    
    def pin_and_check(self):
        pins = []
        checks = [] #Squares where check is applied
        in_check = False

        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.w_king_loc[0]
            start_col = self.w_king_loc[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.b_king_loc[0]
            start_col = self.b_king_loc[1]
        
        #Check for pins and checks
        direction = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))

        for i in range(len(direction)):
            d = direction[i]
            possible_pin = ()
            for j in range(1, 8):
                end_row = start_row + d[0] * j
                end_col = start_col + d[1] * j

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K': #Piece could be pinned
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else: #Not pinned
                            break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1] #What piece

                        if(0 <= i <= 3 and type == 'R') or (4 <= i <= 7 and type == 'B') or \
                            (j == 1 and type == 'p' and ((enemy_color == 'w' and 6 <= i <= 7) or (enemy_color == 'b' and 4 <= i <= 5))) or \
                            (type == 'Q') or (j == 1 and type == 'K'):
                            if possible_pin == (): #No pin == in in_check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else: #Piece guarding is pinned
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else: #Out of bounds
                    break
        
        #Check for knight checks
        knight_moves = ((-2,-1), (-2,1), (2,-1), (2,1), (-1,-2), (-1,2), (1,-2), (1,2))

        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))

        return in_check, pins, checks

class Castle():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

    #Chess notations
    ranks_to_rows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    files_to_cols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    rows_to_ranks = {v : k for k, v in ranks_to_rows.items()}
    cols_to_files = {v : k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, enpass_move=False, castle=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        #Pawn promotion
        self.pawn_promote = (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7)
        #En passant
        self.enpass_move = enpass_move
        if self.enpass_move:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'
        #Castle
        self.castle = castle

        self.move_id = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col

    #Override
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_notation(self):
        #You can make it like real Chess notations
        return self.get_rank_file(self.start_row, self.start_col) + ' ' + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]