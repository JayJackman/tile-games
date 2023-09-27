"""
Filename: utils.py
Date Created: 4/24/2021
"""

import tkinter as tk

class Tile(tk.Frame):
    """
    A tile is the base building block of a grid game. It has a background color and a text value.
    For subclassing Tile, override the onClick method to get your desired functionality.
    """
    def __init__(self, parent, row=0, col=0, color='grey', text=''):
        tk.Frame.__init__(self, parent, bg=color)
        self.label = tk.Label(self, bg=color, text="", font=12, relief="raised")
        self.label.pack(fill='both', expand=1)  # Fill the whole frame with the label
        self.color = color
        self.text = text
        self.row = row
        self.col = col

        self.label.bind("<Button-1>", self.onLeftClick)
        self.label.bind("<Button-2>", self.onRightClick)
        self.label.bind("<Button-3>", self.onRightClick)

        self.clickable = True
        self.callbackFunction = emptyCallback  # Declare the callback function, but leave it empty

    def setColor(self, color):
        self.color = color
        self.refresh()

    def setText(self, text):
        self.text = text
        self.refresh()

    def onLeftClick(self, arg):
        if self.clickable:
            self.callbackFunction(self.row, self.col)

    def onRightClick(self, arg):
        if self.clickable:
            self.callbackFunction(self.row, self.col)

    def __str__(self):
        return "Color: " + self.color + ", text:  " + self.text

    def refresh(self):
        self.label.configure(bg=self.color, text=self.text)

    def configureCallback(self, callbackFunc):
        self.callbackFunction = callbackFunc

class TileGrid(tk.Frame):
    """
    A TileGrid is a grid of tiles, with the desired number of rows and columns.
    You can pass in any type of Tile object you want, to dictate how the grid behaves
    """

    def __init__(self, parent, tile_class=Tile, rows=3, cols=3, tileMinWidth=100, tileMinHeight=100):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.tileClass = tile_class
        self.height = rows
        self.width = cols
        self.tileMinWidth = tileMinWidth
        self.tileMinHeight = tileMinHeight
        self.clickable = True

        # Configure the rows/columns to obey the minimum width, as well as expand on window resize
        for i in range(rows):
            self.rowconfigure(i, minsize=tileMinWidth, weight=1)
        for i in range(cols):
            self.columnconfigure(i, minsize=tileMinHeight, weight=1)

        self.tiles = []
        self.createTiles()

    def createTiles(self):
        for row in range(self.height):
            for col in range(self.width):
                tile = self.tileClass(self, row=row, col=col)
                tile.grid(row=row, column=col, sticky="nsew")
                self.tiles.append(tile)

    def getTile(self, row, col) -> Tile:
        index = row * self.width + col
        return self.tiles[index]

    def getMinWidth(self):
        """
        Returns the minimum width of the entire grid.
        :return: minimum width of the grid (pix)
        """
        return self.tileMinWidth*self.width

    def getMinHeight(self):
        """
        Returns the minimum height of the entire grid.
        :return: minimum height of the grid (pix)
        """
        return self.tileMinHeight*self.height

    def refresh(self):
        """
        Refreshes every tile in the grid
        """
        for tile in self.tiles:
            tile.refresh()

    def refreshTile(self, row, col):
        """
        Refreshes a specific tile in the grid.
        :param row: Row of the tile to refresh
        :param col: Column of the tile to refresh
        """
        self.getTile(row, col).refresh()

    def setClickable(self, clickable):
        self.clickable = clickable
        for tile in self.tiles:
            tile.clickable = clickable


def emptyCallback(*args):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    rows = 5
    cols = 5

    grid = TileGrid(root, rows=rows, cols=cols, tileMinWidth=50, tileMinHeight=50)
    root.minsize(grid.getMinWidth(), grid.getMinHeight())
    grid.pack(fill='both', expand=1)

    grid.getTile(2,4).setText("hi")
    grid.getTile(0,1).setColor("red")

    root.mainloop()
