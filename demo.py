from src.mazeManager import MazeManger

def main():
    manager = MazeManger()
    manager.add_maze(40,40)
    manager.solve_maze(0,"DFS")
    manager.solve_maze(0,"BFS")

if  __name__ == "__main__":
    main()