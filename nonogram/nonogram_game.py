"""
Filename: nonogram_game.py
Date Created: 4/24/2021
"""
import tkinter as tk
from tkinter import simpledialog, filedialog
import time
import os

from nonogram_tile_grid import NonogramTileGrid
from nonogram_board import NonogramBoard
from nonogram_solver import NonogramSolver


class Settings:
    creationBGColor = "plum2"
    solvingBGColor = 'firebrick4'
    clueColor = 'grey'
    controlButtonColor = 'LightBlue1'
    modeLabelColor = 'yellow'
    unknownColor = 'white'
    noColor = "gray75"
    yesColor = "black"
    width = 15
    height = 15
    solverSleepTime = 0
    tileMinHeight = 25
    tileMinWidth = 25

class NonogramGame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.nonogramGrid = NonogramTileGrid(self,
                                             cols=Settings.width, rows=Settings.height,
                                             tileChangeCallback=self.onGameBoardChange,
                                             colorUnknown=Settings.unknownColor,
                                             colorNo=Settings.noColor,
                                             colorYes=Settings.yesColor,
                                             tileMinWidth=Settings.tileMinWidth,
                                             tileMinHeight=Settings.tileMinHeight)
        self.nonogramGrid.grid(row=1, column=1, sticky="nsew")

        # Restrict the rows/columns of the game board from becoming too small, and make them expand to fill on resize
        self.rowconfigure(1, minsize=self.nonogramGrid.getMinHeight(), weight=1)
        self.columnconfigure(1, minsize=self.nonogramGrid.getMinWidth(), weight=1)

        # Create the clue labels
        self.rowClueFrame = None
        self.columnClueFrame = None
        self.rowClueLabels = None
        self.columnClueLabels = None
        self.initClueLabels()

        """ Set up the control Frame in top left """
        self.controlFrame = tk.Frame(master=self, bg=Settings.creationBGColor)
        self.controlFrame.grid(row=0, column=0, sticky="nsew")
        self.controlFrame.columnconfigure([0,1], weight=1)
        self.controlFrame.rowconfigure([0,1,2], weight=1)

        """ Create the buttons """
        self.loadButton = tk.Button(master=self.controlFrame, text="Load",bg=Settings.controlButtonColor,relief='raised', command=self.onLoadButtonClicked)
        self.saveButton = tk.Button(master=self.controlFrame, text="Save", bg=Settings.controlButtonColor, relief="raised", command=self.onSaveButtonClicked)
        self.solveButton = tk.Button(master=self.controlFrame, text="Solve", bg=Settings.controlButtonColor, relief="raised", command=self.onSolveButtonClicked)
        self.checkButton = tk.Button(master=self.controlFrame, text="Check", bg=Settings.controlButtonColor, relief="raised", command=self.onCheckButtonClicked)
        self.switchModeButton = tk.Button(master=self.controlFrame, text="Switch mode", bg=Settings.controlButtonColor, relief='raised', command=self.onSwitchModeButtonClicked)

        """ Set up for creation mode """
        self.gameMode = "creation"
        self.showLoadButton()
        self.showSaveButton()
        self.switchModeButton.grid(row=1,columnspan=2, sticky="nsew", padx=5, pady=5)

        self.modeLabel = tk.Label(master=self.controlFrame, text="Mode: Creating", bg=Settings.modeLabelColor, relief='ridge')
        self.modeLabel.grid(row=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        """ Initialize our internal nonogram board """
        self.nonogramBoard = None
        self.setPuzzle()  # Initialize the empty puzzle

        """ Configure the Solver"""
        self.solver = NonogramSolver(self.nonogramBoard)
        self.solver.configureCallbackFunction(self.onSolverStep)

    def initClueLabels(self):
        """ Set up the row clue labels"""
        self.rowClueFrame = tk.Frame(master=self)
        self.rowClueFrame.columnconfigure(0, minsize=100, weight=1)
        self.rowClueLabels = []
        for row in range(self.nonogramGrid.height):
            self.rowClueFrame.rowconfigure(row, minsize=self.nonogramGrid.tileMinHeight, weight=1)
            label = tk.Label(master=self.rowClueFrame, text="", font=("arial", 12), bg=Settings.clueColor,
                             relief="sunken")
            label.grid(row=row, column=0, sticky="nsew")
            self.rowClueLabels.append(label)
        self.rowClueFrame.grid(row=1, column=0, sticky="nsew")

        """ Set up the column clue labels"""
        self.columnClueFrame = tk.Frame(master=self)
        self.columnClueFrame.rowconfigure(0, minsize=100, weight=1)
        self.columnClueLabels = []
        for col in range(self.nonogramGrid.width):
            self.columnClueFrame.columnconfigure(col, minsize=self.nonogramGrid.tileMinWidth, weight=1)
            label = tk.Label(master=self.columnClueFrame, text="", font=("arial", 12), bg=Settings.clueColor,
                             relief='sunken')
            label.grid(row=0, column=col, sticky="nsew")
            self.columnClueLabels.append(label)
        self.columnClueFrame.grid(row=0, column=1, sticky="nsew")

    def showSaveButton(self):
        self.saveButton.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    def showLoadButton(self):
        self.loadButton.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    def showSolveButton(self):
        self.solveButton.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    def showCheckButton(self):
        self.checkButton.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def onSaveButtonClicked(self):
        """
        Saves the current configuration of the board into a .puz file
        :return:
        """
        saveName = tk.simpledialog.askstring("Save Puzzle", "What would you like to call your puzzle?")
        if saveName is not None:
            file = open("puzzles/" + saveName + ".puz", "w")
            file.write("Rows:\n")
            file.write(str(self.nonogramGrid.height) + "\n")
            file.write("Cols:\n")
            file.write(str(self.nonogramGrid.width) + "\n")
            file.write("Row clues:\n")
            for rowClue in self.nonogramBoard.rowClues:
                for clue in rowClue:
                    file.write(str(clue) + " ")
                file.write("\n")
            file.write("Col clues:\n")
            for colClue in self.nonogramBoard.colClues:
                for clue in colClue:
                    file.write(str(clue) + " ")
                file.write("\n")
            file.close()

    def onLoadButtonClicked(self):
        loadFile = filedialog.askopenfilename(initialdir=os.getcwd()+"\\nonogram\\puzzles", title="Load Puzzle", filetypes=[("Nonogram Puzzles", "*.puz")])
        f = open(loadFile, "r")
        f.readline()         # rows
        line = f.readline()  # numRows
        numRows = int(line)
        f.readline()         # cols
        line = f.readline()  # numCols
        numCols = int(line)
        f.readline()         # rowClues

        rowClues = []
        for i in range(numRows):
            line = f.readline()
            rowClues.append([int(a) for a in line.split()])

        f.readline()         # colClues
        colClues = []
        for i in range(numCols):
            line = f.readline()
            colClues.append([int(a) for a in line.split()])
        f.close()

        self.nonogramBoard = NonogramBoard.initFromClues(rowClues, colClues)
        if numRows != self.nonogramGrid.height or numCols != self.nonogramGrid.width:
            self.nonogramGrid.forget()
            self.nonogramGrid = NonogramTileGrid(self,
                                                 cols=numCols, rows=numRows,
                                                 tileChangeCallback=self.onGameBoardChange,
                                                 colorUnknown=Settings.unknownColor,
                                                 colorNo=Settings.noColor,
                                                 colorYes=Settings.yesColor,
                                                 tileMinWidth=Settings.tileMinWidth,
                                                 tileMinHeight=Settings.tileMinHeight)
            self.nonogramGrid.grid(row=1, column=1, sticky="nsew")
            self.rowClueFrame.forget()
            self.columnClueFrame.forget()
            self.initClueLabels()
        else:
            self.nonogramGrid.resetGrid()

        self.setClueLabels()


    def onSolveButtonClicked(self):
        self.nonogramGrid.setClickable(False)

        self.solver.board = self.nonogramBoard
        self.solver.solvePuzzle()

        self.nonogramGrid.setClickable(True)

    def onSolverStep(self, row, col, status):
        self.nonogramGrid.getTile(row,col).setStatus(status)
        time.sleep(Settings.solverSleepTime)
        self.update()  # Force the grid to show the progress
        self.onGameBoardChange(row, col, status)

    def onCheckButtonClicked(self):
        # TODO: create function in NonogramBoard that checks the current state of the game board against its answerKey
        print("Check not yet implemented")
        # valid = True
        # for row in range(self.nonogramBoard.height):
        #     if not self.nonogramBoard.verifyRow(row):
        #         valid = False
        # for col in range(self.nonogramBoard.width):
        #     if not self.nonogramBoard.verifyCol(col):
        #         valid = False
        # print("Check: ", valid)

    def onSwitchModeButtonClicked(self):
        self.switchMode()

    def onGameBoardChange(self, row, col, status):
        if self.gameMode is "creation":  # Set the clues to update as we edit the board
            self.setPuzzle(validate=False)
        elif self.gameMode is "solving":  # Track the state of the board to match our progress
            self.nonogramBoard.updateBoard(row, col, status)

    def setPuzzle(self, validate=False):
        """
        This function analyzes the current game board and creates the puzzle clues
        :return: #TODO: return false if invalid puzzle, true otherwise
        """
        self.nonogramBoard = NonogramBoard.initFromGrid(self.nonogramGrid)
        self.setClueLabels()

    def setClueLabels(self):
        """ Set the row clue labels based on the input grid """
        for i, rowClue in enumerate(self.nonogramBoard.rowClues):
            label = self.rowClueLabels[i]
            labelText = ""
            for j, clue in enumerate(rowClue):
                if j == 0:
                    labelText += str(clue)
                else:
                    labelText += " " + str(clue)
            label.configure(text=labelText)

        """ Set the column clue labels based on the input grid """
        for i, columnClue in enumerate(self.nonogramBoard.colClues):
            label = self.columnClueLabels[i]
            labelText = ""
            for j, clue in enumerate(columnClue):
                if j == 0:
                    labelText += str(clue)
                else:
                    labelText += "\n" + str(clue)
            label.configure(text=labelText)

    def switchMode(self):
        if self.gameMode is "creation":
            self.nonogramGrid.resetGrid()
            self.gameMode = "solving"
            self.modeLabel.configure(text="Mode: Solving")

            self.controlFrame.configure(bg=Settings.solvingBGColor)
            self.saveButton.grid_forget()
            self.loadButton.grid_forget()
            self.showSolveButton()
            self.showCheckButton()

        elif self.gameMode is "solving":
            self.setPuzzle(validate=True)
            self.gameMode = "creation"
            self.modeLabel.configure(text="Mode: Creating")

            self.controlFrame.configure(bg=Settings.creationBGColor)
            self.solveButton.grid_forget()
            self.checkButton.grid_forget()
            self.showSaveButton()
            self.showLoadButton()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Nonogram Game")

    game = NonogramGame(root)
    game.pack(fill='both', expand=1)


    def onButton():
        game.switchMode()


    # button = tk.Button(root, command=onButton)
    # button.pack()

    # numRows = 15
    # numCols = 15
    # minWidth = 50
    # minHeight = 50
    # colorUnknown = "DarkOrange1"
    # colorNo = "gray75"
    # colorYes = "black"
    #
    # grid = NonogramTileGrid(root, rows=numRows, cols=numCols, tileMinWidth=minWidth, tileMinHeight=minHeight,
    #                         colorUnknown=colorUnknown,
    #                         colorNo=colorNo, colorYes=colorYes)
    # root.minsize(grid.getMinWidth(), grid.getMinHeight())
    # grid.pack(fill='both', expand=1)
    #
    #
    # def onButton():
    #     board = NonogramBoard(grid)
    #     print(board.rowClues)
    #     print(board.colClues)
    #
    #
    # button = tk.Button(root, command=onButton)
    # button.pack()

    # root.resizable(False, False)
    root.mainloop()
