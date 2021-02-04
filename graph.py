"""Define Graph class"""
from random import randint, choice
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.patches import Circle


class Graph:
    """initial function"""
    def __init__(self, N, randomize=True, edges_lst=list()):
        """
        :param N: number of nodes
        :param randomize: initialize weights of edges ramdomly
        :param edges_lst: list of weighted edges (u, v, weight)
        G: a NetworkX graph
        V: list of vertices
        E: number of edges
        """
        self.G = nx.Graph()
        self.N = N
        self.V = np.arange(0, N, 1)
        self.E = 0
        self.weighted_edge_lst = []
        self.colors = []

        # add nodes
        self.G.add_nodes_from(self.V)
        # set colors
        self.colors = ['#1f78b4' for _ in self.G.nodes()]

        if randomize:
            self.randomize()
        else:
            self.E = len(edges_lst)
            self.G.add_weighted_edges_from(edges_lst)

    """random generate edges"""
    def randomize(self):
        # generate list of tuples for all possible edges
        all_edges = set([(u, v) for u in range(self.N) for v in range(self.N) if u != v])
        # print("All edges: {}".format(all_edges))

        # sanity check, ensure generate the correct number of edges
        num_edges_gen = len(all_edges) / 2
        num_edges_theory = self.N * (self.N - 1) / 2
        assert num_edges_gen == num_edges_theory, "%d != %d" % (num_edges_gen, num_edges_theory)

        # choose a random number of edges
        num_edges = randint(1, len(all_edges) // 2)
        # debug("Number of selected edges: {}\n".format(num_edges))
        for i in range(num_edges):
            # choose an edge, remove it and its reverse directed edge
            edge = choice(list(all_edges))
            # debug("Selected edge: {}\n".format(edge))
            all_edges.remove(edge)
            all_edges.remove(edge[::-1])
            # debug("After moving, all edges: {}\n".format(all_edges))

            # unpack tuple into vertex index
            u, v = edge

            # generate a random weight for each edge
            print("Weight of edges:")
            weight = randint(1, 100)
            print(u, v, weight)

            self.weighted_edge_lst.append((u, v, weight))

        # add edges
        self.add_edge()

    """add edges method into graph"""
    def add_edge(self):
        self.E += 1
        self.G.add_weighted_edges_from(self.weighted_edge_lst)

    """draw"""
    def draw_graph(self, colors, name):
        pos = nx.nx_agraph.graphviz_layout(self.G)
        nx.draw_networkx(self.G, node_color=colors, pos=pos)
        labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=labels)
        plt.title(name)
        if name != "original_graph.png":
            red_circle = Circle((0.5, 0.5), radius=0.25, label='0-value', facecolor='r')
            blue_circle = Circle((0.5, 0.5), radius=0.25, label='1-value', facecolor='c')
            plt.legend(handles=[red_circle, blue_circle])
        plt.savefig(name, format="PNG")
        plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Graph(N=6, randomize=True)
    print(g)
    colors = ['#1f78b4' for _ in g.V]
    g.draw_graph(colors=colors, name="original_graph.png")
