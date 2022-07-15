class Cell:
    def __init__(self, chance):
        self.prevState = 0
        self.state = 0
        self.lived = 0
        if random.random() <= chance:
            self.prevState = 1
            self.state = 1
            self.lived += 1

    def getState(self):
        return self.state

    ## Subclasses will override this method in order to
    ## update the appearance of the shape that represents
    ## a cell.
    def setState(self, state):
        self.state = state
        if state == 1:
            self.lived += 1

    def getPrevState(self):
        return self.prevState

    def setPrevState(self, state):
        self.prevState = state

    def copyState(self):
        self.prevState = self.state

    def getNumLived(self):
        return self.lived