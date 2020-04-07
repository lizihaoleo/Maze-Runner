from src.cell import Cell
import time
import random
import math
import matplotlib.pyplot as plt
import os

class Maze(object):
    def __init__(self, num_rows, num_cols,show_maze = True):
        self.cell_size = 1
        self.media_filename = os.getcwd()
        print(self.media_filename)
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.grid_size = num_rows*num_cols
        self.entry_coor = self.pick_random_point_on_boundaries(None)
        self.exit_coor = self.pick_random_point_on_boundaries(self.entry_coor)
        self.generation_path = []
        self.solution_path = None
        self.initial_grid = self.generate_grid()
        self.grid = self.initial_grid
        self.generate_maze()
        if show_maze:
            self.show_maze()

    def pick_random_point_on_boundaries(self,entry_point=None):
        '''
        Return random point on the boundaries and return point must be diff than entry_point
        '''
        random_point = entry_point
        while random_point == entry_point:
            random_side = random.randint(0,3)
            if random_side == 0: # top
                random_point = (0, random.randint(0,self.num_cols-1))
            elif random_point == 1: # bottom
                random_point = (self.num_rows-1, random.randint(0,self.num_cols-1))
            elif random_side == 2: # left
                random_point = (random.randint(0, self.num_rows-1), 0)
            else: # right
                random_point = (random.randint(0, self.num_rows-1), self.num_cols-1)
        return random_point

    def generate_grid(self):
        grid = list()

        # Place a Cell object at each location in the grid
        for i in range(self.num_rows):
            grid.append(list())

            for j in range(self.num_cols):
                grid[i].append(Cell(i, j))

        return grid

    def find_unvisited_neis(self,row,col):
        dirs = [[1,0],[-1,0],[0,1],[0,-1]]
        neis = list()
        for delta_x, delta_y in dirs:
            if self.unvisited_cell(row+delta_x, col+delta_y):
                neis.append((row+delta_x, col+delta_y))
        return neis

    def unvisited_cell(self,row,col):
        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            return self.grid[row][col].visited == False
            

    def generate_maze(self,start_coor = (0,0)):
        cur_row, cur_col = start_coor
        # solution_path = [start_coor]
        self.grid[cur_row][cur_col].visited = True
        visit_counter = 1
        stack = [start_coor]

        print("Generating the maze with depth-first search...")
        time_start = time.clock()

        while stack:
            cur_row, cur_col = stack.pop()
            neis = self.find_unvisited_neis(cur_row,cur_col)
            if neis:
                stack.append((cur_row,cur_col))
                nxt_row, nxt_col = random.choice(neis)
                self.grid[cur_row][cur_col].connect(self.grid[nxt_row][nxt_col])
                self.grid[nxt_row][nxt_col].connect(self.grid[cur_row][cur_col])
                self.grid[nxt_row][nxt_col].visited = True
                stack.append((nxt_row, nxt_col))
            visit_counter += 1

        print("Number of moves performed: {}".format(visit_counter))
        print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))

        self.grid[self.entry_coor[0]][self.entry_coor[1]].set_entry_exit("entry",
            self.num_rows-1, self.num_cols-1)
        self.grid[self.exit_coor[0]][self.exit_coor[1]].set_entry_exit("exit",
            self.num_rows-1, self.num_cols-1)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.grid[i][j].visited = False      # Set all cells to unvisited before returning grid

        # self.generation_path = solution_path

    def show_maze(self):
        # Create the plot figure and style the axes
        fig = self.configure_plot()

        # Plot the walls on the figure
        self.plot_walls()

        # Display the plot to the user
        plt.show()

        if self.media_filename:
            fig.savefig("{}{}.png".format(self.media_filename, "_generation"))

    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        fig = plt.figure(figsize = (7, 7*self.num_rows/self.num_cols))

        # Create the axes
        self.ax = plt.axes()

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        title_box = self.ax.text(0, self.num_rows + self.cell_size + 0.1,
                            r"{}$\times${}".format(self.num_rows, self.num_cols),
                            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return fig

    def plot_walls(self):
        """ Plots the walls of a maze. This is used when generating the maze image"""
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize=7, weight="bold")
                elif self.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize=7, weight="bold")
                if self.initial_grid[i][j].walls["top"]:
                    self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
                                 [i*self.cell_size, i*self.cell_size], color="k")
                if self.initial_grid[i][j].walls["right"]:
                    self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                                 [i*self.cell_size, (i+1)*self.cell_size], color="k")
                if self.initial_grid[i][j].walls["bottom"]:
                    self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                                 [(i+1)*self.cell_size, (i+1)*self.cell_size], color="k")
                if self.initial_grid[i][j].walls["left"]:
                    self.ax.plot([j*self.cell_size, j*self.cell_size],
                                 [(i+1)*self.cell_size, i*self.cell_size], color="k")
