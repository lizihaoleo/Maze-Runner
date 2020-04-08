from src.maze import Maze
from src.solver import DFS
def main():
    maze = Maze(10,10)
    solver = DFS(maze)
    path = solver.solve()
    maze.show_solution(path)

if  __name__ == "__main__":
    main()