import numpy as np

class PatternInfo:
    def __init__(self, start_value, stop_value, start_x, start_y, num_lines, line_length, spacing) -> None:
        # TODO: honestly might be better to just have people pass in
        # the values they want to test.  It's more flexible that way.
        self.pa_values = np.linspace(start_value, stop_value, num_lines)

        self.start_x = start_x
        self.start_y = start_y
        self.line_length = line_length
        self.spacing = spacing

    def lines_start_y(self):
        return [(x * self.spacing) + self.start_y for x in range(len(self.pa_values))]
