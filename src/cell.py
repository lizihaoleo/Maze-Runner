class Cell(object):
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.position = (row,col)
        self.visited = False
        self.is_entry_exit = None
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.neis = set()
        self.prev = None #this filed helps to reverse look up solution path
        self.dist = float('inf') #this field use in dijkstra algorithm

    def __repr__(self):
            return "({},{}) d:{}".format(self.row, self.col,self.dist)

    def __str__(self):
        return self.__repr__()

    # def __hash__(self):
    #     return id(self)

    def __lt__(self, obj):
        """self < obj."""
        return (self.dist) < (obj.dist)


    def set_entry_exit(self,is_entry_exit,row_limit,col_limit):
        if self.row == 0:
            self.walls["top"] = False
        elif self.row == row_limit:
            self.walls["bottom"] = False
        elif self.col == 0:
            self.walls["left"] = False
        elif self.col == col_limit:
            self.walls["right"] = False

        self.is_entry_exit = is_entry_exit

    def connect(self,other_cell):
        neighbour_row, neighbour_col = other_cell.row, other_cell.col
        if self.row - neighbour_row == 1:
            self.walls["top"] = False
            return True
        elif self.row - neighbour_row == -1:
            self.walls["bottom"] = False
            return True
        elif self.col - neighbour_col == 1:
            self.walls["left"] = False
            return True
        elif self.col - neighbour_col == -1:
            self.walls["right"] = False
            return True
        return False

    def is_walls_between(self, neighbour):
        """Function that checks if there are walls between self and a neighbour cell.
        Returns true if there are walls between. Otherwise returns False.

        Args:
            neighbour The cell to check between

        Return:
            True: If there are walls in between self and neighbor
            False: If there are no walls in between the neighbors and self

        """
        if self.row - neighbour.row == 1 and self.walls["top"] and neighbour.walls["bottom"]:
            return True
        elif self.row - neighbour.row == -1 and self.walls["bottom"] and neighbour.walls["top"]:
            return True
        elif self.col - neighbour.col == 1 and self.walls["left"] and neighbour.walls["right"]:
            return True
        elif self.col - neighbour.col == -1 and self.walls["right"] and neighbour.walls["left"]:
            return True

        return False

    def is_hallway(self):
        if not self.walls["top"] and not self.walls["bottom"] and self.walls["left"] and self.walls["right"]:
            return True
        elif not self.walls["left"] and not self.walls["right"] and self.walls["top"] and self.walls["bottom"]:
            return True
        return False

