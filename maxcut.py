"""Calculate cost value of cost function for MAXCUT"""
from math import ceil
from utils import debug
from graph import Graph


class MAXCUT:
    def __init__(self):
        self.curr_cost = float("-inf")
        self.curr_best = ""

    """Calculate the cost value of a candidate bitstring"""
    def cal_cost(self, G, bit_string):
        """Score of a candidate bitstring"""
        assert len(bit_string) == G.N

        cost_val = 0

        # for each edge (u, v), adding the weight of the edge if u, v belong to different sets
        for u, v, weight in G.weighted_edge_lst:
            debug("(u, v, weight): {}, {}, {}\n".format(u, v, weight))
            if bit_string[u] != bit_string[v]:
                cost_val += weight
        debug("Cost: {}\n".format(cost_val))

        return cost_val

    """Find optimal cost and optimal solution"""
    def find_optimal(self, G):
        """
        :return: (optimal cost, optimal solution) that is the best possible assignment for MAXCUT problem
        """
        best_cost = float("-inf")
        best_sol = []

        # Iterate all possible candidate bitstrings
        # just traverse (2^N)/2 cases due to the symmetry
        # e.g. 01111 <-> 10000
        for i in range(ceil((2 ** G.N) // 2)):
            # convert the number to bitstring
            # bin() --> xbxxxx
            bit_string = bin(i)[2:]
            bit_string = "0" * (G.N - len(bit_string)) + bit_string

            curr_cost = self.cal_cost(G=G, bit_string=bit_string)
            if curr_cost > best_cost:
                best_cost = curr_cost
                best_sol = [bit_string]
            elif curr_cost == best_cost:
                best_sol.append(bit_string)

        return best_cost, best_sol

    """Update the best cost and best solution"""
    def update_cost(self, G, bit_string):
        curr_cost = self.cal_cost(G=G, bit_string=bit_string)
        if curr_cost >= self.curr_cost:
            self.curr_cost = curr_cost
            self.curr_best = bit_string

        return curr_cost


if __name__ == "__main__":
    g = Graph(N=5, randomize=True)
    colors = ['#1f78b4' for _ in g.V]
    g.draw_graph(colors=colors, name="original_graph.png")
    mc = MAXCUT()
    mc.cal_cost(G=g, bit_string="01010")
    bc, bs = mc.find_optimal(G=g)
    print(bc, bs)
