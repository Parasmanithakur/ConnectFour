import pygame as p
import math
import ConnectFourEngine
import smartMoveFinder
from multiprocessing import Process, Queue
import time
DIMENSION = 6
BOARD_WIDTH = BOARD_HEIGHT = 512
SQ_SIZE = BOARD_HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = dict()
gs = ConnectFourEngine.GameState()


def main():
    p.init()
    player = 1  # green
    validMoves = gs.getValidMoves()
    screen = p.display.set_mode((BOARD_WIDTH+10, BOARD_HEIGHT+15))
    clock = p.time.Clock()
    screen.fill(p.Color(59, 74, 204))
    running = True
    moveMade = False
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True
    playerTwo = True
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col) and col >= 6 or row >= 6:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        print(sqSelected)
                        for move in validMoves:
                            if move[0] == sqSelected[0] and move[1] == sqSelected[1]:
                                animateMove(move, screen, clock,
                                            player)
                                drawGameState(screen, gs, sqSelected)

                                gs.makeMove(sqSelected, player)
                                print(smartMoveFinder.scoreBoard(gs, player))
                                moveMade = True

                                player ^= 1
                                gs.redMove = not gs.redMove
                                validMoves = gs.getValidMoves()

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    movemade = False

                    player ^= 1
                    gs.redMove = not gs.redMove
            drawGameState(screen, gs, sqSelected)
            if gs.connectmate or gs.stalemate:

                gameOver = True
                Name = "Red" if player else "Green"
                text = Name + " WINS" if gs.connectmate else "Draw"
                drawEndGameText(screen, text)
            if not gameOver and moveMade:

               # AI = smartMoveFinder.findRandomMove(validMoves)
                AI = smartMoveFinder.findBestMove(gs, validMoves, player)
                # animateMove(AI, screen, clock,
                #             player)
                gs.makeMove(AI, player)
                print(smartMoveFinder.scoreBoard(gs, player))
                player ^= 1
                gs.redMove = not gs.redMove
                validMoves = gs.getValidMoves()
                moveMade = False

            clock.tick(MAX_FPS)
            p.display.flip()


def drawGameState(screen, gs, sqSelected, choice=1):
    drawBoard(screen, gs, choice)


def drawBoard(screen, gs, choice):

    green = p.Color(255, 255, 0)
    red = p.Color(255, 0, 0)
    colors = [red, green, p.Color(255, 0, 255), p.Color(255, 255, 255)]
    font = p.font.SysFont("Arial", 14, True, False)
    for c in range(DIMENSION):
        for r in range(DIMENSION):
            # p.draw.rect(screen, colors[2], p.Rect(
            #     c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE),  2)
            p.draw.circle(screen, colors[3],
                          (c*(SQ_SIZE)+36, r*(SQ_SIZE)+36), 34, 100)
            if gs.board[r][c] == 'R':
                p.draw.circle(screen, colors[0],
                              (c*(SQ_SIZE)+36, r*(SQ_SIZE)+36), 34, 0)
            elif gs.board[r][c] == "G":
                p.draw.circle(screen, colors[1],
                              (c*(SQ_SIZE)+36, r*(SQ_SIZE)+36), 34, 0)


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('YELLOW'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH/2-textObject.get_width()/2, BOARD_HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


def animateMove(move, screen, clock, player):

    dc = move[0]
    color = 'G' if player else 'R'
    framesPerSquare = 10  # frames to move one square
    frameCount = (abs(dc))  # * framesPerSquare
    for frame in range(frameCount):
        c, r = (0+dc*frame/frameCount,
                move[1])
        c, r = (0+frame,
                move[1])
        # print(c, r)

        gs.board[math.floor(c)][math.floor(r)] = color
        drawBoard(screen, gs, 1)

        p.display.flip()
        # p.draw.rect(screen, colors, endSquare)
        # p.draw.circle(screen, colors,
        #               (r*(SQ_SIZE)+36, c*(SQ_SIZE)+36), 34, 0)

        # p.draw.circle(screen, p.Color(59, 74, 204),
        #               (r*(SQ_SIZE)+36, c*(SQ_SIZE)+36), 34, 0)

        time.sleep(0.1)
        gs.board[math.floor(c)][math.floor(r)] = '--'
        drawBoard(screen, gs, 1)
        p.display.flip()
        clock.tick(60)
    drawBoard(screen, gs, 1)


if __name__ == "__main__":
    main()
