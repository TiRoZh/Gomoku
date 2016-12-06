from __future__ import print_function
from itertools import product
from random import shuffle

class Gomoku:
    def __init__(self):
        self.board = generate_board()
        self.game_state = State(self.board)

    def get_state(self):
        return self.game_state
    
    def set_state(self, state):
        self.game_state = state

    def is_over(self):
        return self.game_state.is_over()

    def print_board(self):
        # ugly printing
        board=self.board
        print("\t",end=" ")
        for i in range(1,16):
            print("[" + str(i) + "]", end=" ")
        print("")

        for i in range(0,15):
            print(str(i+1), end="\t")
            for j in range(0,15):
                if (board[i][j] == None):
                    print("[ ]", end=" ")
                if (board[i][j] == True):
                    print("[B] ", end=" ")
                if (board[i][j] == False):
                    print("[W]", end=" ")
            print("")


class State:
    # implement values of states; this should be calculated in successor function
    def __init__(self, board, p1_pieces=[], p2_pieces=[], turn=True):
        self.board = board
        self.turn = turn
        self.p1_pieces = p1_pieces
        self.p2_pieces = p2_pieces
        self.value = (self.calculate_value(p2_pieces)) - (self.calculate_value(p1_pieces))
    
    def get_value(self):
        return self.value
        
    def calculate_value(self, pieces_set):
        scores = [[], [], [], []]
                        
        for piece in pieces_set:
            for i in range(2,6):
                if (check_vertical(pieces_set, piece, i) or
                    check_horizontal(pieces_set, piece, i) or
                    check_diagonal_left(pieces_set, i) or
                    check_diagonal_right(pieces_set, i)):
                    scores[i-2].append(piece)
        
        score = ((10 * len(scores[0])) + (40 * len(scores[1])) +
                 (200 * len(scores[2])) + (500 * len(scores[3])))
        return score
                    

    def add_piece(self, coords):
        if self.turn:
            self.p1_pieces.append(coords)
        else:
            self.p2_pieces.append(coords)

        # we entered coordinates as (x,y)
        # but the board is [y][x]
        self.board[coords[1]-1][coords[0]-1] = self.turn

        self.turn = not self.turn

        return State(self.board, self.p1_pieces, self.p2_pieces, self.turn)


    def get_pieces(self):
        pieces = self.p1_pieces+self.p2_pieces
        return pieces

    def is_piece(self, piece):
        return ((piece in self.p1_pieces) or (piece in self.p2_pieces))

    def is_over(self):
        for piece in self.get_pieces():
            if self.five_in_a_row(piece):
                return True
        return False

    def get_turn(self):
        return self.turn

    def set_turn(self,new_turn):
        self.turn=new_turn

    def five_in_a_row(self,piece):
        # we have a piece as a tuple (x,y)
        if piece in self.p1_pieces:
            return (check_vertical(self.p1_pieces,piece,5) or check_horizontal(self.p1_pieces,piece,5)
            or check_diagonal_left(self.p1_pieces,5) or check_diagonal_right(self.p1_pieces,5) )
        else:
            return (check_vertical(self.p2_pieces,piece,5) or check_horizontal(self.p2_pieces,piece,5)
            or check_diagonal_left(self.p2_pieces,5) or check_diagonal_right(self.p2_pieces,5))


def successor(state):
    # successor function, we haven't implemented values
    # this needs to be implemented in State class
    moves_to_check = []
    successors = []

    pieces = state.get_pieces()
    for piece in pieces:
        for i in range(piece[0]-4,piece[0]+4, 1):
            for j in range(piece[1]-4, piece[1]+4, 1):
                if (i < 0 or i > 14 or j < 0 or j > 14):
                    break
                if ((i,j) in state.get_pieces()):
                    break

                successors.append(state.add_piece((i,j)))

    return successors



def generate_board():
    # generate the basic 15x15 board

    board = []
    for i in range(0,15):
        board.append([])

    for ele in board:
        for i in range(0,15):
            ele.append(None)

    return board

def start_game():
    game = Gomoku()
    count=0
    ##generates list of all possibilities,only for testing atm
    coordinates = list(product(range(15), range(15)))
    #shuffles them, this is only for testing atm
    shuffle(coordinates)
    while  game.get_state().is_over()==False:
        if count%2==0:
            game.get_state().set_turn(True)
            game.set_state(game.get_state().add_piece(coordinates[count]))
            game.print_board()
            count+=1
        else:
            game.get_state().set_turn(False)
            game.set_state(game.get_state().add_piece(tuple(int(x.strip()) for x in input().split(','))))
            game.print_board()
            count+=1
        print(game.get_state().get_value())


#amount check is the amount u want to check for, this is what u wanted Tim
def check_horizontal(player,piece,amount_check):
    #get all tuples where the y_coordinate is teh same as piece
    tuples=[t for t in player if t[1] == piece[1]]
    #create two lists, one with all the x_coords and one with y_coordinates
    zipped=list(zip(*tuples))
    #just get the x_coordinates since we are looking for horizontal rows
    x_coords=zipped[0]

    #if the number of consecutive x_coordinates is greater than 5, return true otherwise False
    return (s(x_coords)>=amount_check)



def check_vertical(player,piece,amount_check):
    #get all tuples where the x_coordinate is teh same as piece
    tuples=[t for t in player if t[0] == piece[0]]
    #create two lists, one with all the x_coords and one with y_coordinates
    zipped=list(zip(*tuples))
    #just get the y_coordinates since we are looking for vertical rows
    y_coords=zipped[1]

    #if the number of consecutive x_coordinates is greater than 5, return true otherwise False
    return (s(y_coords)>=amount_check)


def check_diagonal_right(player,amount_check):
    #name are misleading, since the coordinates towards teh right are always
    #the same, i dont need to keep track of the y coordinates, too lazy to change variable name
    x_cord=0
    in_a_row=0
    while x_cord<15:
        if ((x_cord,x_cord) in player):
            in_a_row+=1
            if in_a_row==amount_check:
                return True
        else:
            in_a_row=0
        x_cord+=1
    return False

#follows the same concept as check_diagonal_right
#except that this time both x and y change
#so i could check from bottom left to top right(which is what I did)
#or top right to bottom left
#I went from (0,14) to (14,0)
def check_diagonal_left(player,amount_check):
    x_cord=0
    y_cord=14
    in_a_row=0
    while x_cord<15:
        if ((x_cord,y_cord) in player):
            in_a_row+=1
            if in_a_row==amount_check:
                return True
        else:
            in_a_row=0
        x_cord+=1
        y_cord-=1
    return False

#return the number of consecutive integers
def s(l):
    n=1
    while n<len(l)and l[n]-l[0]==n:n+=1
    return max(n,s(l[n:])if l else 0)
