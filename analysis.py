import numpy as np
from constants import *

def brightest_average(pixel_values: np.ndarray):
    brightest_pixels = np.argsort(pixel_values)[-3:]
    line_brightest_x = FRAME_SIZE_X - np.average(brightest_pixels)
    return line_brightest_x


def weighted_average(pixel_values: np.ndarray):
    normalized_values = pixel_values / 255
    adjusted_values = normalized_values ** 100
    x_values = np.arange(adjusted_values.size)
    if adjusted_values.max() == 0:
        # FIXME: I need an appropriate solution for what to do if there are no non-zero values.
        return 70
    return FRAME_SIZE_X - np.average(x_values, weights=adjusted_values)


def first_non_zero(pixel_values: np.ndarray):
    try:
        return np.nonzero(pixel_values)[0][0]
    except:
        print()


def count_non_zero(pixel_values: np.ndarray):
    return np.count_nonzero(pixel_values)


def compute_x_value(pixel_values: np.ndarray):
    algorithms = {
        "brightest_avg": brightest_average,
        "weighted_avg": weighted_average,
        "first_non_zero": first_non_zero,
        "count_non_zero": count_non_zero,
    }
    # return algorithms["brightest_avg"](pixel_values)
    # return algorithms["count_non_zero"](pixel_values)
    # return algorithms["first_non_zero"](pixel_values)
    return algorithms["weighted_avg"](pixel_values)
