from collections import defaultdict
from src.cell import Cell
from src.timer import timeit
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
class Graph:

    def __init__(self, maze, show = False, debug = False):
        self.total_size = maze.grid_size
        self.num_rows = maze.num_rows
        self.num_cols = maze.num_cols
        self.id = maze.id
        self.debug = debug
        self.rows = defaultdict(list)
        self.cols = defaultdict(list)
        self.grid = defaultdict()
        self.start = None
        self.end = None
        self.init_graph(maze)
        self.cell_size = 1
        self.media_filename = maze.media_filename
        if show:
            self.show_graph()

    @timeit
    def init_graph(self,maze):
        for i in range(maze.num_rows):
            for j in range(maze.num_cols):
                cell = maze.grid[i][j]
                if not cell.is_hallway():
                    if len(self.rows[i]) >= 1:
                        pre = self.rows[i][-1]
                        if maze.no_wall_in_row_between(pre.position, cell.position):
                            pre.neis.add(cell)
                            cell.neis.add(pre)
                            if self.debug:
                                print("{} connect to {} at row #{}".format(pre,cell,i))

                    if len(self.cols[j]) >= 1:
                        pre = self.cols[j][-1]
                        if maze.no_wall_in_col_between(pre.position, cell.position):
                            pre.neis.add(cell)
                            cell.neis.add(pre)
                            if self.debug:
                                print("{} connect to {} at col #{}".format(pre,cell,j))
                    self.rows[i].append(cell)
                    self.cols[j].append(cell)
                    self.grid[(i,j)] = cell

                if cell.is_entry_exit == "entry":
                    self.start = cell
                elif cell.is_entry_exit == "exit":
                    self.end = cell

    def find_valid_neis(self,position):
        cell = self.grid[position]
        return cell.neis

    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        self.fig = plt.figure(figsize = (7, 7*len(self.rows)/len(self.cols)))

        # Create the axes
        self.ax = plt.axes()

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        title_box = self.ax.text(0, len(self.rows) + self.cell_size + 0.1,
                            r"{}$\times${}".format(len(self.rows), len(self.cols)),
                            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return self.fig

    def plot_graph(self):
        offset = self.cell_size / 2
        for row in self.rows.values():
            for node in row:
                # draw the graph node on the maze
                i,j = node.position[0] + offset, node.position[1] + offset
                color = 'r' if node.is_entry_exit!=None else 'g'
                circle = patches.Circle((j*self.cell_size,i*self.cell_size),self.cell_size*.25,linewidth=1,alpha=.5,facecolor=color)
                self.ax.add_patch(circle)
                # connect all its neis
                for nei in node.neis:
                    nei_i, nei_j = nei.position[0] + offset, nei.position[1] + offset
                    plt.plot([nei_j,j],[nei_i,i],color='green',linewidth=2,alpha=.5)

    def plot_solution(self, path):
        for idx in range(1,len(path)):
            pre = path[idx-1]
            cur = path[idx]
            # draw pre node first
            self.draw_rec(pre[0],pre[1])

            if pre[0] == cur[0]: #same row
                i = pre[0]
                left ,right = min(pre[1], cur[1]), max(pre[1], cur[1])
                for j in range(left+1,right):
                    self.draw_rec(i,j)
            elif pre[1] == cur[1]: #same col
                j = pre[1]
                lo, hi = min(pre[0],cur[0]), max(pre[0],cur[0])
                for i in range(lo+1,hi):
                    self.draw_rec(i,j)
        self.draw_rec(cur[0],cur[1])

    def draw_rec(self,i,j):
        rect = patches.Rectangle((j*self.cell_size,i*self.cell_size),self.cell_size,self.cell_size,linewidth=1,alpha=.25,facecolor='r')
        self.ax.add_patch(rect)

    @timeit
    def show_graph(self):
        print("\nVisualize graph ...")
        # Create the plot figure and style the axes
        fig = self.configure_plot()

        # Plot the walls and graph nodes on the figure
        self.plot_graph()

        # Display the plot to the user
        # plt.show()

        if self.media_filename:
            fig.savefig("{}{}{}.png".format(self.media_filename, "/graph_generation_",self.id))

    @timeit
    def show_solution(self,path,solver):
        print("\nVisualize graph solution ...")
        # Create the figure and style the axes
        fig = self.configure_plot()

        self.plot_graph()
        self.plot_solution(path)

        # Display the plot to the user
        # plt.show()

        # Handle any saving
        if self.media_filename:
            fig.savefig("{}{}{}.png".format(self.media_filename, "/graph_solution_",solver.name))
