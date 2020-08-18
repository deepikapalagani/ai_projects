"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xnum=0
    onum=0
    for i in range(3):
        for j in range(3):
            if board[i][j]== X:
                xnum+= 1
            if board[i][j]== O:
                onum+= 1
    if xnum> onum:
        return O
    if xnum == onum:
        return X
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    act= []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                act.append((i, j))
    return act
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (i, j)= action
    if board[i][j] != EMPTY:
        raise Exception("already filled")
    else:
        b= copy.deepcopy(board)
        p= player(b)
        b[i][j]= p
        return b
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0]== X and board[1][1]== X and board[2][2]==X:
        return X
    if board[0][0]== O and board[1][1]== O and board[2][2]== O:
        return O
    for i in range(3):
        if board[i][0]== X and board[i][1]== X and board[i][2]== X:
            return X
    for i in range(3):
        if board[0][i]== X and board[1][i]== X and board[2][i]== X:
            return X
    for i in range(3):
        if board[i][0]== O and board[i][1]== O and board[i][2]== O:
            return O
    for i in range(3):
        if board[0][i]== O and board[1][i]== O and board[2][i]== O:
            return O
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    a= actions(board)
    if len(a)== 0:
        return True
    w= winner(board)
    if w== X or w== O:
        return True
    return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w= winner(board)
    if w== X:
        return 1
    if w== O:
        return -1
    return 0
    raise NotImplementedError

def maxval(board):
    if terminal(board):
        return utility(board)
    v= -math.inf
    for a in actions(board):
        v= max(v, minval(result(board, a)))
    return v


def minval(board):
    if terminal(board):
        return utility(board)
    v= math.inf
    for a in actions(board):
        v= min(v, maxval(result(board, a)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    turn= player(board)
    if turn== X:
        act= actions(board)
        best= act[0]
        v= -1000
        v1= -1000
        for a in act:
          v=  minval(result(board, a))
          if v> v1:
              best= a
              v1= v
        return best
    if turn== O:
        act= actions(board)
        v= 1000
        v1= 1000
        best= act[0]
        for a in act:
          v=  maxval(result(board, a))
          if v< v1:
              best= a
              v1= v
        return best


    raise NotImplementedError
