from src.maze import Maze
from collections import deque
import logging
import time

class Solver(object):
    def __init__(self,maze, quiet_mode):
        self.maze = maze
        self.name = None
        self.quiet_mode = quiet_mode
        self.path = list()

    def solve(self):
        raise NotImplementedError

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

class DFS(Solver):
    def __init__(self, maze, quiet_mode = False):
        super().__init__(maze, quiet_mode)
        self.name = "DFS"

    def solve(self):
        print("Solving the maze")
        start_row, start_col = self.maze.entry_coor

        self.maze.grid[start_row][start_col].visited = True
        stack = [(start_row,start_col)]

        completed = False
        step = 1
        time_start = time.clock()
        # print("*", self.maze.entry_coor,self.maze.exit_coor)
        while stack:
            cur_row, cur_col = stack.pop()
            step += 1
            if (cur_row, cur_col) == self.maze.exit_coor:
                completed = True
                break
            self.maze.grid[cur_row][cur_col].visited = True
            neis = self.maze.find_valid_neis(cur_row, cur_col)
            for nei in neis:
                if nei and not self.maze.grid[nei[0]][nei[1]].visited:
                    stack.append(nei)
                    
                    self.maze.grid[nei[0]][nei[1]].prev = (cur_row, cur_col)
                # print('Current {} -> next {} stack {}'.format((cur_row, cur_col),nei,stack))
        
        if not self.quiet_mode:
            print("Number of moves performed: {}".format(step))
            print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))

        
        path = deque()
        current = self.maze.exit_coor

        while current != None and completed:
            path.appendleft(current)
            row, col = current[0], current[1]
            current = self.maze.grid[row][col].prev
        return path





