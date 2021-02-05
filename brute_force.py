import numpy as np
from matplotlib import pyplot as plt
from qiskit import IBMQ
from utils import debug
from graph import Graph
from qaoa import myQAOA
from maxcut import MAXCUT


def create_weight_matrix(G):
    """Creation of a weight matrix with w[i,j] <-> weight of edges connecting between node i and node j"""
    w = np.zeros([G.N, G.N])
    for i, j, weight in G.weighted_edge_lst:
        w[i, j] = weight
        w[j, i] = weight

    debug("weigth matrix\n")
    print(w)

    return w


def brute_force(G, w):
    best_cost_brute = float("-inf")
    xbest_brute = []
    for b in range(2**G.N):
        x = [int(t) for t in reversed(list(bin(b)[2:].zfill(G.N)))]
        cost = 0
        for i in range(G.N):
            for j in range(G.N):
                cost = cost + w[i,j]*x[i]*(1-x[j])
        if best_cost_brute < cost:
            best_cost_brute = cost
            xbest_brute = x
        debug('case = ' + str(x) + ' cost = ' + str(cost) + '\n')

    # plt.figure(2)
    colors = ['r' if xbest_brute[i] == 0 else 'c' for i in range(G.N)]
    # draw_graph(G, colors, pos)
    G.draw_graph(colors=colors, name="brute-force_result_graph.png")
    debug('\nBest solution from Brute-Force = ' + str(xbest_brute) + ' cost = ' + str(best_cost_brute) + '\n')


if __name__ == "__main__":
    g = Graph(N=10, randomize=True)
    plt.figure(1)
    colors = ['#1f78b4' for _ in g.V]
    g.draw_graph(colors=colors, name="original_graph.png")

    # Brute force approach
    w = create_weight_matrix(G=g)
    brute_force(G=g, w=w)

    # # load IBMQ account
    # IBMQ.load_account()
    # provider = IBMQ.get_provider()
    # debug("Available backends: {}\n".format(provider.backends()))
    # # use IBMQ backend
    # simulator = provider.get_backend('ibmq_qasm_simulator', hub=None)
    #
    # # QAOA algorithm
    # qaoa = myQAOA(params=(np.pi, np.pi), G=g, simulator=simulator)
    # qaoa.circuit_formulate()
    # # qaoa.draw_circuit()
    # qaoa.run_simulator()
    # qaoa.draw_histogram()
    #
    # problem = MAXCUT()
    # qaoa.cal_expectation(problem=problem)
