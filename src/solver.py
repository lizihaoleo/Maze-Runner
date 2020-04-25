from src.maze import Maze
from src.cell import Cell
from src.graph import Graph
from collections import deque
import logging
import time
from heapq import heappop, heappush

class Solver(object):
    def __init__(self,graph, quiet_mode):
        self.graph = graph
        self.name = None
        self.quiet_mode = quiet_mode
        self.path = list()

    def solve(self):
        raise NotImplementedError

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def reset_graph(self):
        for row_id in self.graph.rows.keys():
            for cell in self.graph.rows[row_id]:
                cell.visited = False
                cell.prev = None

class DFS(Solver):
    def __init__(self, maze, quiet_mode = False):
        super().__init__(maze, quiet_mode)
        self.name = "DFS"

    def solve(self):
        print("\nSolving the maze using {}".format(self.name))
        
        self.graph.start.visited = True
        stack = [self.graph.start.position]

        completed = False
        step = 1
        time_start = time.clock()
        # print("*", self.maze.entry_coor,self.maze.exit_coor)
        while stack:
            cur_pos = stack.pop()
            step += 1
            if cur_pos == self.graph.end.position:
                completed = True
                break

            self.graph.grid[cur_pos].visited = True
            neis = self.graph.find_valid_neis(cur_pos)
            for nei in neis:
                if nei and not nei.visited:
                    stack.append(nei.position)
                    
                    self.graph.grid[nei.position].prev = cur_pos
                # print('Current {} -> next {} stack {}'.format((cur_row, cur_col),nei,stack))

        path = deque()
        cur_pos = self.graph.end.position

        while cur_pos != None and completed:
            path.appendleft(cur_pos)
            cur_pos = self.graph.grid[cur_pos].prev
        
        self.reset_graph()

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(step))
            print("Length of solution: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
        
        return path

class BFS(Solver):
    def __init__(self, maze, quiet_mode = False):
        super().__init__(maze, quiet_mode)
        self.name = "BFS"

    def solve(self):
        print("\nSolving the maze using {}".format(self.name))
        
        self.graph.start.visited = True
        queue = deque()
        queue.append(self.graph.start.position)

        completed = False
        step = 1
        time_start = time.clock()
        # print("*", self.maze.entry_coor,self.maze.exit_coor)
        while queue:
            cur_pos = queue.popleft()
            step += 1
            if cur_pos == self.graph.end.position:
                completed = True
                break

            self.graph.grid[cur_pos].visited = True
            neis = self.graph.find_valid_neis(cur_pos)
            for nei in neis:
                if nei and not nei.visited:
                    queue.append(nei.position)
                    
                    self.graph.grid[nei.position].prev = cur_pos
                # print('Current {} -> next {} stack {}'.format((cur_row, cur_col),nei,stack))

        path = deque()
        cur_pos = self.graph.end.position

        while cur_pos != None and completed:
            path.appendleft(cur_pos)
            cur_pos = self.graph.grid[cur_pos].prev
        
        self.reset_graph()

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(step))
            print("Length of solution: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
        
        return path

class Dijkstra(Solver):
    def __init__(self, maze, quiet_mode = False):
        super().__init__(maze, quiet_mode)
        self.name = "Dijkstra"
    
    def dist_between(self,cur,nei):
        x,y = cur.position
        a, b = nei.position
        return abs(x - a) + abs(y - b)

    def solve(self):
        print("\nSolving the maze using {}".format(self.name))
        
        self.graph.start.dist = 0
        heap = [self.graph.start]
        
        step = 1
        completed = False
        time_start = time.clock()
        while heap:
            step += 1
            # print(heap)
            cur = heappop(heap)

            if cur == self.graph.end:
                completed = True
                break

            for nei in cur.neis:
                alt = cur.dist + self.dist_between(cur,nei)
                if alt < nei.dist:
                    nei.dist = alt
                    heappush(heap,nei)
                    nei.prev = cur.position


        path = deque()
        cur_pos = self.graph.end.position

        while cur_pos != None and completed:
            path.appendleft(cur_pos)
            cur_pos = self.graph.grid[cur_pos].prev
        
        self.reset_graph()

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(step))
            print("Length of solution: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
        
        return path