from src.maze import Maze
from src.graph import Graph
from src.solver import DFS,BFS,Dijkstra

class MazeManger(object):
    def __init__(self):
        self.graphs = []
        self.mazes = []

    def add_maze(self,row,col,id=0, show = True, debug=False): # return a optimize graph instead of maze instance
        if id is not 0:
            self.mazes.append(Maze(row, col, id, show, debug))
        else:
            if len(self.mazes) < 1:
                self.mazes.append(Maze(row, col, 0, show, debug))
            else:
                self.mazes.append(Maze(row, col, len(self.mazes) + 1, show, debug))

        graph = Graph(self.mazes[-1],show,debug)
        self.graphs.append(graph)
        return self.graphs[-1]

    def get_maze(self, id):
        for maze in self.mazes:
            if maze.id == id:
                return maze
        print("Unable to locate maze")
        return None

    def get_graph(self, id):
        for graph in self.graphs:
            if graph.id == id:
                return graph
        print("Unable to locate graph")
        return None

    def solve_graph(self, graph_id, method, show_solution = True):
        graph = self.get_graph(graph_id)
        if not graph:
            print("No valid graph")
            return 
        if method == "DFS":
            solver = DFS(graph)
        elif method == "BFS":
            solver = BFS(graph)
        elif method == "DIJ":
            solver = Dijkstra(graph)
        else:
            print("Not valid solver method name")
            return
        path = solver.solve()
        if show_solution:
            graph.show_solution(path,solver)
        return path
    