"""
Filename: nonogram_tile.py
Date Created: 5/4/2021
"""
from utils import Tile

class NonogramTile(Tile):
    STATUS_TYPES = ["unknown", "no", "yes"]

    def __init__(self, parent, row=0, col=0, colorUnknown="white", colorNo="gray75", colorYes="black", status="unknown"):
        Tile.__init__(self, parent, row=row, col=col, color=colorUnknown)
        self.colors = {"unknown": colorUnknown,
                       "yes": colorYes,
                       "no": colorNo}
        self.status = None
        self.setStatus(status)

    def onLeftClick(self, arg):
        if self.clickable:
            if self.status == "yes":
                self.setStatus("unknown")
            else:
                self.setStatus("yes")
            self.callbackFunction(self.row, self.col, self.status)

    def onRightClick(self, arg):
        if self.clickable:
            if self.status == "no":
                self.setStatus("unknown")
            else:
                self.setStatus("no")
            self.callbackFunction(self.row, self.col, self.status)

    def configureColor(self, status, color):
        self.colors[status] = color
        if status == self.status:  # See if our current color has to be updated
            self.color = color
            self.refresh()

    def setColor(self, color):
        """ This method should not be used for this class. Instead, use setStatus to change the current color,
        or use configureColor to change which colors represent the tile. """
        print("NonogramTile: Don't use setColor with this class. Use configureColor or setStatus.")

    def setStatus(self, status):
        if status in NonogramTile.STATUS_TYPES:
            self.status = status
        else:
            print("NonogramTile: unknown status type")
            self.status = "unknown"

        self.color = self.colors[self.status]
        self.refresh()

    def __str__(self):
        return "Nonogram tile: " + self.status