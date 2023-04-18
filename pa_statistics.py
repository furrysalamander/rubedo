from pa_result import PaResult
import numpy as np

class PaStatistics:
    def __init__(self, lines: list[PaResult], output_directory):
        self.lines = lines
        self.output_directory = output_directory
        self.scores = list([x.score for x in lines])

    def average_deviation(self):
        return np.average(self.scores)

    def generate_graphs():
        pass

    def generate_height_maps():
        pass

    def __str__(self) -> str:
        return \
f"""Average deviation: {self.average_deviation()}
"""
