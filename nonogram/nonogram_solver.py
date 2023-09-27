"""
Filename: nonogram_solver.py
Date Created: 5/4/2021
"""

from utils import emptyCallback

class NonogramSolver:
    def __init__(self, nonogram_board):
        self.board = nonogram_board

        self.callbackFunction = emptyCallback

        self.showSteps = True
        self.numSteps = 0

    def configureCallbackFunction(self, function):
        """
        Configures the callback function. This callback function will be called whenever the solver makes an update.
        This will allow the owner of the solver to visually update the board as the solver solves.
        :param function: callbackfunction(row, col, status)
        """
        self.callbackFunction = function

    def solvePuzzle(self):
        self.numSteps = 0
        self.solveTile(0, 0)
        print("Puzzle Solved! It took " + str(self.numSteps) + " steps.")

    def solveTile(self, row, col):
        self.numSteps += 1
        nextRow, nextCol = self.getNextTile(row, col)
        noWorks = False
        yesWorks = False

        self.board.updateBoard(row, col, "no")
        self.callbackFunction(row, col, "no")
        if self.verifyCell(row,col):
            if nextRow is None:
                return True
            else:
                noWorks = self.solveTile(nextRow, nextCol)
        if noWorks:
            return True

        self.board.updateBoard(row, col, "yes")
        self.callbackFunction(row, col, "yes")
        if self.verifyCell(row,col):
            if nextRow is None:
                return True
            else:
                yesWorks = self.solveTile(nextRow, nextCol)

        if noWorks and yesWorks:
            print("INVALID PUZZLE, MULTIPLE SOLUTIONS") # TODO: Make this work somehow
        if not (noWorks or yesWorks):
            self.board.updateBoard(row, col, "unknown")
            self.callbackFunction(row, col, "unknown")

        return noWorks or yesWorks


    def verifyCell(self, row, col):
        """
        This function checks to see if a specific cell is viable. It does this by checking to see if the row and column
        containing the cell are viable.
        :param row: row of the cell
        :param col: column of the cell
        :return: True if viable, False otherwise
        """
        def verifyClue(clue, statuses):
            clueSum = sum(clue)
            clueIdx = 0
            yesCount = 0
            totalYes = 0
            for i, status in enumerate(statuses):
                if status == 0:  # If the current tile is Unknown, then check to see if we can get enough yeses
                    tilesLeft = len(statuses) - i
                    if clueSum > tilesLeft + totalYes:  # If we have too few yeses, the row/col is impossible
                        return False
                    # if we have enough yeses possible, just return True, this row/col is plausible
                    return True
                elif status == 1:  # If the current tile is No, then we check to see if the clue matches
                    if yesCount > 0:  # only check if clue matches if we have a clue
                        if yesCount == clue[clueIdx]:  # If we match, then we keep going
                            clueIdx += 1
                            yesCount = 0
                        else:  # The clue did not match, terminate
                            return False
                elif status == 2:  # If the current tile is Yes, then we increment our current clue
                    yesCount += 1
                    totalYes += 1
                    if totalYes > clueSum:  # If we have accumulated too many yeses, the row/col is invalid
                        return False
                    if yesCount > clue[clueIdx]:  # If we have exceeded the length of our current clue, the row/col is invalid
                        return False

            #  If we have exited the loop, then we are at the end of the row/col. We can only be valid if the row/col is
            #  solved. Because we have been checking each clue as we go, this can be checked by verifying the total
            #  yeses is the same as the row/col clue sum
            if totalYes == clueSum:
                return True
            else:
                return False

        rowClue = self.board.rowClues[row]
        colClue = self.board.colClues[col]
        rowStatuses = [self.board.board[row, c] for c in range(self.board.width)]
        colStatuses = [self.board.board[r, col] for r in range(self.board.height)]
        return verifyClue(rowClue, rowStatuses) and verifyClue(colClue, colStatuses)


    def getNextTile(self, row, col):
        """
        This function gets the  row/col of the next cell in the grid. It goes top to bottom, left to right
        :param row: row of the current cell
        :param col: column of the current cell
        :return: (row,col) of next cell
        """
        if col == self.board.width - 1:
            if row == self.board.height - 1:
                return None, None
            else:
                return (row + 1), 0
        else:
            return row, (col + 1)




