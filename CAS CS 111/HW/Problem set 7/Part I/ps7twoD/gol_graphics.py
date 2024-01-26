# 2011-10-23 Rick Zaccone. Based on code supplied by HMC.
# Minor modifications by Dave Sullivan.
# This code assumes that there is a function named next_gen in the
# file ps7pr3.py.

import time
from turtle import *
from ps7pr2 import *
from ps7pr3 import *

def getMousePosition(mouse_x, mouse_y):
    """ Returns the row and column clicked by the mouse in a tuple.  mouse_x and
        mouse_y are the mouse coordinates in pixels.  The return value is the
        cell position in the 2D list.
    """
    col = 0
    row = 0

    for i in range(len(currentXs) - 1):
        if currentXs[i] <= mouse_x < currentXs[i + 1]:
            col = i
            break
    for i in range(len(currentYs) - 1):
        if currentYs[i] <= mouse_y < currentYs[i - 1]:
            row = i - 1
            break

    if mouse_x > 0 and col == 0:
        col = len(currentXs) - 2
    if mouse_y < 0 and row == 0:
        row = len(currentYs) - 2

    return (row, col)

def set_color(key, color):
    """ Sets a color in the color dictionary.  For example, use
        setColor(1, "purple") to have the live cells appear in purple.
    """
    global colorDict
    colorDict[key] = color
    return

def colorLookup(color):
    """ Looks up a color in the color dictionary.  color is the numerical value
        of the color.  The return value is a string for the color.  For example,
        "red".
    """
    if color in colorDict:
        return colorDict[color]
    else:
        return color

def drawSquare(upperLeftX, upperLeftY, sideLength, color):
    """ Draws a single square, and fills it based on the
        number held in that square's position on the array"""
    delay(0)
    tracer(False)
    up()
    # try setting the color
    pencolor("black")
    # look up the color
    color = colorLookup(color)
    # go!
    try:
        fillcolor(color)
    except:
        print("Color", color, "was not recognized.")
        print("Using blue instead.")
        fillcolor("blue")

    goto(upperLeftX, upperLeftY)
    down()
    setheading(0) # east

    begin_fill()
    for side in range(4):
        forward(sideLength)
        right(90)
    end_fill()

    up()

