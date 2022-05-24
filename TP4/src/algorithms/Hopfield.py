import numpy as np

from utils.HopfieldParameters import HopfieldParameters


class Hopfield:

    def __init__(self, parameters: HopfieldParameters, patterns):
        self.patterns = np.transpose(patterns)
        self.w = (1 / len(patterns)) * np.matmul(self.patterns, np.transpose(self.patterns))
        np.fill_diagonal(self.w, 0)
        self.parameters = parameters

    def predict(self, x):
        stable = False
        i = 0
        results = []

        prev_state = np.sign(np.matmul(self.w, x))
        results.append(prev_state)

        while not stable and i < self.parameters.max_iterations:
            next_state = np.sign(np.matmul(self.w, prev_state))

            if np.array_equal(next_state, prev_state):
                stable = True
            else:
                results.append(next_state)
                prev_state = next_state

        return results
