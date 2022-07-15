class Automata:
    def __init__(self, numcols, numrows, chanceOfLife):
        self.rows = numrows
        self.cols = numcols
        self.numcells = numrows * numcols

        self.cells = []
        # Make a (column) list.
        for i in range(numcols):
            column = []
            # Make a list of (row) cells for each column
            for j in range(numrows):
                cell = self.getACell(chanceOfLife)
                column.append(cell)
            self.cells.append(column)
        # self.initGraphics()

    # def repr(self):
    #   return self.cells

    ## Subclasses will override this method so that
    ## instances of their subclass of Cell will be used by
    ## the automata.
    def getACell(self, chanceOfLife):
        return Cell(chanceOfLife)

    ## Subclasses will override this method in order to
    ## position the shapes that represent the cells.
    def initGraphics(self):
        print("Warning: Automata.initGraphics() is not implemented!")

    def getAllCells(self):
        return self.cells

    def getAllStates(self):
        AllStates = []
        for i in range(self.cols):
            for j in range(self.rows):
                AllStates.append(self.cells[i][j].getState())
        return AllStates

    def countLiving(self):
        numLiving = 0.0
        for i in range(self.cols):
            for j in range(self.rows):
                numLiving += self.cells[i][j].getState()
        return numLiving

    def nextGeneration(self):
        # Move to the "next" generation
        for i in range(self.cols):
            for j in range(self.rows):
                self.cells[i][j].copyState()

        for i in range(self.cols):
            for j in range(self.rows):
                numLive = 0
                iprev = i - 1
                inext = i + 1
                jprev = j - 1
                jnext = j + 1
                # When a cell is at the outer edge we "wrap"
                if i == 0: iprev = self.cols - 1
                if j == 0: jprev = self.rows - 1
                if i == self.cols - 1: inext = 0
                if j == self.rows - 1: jnext = 0
                # Query the state of the neighborhood.
                # Cells those above___
                numLive += self.cells[iprev][jprev].getPrevState()
                numLive += self.cells[i][jprev].getPrevState()
                numLive += self.cells[inext][jprev].getPrevState()
                # Cells either side___
                numLive += self.cells[iprev][j].getPrevState()
                numLive += self.cells[inext][j].getPrevState()
                # Cells below___
                numLive += self.cells[iprev][jnext].getPrevState()
                numLive += self.cells[i][jnext].getPrevState()
                numLive += self.cells[inext][jnext].getPrevState()

                prevState = self.cells[i][j].getPrevState()
                currCell = self.cells[i][j]
                Automata.applyRulesOfLife(self, currCell, numLive)

    ## Subclasses can override this method in order to apply
    ## their own custom rules of life.
    def applyRulesOfLife(self, cell, liveNeighbors):
        if cell.prevState == 1:
            if liveNeighbors == 2 or liveNeighbors == 3:
                cell.setState(1)
            else:
                cell.setState(0)
        if cell.prevState == 0:
            if liveNeighbors == 3:
                cell.setState(1)
            else:
                cell.setState(0)