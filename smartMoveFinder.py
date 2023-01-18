
import random

scoreInitial = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0],
    [1, 1.5, 2, 2, 1.5, 1],
    [1.5, 3, 2, 2, 3, 1.5]]

CONNECTMATE = 1000
STALEMATE = 0
DEPTH = 5


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def scoreBoard(gs, player):

    if gs.connectmate == True:
        if player:
            return CONNECTMATE
        else:
            return -CONNECTMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0.0
    Color = 'R' if not player else 'G'
    for c in range(6):
        for r in range(6):
            score += scoreInitial[r][c] if Color == gs.board[r][c] else 0.0
    for c in range(6):
        for r in range(6):

            rowCounter = 0.0
            colCounter = 0.0
            for i in range(4):

                if (r+i+1 < 6 and gs.board[r+i+1][c] == gs.board[r][c] and gs.board[r][c] == Color):
                    rowCounter += 3

                if (c+i+1 < 6 and gs.board[r][c+i+1] == gs.board[r][c] and gs.board[r][c] == Color):
                    colCounter += 3

            score = float(score) + colCounter+rowCounter
    for c in range(6):
        for r in range(6):
            rowCounter = 0.0
            colCounter = 0.0
            for i in range(4):

                if (r+i+1 < 6 and c+i+1 < 6 and gs.board[r+i+1][c+i+1] == gs.board[r][c] and gs.board[r][c] == Color):
                    rowCounter += 2
                if (c+i+1 < 6 and r-(i+1) >= 0 and gs.board[r-i-1][c+i+1] == gs.board[r][c] and gs.board[r][c] == Color):
                    colCounter += 2

        score += rowCounter+colCounter
    return score if player else -1*score


def findBestMove(gs, validMoves, player):

    global nextMove
    nextMove = None
    scoreT = findMove(gs, validMoves, DEPTH, player)
    return nextMove


def findMove(gs, validMoves, depth, player):
    global nextMove
    if depth == 0:
        return scoreBoard(gs, player)
    if player:
        maxScore = -CONNECTMATE
        for move in validMoves:
            gs.makeMove(move, player)
            nextMoves = gs.getValidMoves()
            score = findMove(gs, nextMoves, depth-1, 0)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CONNECTMATE
        for move in validMoves:
            gs.makeMove(move, player)
            nextMoves = gs.getValidMoves()
            score = findMove(gs, nextMoves, depth-1, 1)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
