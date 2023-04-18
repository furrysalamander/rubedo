import pickle
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from pa_result import PaResult
from visualization import generate_color_map, generate_3d_height_map
import statistics
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import gaussian_kde
from collections import Counter


def plot_scatter(data_clean: list[tuple[float, float]], dataset: str, ax):
    x, y = list(zip(*data_clean))
    p = np.polyfit(x, y, 3)
    trendline_x = np.linspace(min(x), max(x), 100)

    # Calculate the R-squared value
    y_pred = np.poly1d(p)(x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    ax.set_title(dataset)

    # Calculate the point density
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)
    ax.scatter(x, y, c=z)
    ax.plot(trendline_x, np.poly1d(p)(trendline_x))
    ax.set_xlabel("PA Value")
    ax.set_ylabel("Score")

    # add equation and R-squared annotation
    equation = f'y = {p[0]:.0f}x^3 + {p[1]:.0f}x^2 + {p[2]:.0f}x + {p[3]:.0f}'
    r2_text = f'R-squared = {r2:.2f}'
    ax.annotate(equation + '\n' + r2_text, xy=(0.1, 0.95), xycoords='axes fraction', fontsize=12, ha='left', va='top')


def generate_consistency_chart(data_clean: list[tuple[float, float]], dataset:str, ax):
    winning_results = []

    for i in range(0, len(data_clean), 10):
        x = i
        individual_scan = list(sorted(data_clean[x:x+10], key=lambda x: x[1]))
        pprint(individual_scan[0])
        winning_results.append(individual_scan[0][0])
        # pprint(data_clean[x:x+10])
    counter = Counter(winning_results)

    # fig, ax = plt.subplots()
    ax.set_ylabel("Winning Frequency")
    ax.set_xlabel("PA Value")
    ax.bar(counter.keys(), counter.values(), width=0.06/10)

    # Calculate the standard deviation of the winning results
    std_dev = statistics.stdev(winning_results)

    # Add the standard deviation as a subtitle for the plot
    ax.set_title(f"Standard deviation: {std_dev:.5e}", fontsize=10)
    # fig.suptitle(dataset)
    # return fig


def main():
    datasets = [
        ("matte_black_ambient_light.pkl", "Matte Black Print Bed, Black Filament, Ambient Lighting"),
        ("matte_black_dark.pkl", "Matte Black Print Bed, Black Filament, No Ambient Light"),
        ("matte_white_ambient_light.pkl", "Matte Black Print Bed, White Filament, Ambient Lighting"),
        ("matte_white_dark.pkl", "Matte Black Print Bed, White Filament, No Ambient Light"),
        ("pei_black_ambient_light.pkl", "PEI Print Bed, Black Filament, Ambient Light"),
        ("pei_black_dark.pkl", "PEI Print Bed, Black Filament, No Ambient Light"),
        ("pei_white_ambient_light.pkl", "PEI Print Bed, White Filament, Ambient Light"),
        ("pei_white_dark.pkl", "PEI Print Bed, White Filament, No Ambient Light"),
        ("texture_black_ambient_light.pkl", "Textured Print Bed, Black Filament, Ambient Light"),
        ("texture_black_dark.pkl", "Textured Print Bed, Black Filament, No Ambient Light"),
        ("texture_white_ambient_light.pkl", "Textured Print Bed, White Filament, Ambient Light"),
        ("texture_white_dark.pkl", "Textured Print Bed, White Filament, No Ambient Light")
    ]


    fig_scatter, axs_scatter = plt.subplots(3, 4)
    fig_bar, axs_bar = plt.subplots(3, 4)

    

    for i, dataset in enumerate(datasets):

        with open(dataset[0], "rb") as f:
            # List of tuples where tuples are the PaValue and the PaResult
            data: list[tuple[float, PaResult]] = pickle.load(f)

        data_clean: list[tuple[float, float]] = list([(x, y.score) for x, y in data])
        
        row = i // 4
        col = i % 4

        plot_scatter(data_clean, dataset[1], axs_scatter[row, col])
        generate_consistency_chart(data_clean, dataset[1], axs_bar[row, col])

        # Set the same limits for the x and y axes of all subplots
        axs_scatter[row, col].set_ylim(0, 350)

        # axs_bar[row, col].set_xlim(xlim)
        # axs_bar[row, col].set_ylim(ylim)

    # Adjust the spacing between subplots
    fig_scatter.tight_layout()
    fig_bar.tight_layout()

        # generate_3d_height_map(data[5][1])
        # generate_color_map(data[5][1])

    plt.show()

if __name__=="__main__":
    main()
