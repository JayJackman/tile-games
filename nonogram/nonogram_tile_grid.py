"""
Filename: nonogram_tile_grid.py
Date Created: 5/4/2021
"""

from utils import TileGrid, emptyCallback
from nonogram_tile import NonogramTile

class DefaultSettings:
    unknownColor = 'white'
    noColor="gray75"
    yesColor="black"


class NonogramTileGrid(TileGrid):
    def __init__(self, parent,
                 rows=5, cols=5,
                 tileMinWidth=50, tileMinHeight=50,
                 colorUnknown=DefaultSettings.unknownColor,
                 colorNo=DefaultSettings.noColor,
                 colorYes=DefaultSettings.yesColor,
                 tileChangeCallback=emptyCallback):

        TileGrid.__init__(self, parent, NonogramTile, rows=rows, cols=cols,
                          tileMinWidth=tileMinWidth, tileMinHeight=tileMinHeight)
        for tile in self.tiles:
            tile.configureColor("unknown", colorUnknown)
            tile.configureColor("no", colorNo)
            tile.configureColor("yes", colorYes)
            tile.configureCallback(self.onTileChange)

        self.tileChangeCallback = tileChangeCallback

    def onTileChange(self, row, col, status):
        """
        This method will be called whenever a Tile changes within the grid
        :param row: row of tile that changed
        :param col: col of tile that changed
        :param status: status of tile that changed
        """
        self.tileChangeCallback(row, col, status)


    # def createAnswerKey(self):
    #     """
    #     This method creates an answer key from the current configuration of the grid
    #     :return answerKey: A boolean numpy array of size (row, col) indicating which tiles have been selected
    #     """
    #     answerKey = np.zeros((self.height, self.width), dtype=bool)
    #     for row in range(self.height):
    #         for col in range(self.width):
    #             status = self.getTile(row, col).status
    #             if status == "yes":
    #                 answerKey[row, col] = True
    #             else:
    #                 answerKey[row, col] = False
    #     return answerKey

    def resetGrid(self):
        for row in range(self.height):
            for col in range(self.width):
                self.getTile(row, col).setStatus("unknown")