def displayBoard(board):
    """ Displays the board using Turtle Graphics.
    """
    global currentBoard
    currentBoard = board

    windowWidth = window_width()
    windowHeight = window_height()
    if len(board) == 0:
        print("You can't display a board with no cells.")
        return

    # Add 2 to the width and height to account for the border.

    boardWidth = len(board[0]) + 2
    boardHeight = len(board) + 2
    global squareSide
    squareSide = min(windowWidth // boardWidth, windowHeight // boardHeight, 100)

    global topLeftX
    global topLeftY
    topLeftY = squareSide * boardHeight // 2
    topLeftX = -squareSide * boardWidth // 2

    global currentYs
    currentYs = [topLeftY]
    global currentXs
    currentXs = [topLeftX]

    clear()
    upperLeftX = topLeftX
    upperLeftY = topLeftY
    for row in board:
        for color in row:
            drawSquare(upperLeftX, upperLeftY, squareSide, color)
            upperLeftX += squareSide
            if upperLeftX not in currentXs:
                currentXs.append(upperLeftX)
        upperLeftY -= squareSide
        currentYs.append(upperLeftY)
        upperLeftX = topLeftX
    return

def translateRowColToXY(row, col):
    """ Translates a row and column to the coordinates of the upper left
        corner of the square.
    """
    x = topLeftX + col * squareSide
    y = topLeftY - row * squareSide
    return (x, y)

def lifeMouseHandler(x, y):
    """ This function is called with each mouse click.

        Its inputs are the pixel location of the
        next mouse click: (x,y)

        It computes the column and row (within the board)
        where the click occurred with getMousePosition, and changes the
        color of the clicked square.

        The overall list is shared between turtle graphics
        and the other parts of your program as a global
        variable named currentBoard. In general, global variables
        make software more complex, but sometimes they are
        necessary.
    """
    row, col = getMousePosition(x, y)
    if isBorderCell(row, col):
        print("Don't click on the border!!! >:O")
        return
    else:
        currentBoard[row][col] = 1 - currentBoard[row][col]
    x, y = translateRowColToXY(row, col)
    drawSquare(x, y, squareSide, currentBoard[row][col])

def isBorderCell(row, col):
    """ Determines if the cell at (row, col) is a border cell.
    """
    return row == 0 or row == len(currentBoard) - 1 or \
           col == 0 or col == len(currentBoard[0]) - 1

def displayNextLifeGeneration():
    """ Makes the next life generation appear"""
    global currentBoard
    oldBoard = currentBoard
    currentBoard = addBorder(next_gen(removeBorder(currentBoard)))
    displayDifferences(oldBoard)

def displayDifferences(oldBoard):
    """ Displays the cells that have changed since oldBoard.
    """
    for row in range(len(currentBoard)):
        for col in range(len(currentBoard[0])):
            if oldBoard[row][col] != currentBoard[row][col]:
                x, y = translateRowColToXY(row, col)
                drawSquare(x, y, squareSide, currentBoard[row][col])

def runGameOfLife():
    """ Sets the board to keep moving through generations of life.
        Allows for pausing with "p", resuming with "Enter"/"Return",
        and automatically pauses the game if the board stops changing
        or becomes blank."""
    screen.onkey(stopGame, "p")
    screen.onkey(bye, "q")
    screen.onkey(resumeGame, "Return")
    screen.listen()
    if isGameRunning():
         nextGeneration = next_gen(removeBorder(currentBoard))
         followingGeneration = next_gen(nextGeneration)
         if nextGeneration == followingGeneration:
            stopGame()
         else:
            displayNextLifeGeneration()
            screen.ontimer(runGameOfLife,  t = 0)
            #The t value above sets how many milliseconds there are
            # between each generation of life. Set it low (e.g. 0 seconds, or 500
            # for half a second, etc.) for fast movement, or
            # set it high (e.g. 1000 for 1 second, 3000 for 3 seconds, etc.)
            # for fast slower movement.

def eraseBoard():
    """ Makes the board blank (resets the board)"""
    global currentBoard
    rows = len(currentBoard)
    cols = len(currentBoard[0])
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if currentBoard[row][col] != 0:
                currentBoard[row][col] = 0
                x, y = translateRowColToXY(row, col)
                drawSquare(x, y, squareSide, 0)

def startGame():
    """ Starts the current game without showing the board.
    """
    global isRunning
    isRunning = True

def resumeGame():
    """Resumes a paused game."""
    global isRunning
    isRunning = True
    runGameOfLife()

def stopGame():
    """ Stops or pauses the current game.
    """
    global isRunning
    isRunning = False

def isGameRunning():
    """ Determines if the game is running.
    """
    return isRunning

def instructions():
    print("Welcome to the game of 'Life'!!\n")
    print("Click on a blank square to bring it to life,")
    print("or on a live square to kill it.\n")
    print("By pressing 'Return'/'Enter', the simulation begins.\n")
    print("The rules of the game are as follows:")
    print()
    print("1. A cell that has fewer than two live neighbors dies (because")
    print("   of loneliness).\n")
    print("2. A cell that has more than three live neighbors dies (because")
    print("   of over-crowding).\n")
    print("3. A cell that is dead and has exactly three live neighbors")
    print("   comes to life.\n")
    print("4. All other cells maintain their state.")
    print()
    print("The game automatically pauses if the board stops changing")
    print("or becomes blank.")
    print()
    print("You can pause the game by pressing 'p',")
    print("and resume it by pressing 'Return'/'Enter'.")
    print()
    print("You can reset the board (make all squares blank)")
    print("by pressing the 'Space' key.")
    print()
    print("The game can be closed at any time by pressing the 'Escape'")
    print("or 'q' key.")
    print()
    print("Have fun!! :D")

def show_graphics(aBoard):
    """ Creates a window, adds an extra border around the board, then displays
        it.
    """
    global currentBoard
    newWindow()
    currentBoard = addBorder(aBoard)
    displayBoard(currentBoard)
    done()

def newWindow():
    """ Creates a window and perform some initialization so we can start
        displaying life generations.
    """
    global screen
    screen = Screen() # Singleton instance of TurtleScreen
    startGame()
    screen.listen()
    onscreenclick(lifeMouseHandler)
    screen.onkey(runGameOfLife, "Return")
    screen.onkey(bye, "Escape")
    screen.onkey(bye, "q")
    screen.onkey(eraseBoard, "space")
    screen.title("The Game of Life")
    reset()
    tracer(False)
    delay(0)

def readBoard():
    """ Reads in Life patterns found on
        http://www.argentum.freeserve.co.uk/lex.htm
        Just copy and paste as the input to this function.
    """
    print('enter the pattern:')
    s = input()
    s = s.strip()
    s = s.replace("\t", "")
    s = s.replace(" ", "")
    s = s.replace('.', '0')
    s = s.replace('O', '1')
    s = s.split("\n")
    board = []
    for i in range(len(s)):
        row = list(s[i])
        row = [int(row[i]) for i in range(len(row))]
        board.append(row)
    return board

def read_pattern(rowPad, colPad):
    """ Reads a board and pads all around with rowPad and colPad.
    """
    if rowPad < 0 or colPad < 0:
        print("The padding must be nonnegative.")
        return None
    board = readBoard()
    oldRows = len(board)
    newCols = len(board[0]) + 2 * colPad
    newBoard = []
    for i in range(rowPad):
        newBoard.append(newCols * [0])
    for i in range(oldRows):
        newBoard.append(colPad * [0] + board[i] + colPad * [0])
    for i in range(rowPad):
        newBoard.append(newCols * [0])
    return newBoard


def addBorder(board):
    """ Adds a blue border to the board.
    """
    boardHeight = len(board)
    boardWidth = len(board[0])
    newWidth = boardWidth + 2
    newBoard = []
    newBoard.append([2] * newWidth)
    for row in range(boardHeight):
         newRow = [2]
         for col in range(boardWidth):
              newRow.append(board[row][col])
         newRow.append(2)
         newBoard.append(newRow)
    newBoard.append([2] * newWidth)
    return newBoard

def removeBorder(board):
    """ Removes the board's border.
    """
    rows = len(board)
    cols = len(board[0])
    newBoard = []
    for row in range(1, rows - 1):
        newRow = []
        for col in range(1, cols - 1):
            newRow.append(board[row][col])
        newBoard.append(newRow)
    return newBoard

global colorDict
colorDict = { 0:"white", 1:"red", 2:"blue", 3:"green", 4:"gold" }
