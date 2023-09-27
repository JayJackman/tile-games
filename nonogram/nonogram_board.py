"""
Filename: nonogram_board.py
Date Created: 5/4/2021
"""

import numpy as np
from nonogram_tile_grid import NonogramTileGrid


class NonogramBoard:
    def __init__(self):
        self.height = None
        self.width = None
        self.board = None
        self.answerKey = None
        self.rowClues = None
        self.colClues = None

    @classmethod
    def initFromClues(cls, rowClues, colClues):
        """
        Create a board from row/col clues.
        :param rowClues: row clues of the puzzle to create
        :param colClues: col clues of the puzzle to create
        :return: a NonogramBoard with the proper clues
        """
        board = cls()
        board.height = len(rowClues)
        board.width = len(colClues)
        board.answerKey = np.zeros((board.height, board.width),
                                   dtype=bool)  # TODO: make this answer key by solving the puzzle
        board.board = np.zeros((board.height, board.width), dtype=int)
        board.rowClues = rowClues
        board.colClues = colClues
        return board

    @classmethod
    def initFromGrid(cls, inputGrid: NonogramTileGrid):
        """
        Create a board from a filled-in NonogramTileGrid
        :param inputGrid: a NonogramTileGrid that indicates the answerKey for the board
        :return:
        """
        board = cls()
        board.height = inputGrid.height
        board.width = inputGrid.width
        board.answerKey = np.zeros((board.height, board.width), dtype=bool)
        board.board = np.zeros((board.height, board.width), dtype=int)
        board.initializeAnswerKeyFromTileGrid(inputGrid)
        # TODO: Add verify here ( check for multiple solutions )
        return board

    def initializeAnswerKeyFromClues(self, rowClues, colClues):
        # TODO: solve the board, then create the answer key
        pass

    def initializeAnswerKeyFromTileGrid(self, gameGrid: NonogramTileGrid):
        """ This creates a puzzle from an arbitrary layout of a game grid. It does not do any checking for puzzle validity """
        self.rowClues = []
        for row in range(self.height):
            prevStatus = "no"
            yesCount = 0
            rowClue = []
            for col in range(self.width):
                status = gameGrid.getTile(row, col).status
                if status == "yes":
                    self.answerKey[row, col] = True
                else:
                    self.answerKey[row, col] = False

                if prevStatus == "yes":
                    if status is "yes":
                        yesCount += 1
                    else:  # yes -> no, need to add our clue and reset the counter
                        rowClue.append(yesCount)
                        yesCount = 0
                else:
                    if status is "yes":
                        yesCount += 1

                # Handle case when we have yes at the end and so we never got the yes -> no transition
                if col == (self.width - 1):
                    if yesCount > 0:
                        rowClue.append(yesCount)
                prevStatus = status
            if rowClue == []:
                rowClue = [0]
            self.rowClues.append(rowClue)

        self.colClues = []
        for col in range(self.width):
            prevStatus = "no"
            yesCount = 0
            colClue = []
            for row in range(self.height):
                status = gameGrid.getTile(row, col).status

                if prevStatus == "yes":
                    if status is "yes":
                        yesCount += 1
                    else:  # yes -> no, need to add our clue and reset the counter
                        colClue.append(yesCount)
                        yesCount = 0
                else:
                    if status is "yes":
                        yesCount += 1

                # Handle case when we have yes at the end and so we never got the yes -> no transition
                if row == (self.height - 1):
                    if yesCount > 0:
                        colClue.append(yesCount)
                prevStatus = status
            if colClue == []:
                colClue = [0]
            self.colClues.append(colClue)

    def status2boardNumber(self, status):
        if status is "unknown":
            return 0
        elif status is "no":
            return 1
        elif status is "yes":
            return 2

    def updateBoard(self, row, col, status):
        """
        Updates a given cell of the board with the passed in parameters
        :param row: row to update
        :param col: column to update
        :param status: status to update
        """
        self.board[row, col] = self.status2boardNumber(status)

    def copyTileGrid(self, gameGrid: NonogramTileGrid):
        """
        Sets the state of the board to copy a given NonogramTileGrid
        :param gameGrid: the NonogramTileGrid to copy
        """
        for row in range(self.height):
            for col in range(self.width):
                self.updateBoard(row, col, gameGrid.getTile(row, col).status)

    # TODO: Add an initialize from clues function. This will require the solver to work.

    def __str__(self):
        toReturn = "Nonogram Board:"
        for row in range(self.height):
            toReturn += "\n  "
            for col in range(self.width):
                toReturn += str(self.board[row, col]) + " "
        return toReturn
