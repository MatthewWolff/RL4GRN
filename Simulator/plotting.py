from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

EPSILON = 1E-12
WEIGHT_SCALING = 3  # an edge with weight 0.1 is very faint. scale it up


class CoefficientGraph:

    def __init__(self, coefficients: np.array, edge_threshold=0.0):
        """
        Initialize a graph
        :param coefficients: the real-valued coefficients to make a graph of
        :param edge_threshold: the percentile that edges must be above to be shown
        """
        self.coefficients: np.array = coefficients
        self.edge_threshold = edge_threshold

        self._validate_input()
        self._G = nx.Graph()
        self._edges = list()
        self._weights = list()
        self._make_graph()

    def _validate_input(self):
        assert isinstance(self.coefficients, np.ndarray)
        assert len(self.coefficients) == len(self.coefficients[0])  # square

        assert isinstance(self.edge_threshold, float)
        assert 0 <= self.edge_threshold < 1

    def _make_graph(self):
        # scale the coefficients to be between 0-1
        small, large = self.coefficients.min(), self.coefficients.max()
        normalized = (self.coefficients - small) / (large - small + EPSILON)

        nodes = len(self.coefficients)
        for u, v in combinations(range(nodes), 2):
            if normalized[u, v] >= self.edge_threshold:
                self._G.add_edge(u + 1, v + 1, weight=normalized[u, v])
                self._edges.append((u + 1, v + 1))
                self._weights.append(normalized[u, v] * WEIGHT_SCALING)

    def plot(self):
        pos = nx.spring_layout(self._G)
        nx.draw_networkx_nodes(self._G, pos, node_size=700)
        nx.draw_networkx_edges(self._G, pos, edgelist=self._edges, width=self._weights)
        nx.draw_networkx_labels(self._G, pos, font_size=16, font_family="sans-serif", font_color="white")
        plt.title("Network Coefficients")
        plt.show()


if __name__ == "__main__":
    c = np.random.random((10, 10))
    g = CoefficientGraph(c)
    g.plot()
