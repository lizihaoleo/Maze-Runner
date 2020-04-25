from src.mazeManager import MazeManger
from src.maze import Maze
from src.graph import Graph
def main():
    manager = MazeManger()
    manager.add_maze(40,40,show = True, debug=True)
    manager.solve_graph(0,"DFS")
    manager.solve_graph(0,"BFS")
    manager.solve_graph(0,"DIJ")


if  __name__ == "__main__":
    main()