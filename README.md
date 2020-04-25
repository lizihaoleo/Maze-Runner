# Maze-Runner
* An experience project to practice OOP and multiple algorithm
* Generate random maze and find the solution path using different algorithm

# Baisc Algorithm
## Maze generation
A simple DFS with random selection at each step, it will walk through all cells in the m by n matrix grid, and at each step it will connect adjacency in random order.

Here is the pesudo code:

<pre><code>Initialze m * n grid of cells, each cells has 4 walls

stack = [any cell in the graph, let start at cell at (0,0)]
cell(0,0).visited = True
while stack:
    cur = stack.pop()
    for nei in neighbours of cur:
        if nei is not visited:
            nei.visited = True
            remove wall between cur and nei
            stack.append(nei)
Random pick two cells on any outter maze edges as start and end porint
@ref: https://en.wikipedia.org/wiki/Maze_generation_algorithm
</code> </pre>

### Maze example
Here is a maze example

![Here is a maze example](/MazeGenerate/maze_generation_0.png)

## Graph optimization
After generate the maze we can apply different path algorithm on the maze (such as DFS,BFS), but I realize there are many cells are useless and will waste computaional time if we keep those cells.

For example, the 2 hightlight cells can only move in one dirction, and we have spend 2 more step to calcuate this 2 cells, which case useless computation. Actually we can skip thos 2 cells casue we know we will move straghtford from end to end.
![Hallway example](/MazeGenerate/maze_hallways_0.png)

So Ideally, we can ignore those "hallway" cells, create a graph instance store all import cells and connected relationships. The maze can optimize as following graph.
![Graph example](/MazeGenerate/graph_generation_0.png)

Then we can apply different solver algorithm on the graph.
## Solvers Algorithm
### DFS/BFS
Very straightforwad idea to solve graph problem.

Here is the DFS pesudo code:
<pre><code>stack = [start]
start.visited = True
while stack:
    cur = stack.pop()
    if cur == end:
        # find the solution
        return
    for nei in neigbours of cur:
        if nei is not visited:
            nei.visited = True
            stack.append(nei)
</code></pre>
For BFS, replace stack as queue.
Time complexity will be O(m*n).

### Dijkstra
Dijkstra is an algorithm to guarantee find shortes path in the graph.
Here is the pesudo code.
<pre><code>heap = [start] # min-heap
start.dist = 0 # dist = inf by default
while heap:
    cur = heap.heappop() # heap pop the smallest dist cell
    if cur == end:
        # find the solution
        return
    for nei in neigbours of cur:
        alt = cur.dist + distance between nei and cur
        if alt < nei.dist:
            nei.dist = alt # update shortest distance btw cur and nei
            heap.heappush(nei)
</code></pre>
Time complextiy is O(ElogV), where E is number of edge and V is number of cell in the graph.

### Visualize the Result
Here is the solution result.

![Graph result example](/MazeGenerate/graph_solution_Dijkstra.png)

## Demo code
<pre><code>manager = MazeManger()
manager.add_maze(10,10,show = True, debug=True)
manager.solve_graph(0,"DFS")
manager.solve_graph(0,"BFS")
manager.solve_graph(0,"DIJ")
</code></pre>

### Output
<pre><code>Generating the maze with depth-first search...
Number of moves performed: 200
Execution time for algorithm: 0.0008

Visualize maze ...
Total execution time: 555 ms

Visualize graph ...
Total execution time: 320 ms

Solving the maze using DFS
Number of moves performed: 37
Length of solution: 16
Execution time for algorithm: 0.0001

Visualize graph solution ...
Total execution time: 369 ms

Solving the maze using BFS
Number of moves performed: 38
Length of solution: 16
Execution time for algorithm: 0.0001

Visualize graph solution ...
Total execution time: 348 ms

Solving the maze using Dijkstra
Number of moves performed: 36
Length of solution: 16
Execution time for algorithm: 0.0001

Visualize graph solution ...
Total execution time: 369 ms
</code></pre>

## Maintainer
@lizihaoleo 