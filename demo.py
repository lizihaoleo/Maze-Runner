from src.mazeManager import MazeManger

def main():
    manager = MazeManger()
    manager.add_maze(10,10,show = True, debug=True)
    manager.solve_graph(0,"DFS")
    manager.solve_graph(0,"BFS")
    manager.solve_graph(0,"DIJ")


if  __name__ == "__main__":
    main()