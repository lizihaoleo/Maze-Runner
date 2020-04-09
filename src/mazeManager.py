from src.maze import Maze
from src.solver import DFS,BFS

class MazeManger(object):
    def __init__(self):
        self.mazes = []

    def add_maze(self,row,col,id=0):
        if id is not 0:
            self.mazes.append(Maze(row, col, id))
        else:
            if len(self.mazes) < 1:
                self.mazes.append(Maze(row, col, 0))
            else:
                self.mazes.append(Maze(row, col, len(self.mazes) + 1))

        return self.mazes[-1]

    def get_maze(self, id):
        for maze in self.mazes:
            if maze.id == id:
                return maze
        print("Unable to locate maze")
        return None
    
    def solve_maze(self, maze_id, method, show_solution = True):
        maze = self.get_maze(maze_id)
        if not maze:
            print("No valid maze")
            return 
        if method == "DFS":
            solver = DFS(maze)
        elif method == "BFS":
            solver = BFS(maze)
        else:
            print("Not valid solver method name")
            return
        path = solver.solve()
        if show_solution:
            maze.show_solution(path,solver)
        return path

    