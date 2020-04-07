class Cell(object):
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.visited = False
        self.is_entry_exit = None
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

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