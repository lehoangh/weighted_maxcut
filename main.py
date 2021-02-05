# This is a main Python script for solving a weighted maximum cut problem.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
from matplotlib import pyplot as plt
from graph import Graph
from qiskit import IBMQ
from utils import debug
from brute_force import create_weight_matrix, brute_force
from qaoa import myQAOA
from maxcut import MAXCUT


def main():
    """create an undirected graph with weights on edges"""
    g = Graph(N=10, randomize=True)
    colors = ['#1f78b4' for _ in g.V]
    g.draw_graph(colors=colors, name="original_graph.png")

    # Brute force approach
    w = create_weight_matrix(G=g)
    brute_force(G=g, w=w)

    # load IBMQ account
    IBMQ.load_account()
    provider = IBMQ.get_provider()
    debug("Available backends: {}\n".format(provider.backends()))
    # use IBMQ backend
    simulator = provider.get_backend('ibmq_qasm_simulator', hub=None)

    problem = MAXCUT()
    # QAOA algorithm
    qaoa = myQAOA(problem=problem, params=(np.pi, np.pi), G=g, simulator=simulator)
    qaoa.circuit_formulate()
    # qaoa.draw_circuit()
    qaoa.run_simulator()
    qaoa.draw_histogram()
    qaoa.cal_expectation()
    qaoa.draw_result_graph()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
