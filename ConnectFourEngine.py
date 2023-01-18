import numpy


class GameState():
    boards = list()

    def __init__(self):
        self.board = [
            ['--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--'],

            ['--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--']]
        self.redMove = False
        self.connectmate = False
        self.stalemate = False
        self.moveLog = []

    def makeMove(self, move, player):
        self.board[move[0]][move[1]] = 'G' if player else 'R'
        self.isConnected()
        self.moveLog.append((move[0], move[1]))

    def getValidMoves(self):

        validMoves = []
        for c in range(6):
            for r in range(6):
                if (self.board[r][c] == '--'):
                    if (r == 5):
                        validMoves.append((r, c))
                    elif (self.board[r+1][c] != '--'):
                        validMoves.append((r, c))

        return validMoves

    def isConnected(self):

        full = 0
        for c in range(6):
            for r in range(6):
                if self.board[r][c] != '--':
                    full += 1
                rowCounter = 0
                colCounter = 0
                for i in range(4):

                    if colCounter == 3 or rowCounter == 3:
                        self.connectmate = True
                        break
                    if (r+i+1 < 6 and self.board[r+i+1][c] == self.board[r][c] and self.board[r][c] != '--'):
                        rowCounter += 1
                        continue
                    if (c+i+1 < 6 and self.board[r][c+i+1] == self.board[r][c] and self.board[r][c] != '--'):
                        colCounter += 1
                        continue
                    break

                if full == 36:
                    self.stalemate = True
        for c in range(6):
            for r in range(6):
                rowCounter = 0
                colCounter = 0
                for i in range(4):

                    if colCounter == 3 or rowCounter == 3:
                        self.connectmate = True
                        break
                    if (r+i+1 < 6 and c+i+1 < 6 and self.board[r+i+1][c+i+1] == self.board[r][c] and self.board[r][c] != '--'):
                        rowCounter += 1
                        continue
                    if (c+i+1 < 6 and r-(i+1) >= 0 and self.board[r-i-1][c+i+1] == self.board[r][c] and self.board[r][c] != '--'):
                        colCounter += 1
                        continue
                    break

    def undoMove(self):
        if len(self.moveLog) == 0:
            return
        move = self.moveLog.pop()
        self.board[move[0]][move[1]] = '--'
        self.connectmate = self.stalemate = False
