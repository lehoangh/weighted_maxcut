"""QAOA implementation (from https://qiskit.org/textbook/ch-applications/qaoa.html)"""
import numpy as np
from matplotlib import pyplot as plt
from qiskit import IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
from qiskit.visualization import plot_histogram
from utils import debug
from graph import Graph
from maxcut import MAXCUT


pbar = None


class myQAOA:
    def __init__(self, problem, params, G, simulator, NUM_SHOTS=1024):
        self.params = params
        self.G = G
        self.problem = problem
        self.simulator = simulator
        self.NUM_SHOTS = NUM_SHOTS
        self.quantum_circuit = None
        self.histogram = None
        self.runs = []

    """formulate the circuit"""
    def circuit_formulate(self):
        global pbar

        gamma, beta = self.params

        debug("Gamma: {}, beta: {}\n".format(gamma, beta))

        # construct quantum circuit
        quantum_reg = QuantumRegister(self.G.N)
        classical_reg = ClassicalRegister(self.G.N)
        quantum_circuit = QuantumCircuit(quantum_reg, classical_reg)

        # apply Hadamard gate to all inputs
        for i in range(self.G.N):
            quantum_circuit.h(quantum_reg[i])
        quantum_circuit.barrier()

        # apply the Ising type gates with angle gamma along the edges in weighted_edge_lst
        for u, v, weight in self.G.weighted_edge_lst:
            quantum_circuit.cp(-2 * gamma * weight, u, v)
            quantum_circuit.p(gamma, u)
            quantum_circuit.p(gamma, v)
        quantum_circuit.barrier()

        # then apply the single qubit X rotations with angle beta to all vertices
        for i in range(self.G.N):
            quantum_circuit.rx(2 * beta, quantum_reg[i])

        # finally measure the result in the computational basis
        quantum_circuit.barrier()
        quantum_circuit.measure(quantum_reg, classical_reg)

        self.quantum_circuit = quantum_circuit

    """draw quantum circuit"""
    def draw_circuit(self):
        # draw the circuit
        self.quantum_circuit.draw(output="mpl")

    """run simulator"""
    def run_simulator(self):
        simulate = execute(self.quantum_circuit, backend=self.simulator, shots=self.NUM_SHOTS)
        results = simulate.result()
        results_histogram = results.get_counts(self.quantum_circuit)

        print("Finish\n")

        print("Results: \n{}".format(results))
        print("Histogram: \n{}".format(results_histogram))
        self.histogram = results_histogram

    """calculate expectation value"""
    def cal_expectation(self):
        # calculate the expectation value of a candidate bitstring
        exp = 0
        for bit_string, freq in self.histogram.items():
            prob = np.float(freq) / self.NUM_SHOTS
            cost_val = self.problem.update_cost(G=self.G, bit_string=bit_string)
            print("Cost: {}".format(cost_val))

            # expectation value
            exp += prob * cost_val

        print("QAOA Results: \n")
        print("\tExpected Value: {}\n".format(exp))
        print("\tBest Found Solution: {}, {}\n".format(self.problem.curr_cost, self.problem.curr_best))

    """add each iteration"""
    def add_iter(self, gamma, beta, expected_value):
        """save data from each run of iteration"""
        self.runs.append([gamma, beta, expected_value])

    """draw histogram of candidate bitstrings"""
    def draw_histogram(self):
        plot_histogram(self.histogram)
        plt.savefig("histogram.png", format="PNG")
        plt.show()

    """draw the result graph"""
    def draw_result_graph(self):
        # plt.figure(3)
        colors = ['r' if self.problem.curr_best[i] == '0' else 'c' for i in range(self.G.N)]
        self.G.draw_graph(colors=colors, name="qaoa_result_graph.png")
        debug('\nBest solution from QAOA = ' + str(self.problem.curr_best) + ' cost = ' + str(self.problem.curr_cost) + '\n')


if __name__ == "__main__":
    g = Graph(N=5, randomize=True)
    colors = ['#1f78b4' for _ in g.V]
    g.draw_graph(colors=colors, name="original_graph.png")

    # load IBMQ account
    IBMQ.load_account()
    provider = IBMQ.get_provider()
    print("Available backends: {}".format(provider.backends()))
    # use IBMQ backend
    simulator = provider.get_backend('ibmq_qasm_simulator', hub=None)

    problem = MAXCUT()
    qaoa = myQAOA(problem=problem, params=(np.pi, np.pi), G=g, simulator=simulator)
    qaoa.circuit_formulate()
    # qaoa.draw_circuit()
    qaoa.run_simulator()
    qaoa.cal_expectation()
    qaoa.draw_result_graph()