from itertools import product as prod

import networkx as nx
from common import print_results, readline


FAVORITE = 1350
SOURCE = (1, 1)
TARGET = tuple(map(int, readline(__file__).split(',')))
MAX_EXPANSION = 50
MAX_DISTANCE = 50

class Maze:
    def __init__(self):
        self.graph = nx.Graph()
        self.__set_up_graph()

        # Find shortest path to each node starting at 'SOURCE'.
        self.shortest_paths = nx.shortest_path_length(self.graph, source=SOURCE)

    # Set up a graph where the nodes are the open spaces. Neighboring open
    # spaces are connected by an edge.
    def __set_up_graph(self):
        for i, j in prod(range(0, MAX_EXPANSION), repeat=2):
            if self.__is_open_space(i, j):
                for k, l in list(prod([-1, 1], [0])) + list(prod([0], [-1, 1])):
                    if self.__is_open_space(i + k, j + l):
                        self.graph.add_edge((i, j), (i + k, j + l))

    def __is_open_space(self, x, y):
        if x < 0 or y < 0:
            return False
        return format((x + y)**2 + 3*x + y + FAVORITE, 'b').count('1') % 2 == 0

    def get_number_paths_not_longer_than(self, threshold):
        return sum(1 for i in self.shortest_paths.values() if i <= threshold)

#### Main Part.

maze = Maze()

print_results(
    maze.shortest_paths[TARGET],
    maze.get_number_paths_not_longer_than(MAX_DISTANCE)
)
