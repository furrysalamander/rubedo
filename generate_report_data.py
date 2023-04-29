import os
import pickle
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from pa_result import PaResult
from visualization import generate_color_map, generate_3d_height_map
import statistics
from scipy.stats import gaussian_kde
from collections import Counter
from pathlib import Path


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
    ax.set_ylabel("Deviation")

    # add equation and R-squared annotation
    # equation = f'y=({p[0]:.2e})x^3+{p[1]:.0f}x^2+{p[2]:.0f}x+{p[3]:.0f}'
    equation = f"y=({p[0]:.2e})x^3" \
           f"{'-' if p[1]<0 else '+'}{abs(p[1]):.0f}x^2" \
           f"{'-' if p[2]<0 else '+'}{abs(p[2]):.0f}x" \
           f"{'-' if p[3]<0 else '+'}{abs(p[3]):.0f}"

    min_interpolated_value = trendline_x[np.argmin(np.poly1d(p)(trendline_x))]

    min_text = f"Interpolated Minimum={min_interpolated_value:.3f}"
    r2_text = f'R-squared={r2:.2f}'
    ax.annotate(equation + '\n' + r2_text + '\n' + min_text, xy=(0.99, 0.98), xycoords='axes fraction', fontsize=9, ha='right', va='top')


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

    # Add the standard deviation as an annotation for the plot
    ax.annotate(f"Standard deviation: {std_dev:.5e}", xy=(0.02, 0.95), xycoords='axes fraction',
                fontsize=10, ha='left', va='top')

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

    fig_scatter.set_figheight(10)
    fig_scatter.set_figwidth(16)
    fig_bar.set_figheight(10)
    fig_bar.set_figwidth(16)

    pad = 5 # in points
    cols = ['Black Filament, Ambient Light', 'Black Filament, No Ambient Light', 'White Filament, Ambient Light', 'White Filament, No Ambient Light']
    rows = ['Matte Black', 'PEI', 'Textured']

    for axs in [axs_bar, axs_scatter]:
        for ax, col in zip(axs[0], cols):
            ax.annotate(col, xy=(0.5, 1), xytext=(0, pad),
                        xycoords='axes fraction', textcoords='offset points',
                        size='large', ha='center', va='baseline')

        for ax, row in zip(axs[:,0], rows):
            ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                        xycoords=ax.yaxis.label, textcoords='offset points',
                        size='large', ha='right', va='center')

    for i, dataset in enumerate(datasets):

        with open(dataset[0], "rb") as f:
            # List of tuples where tuples are the PaValue and the PaResult
            data: list[tuple[float, PaResult]] = pickle.load(f)

        data_clean: list[tuple[float, float]] = list([(x, y.score) for x, y in data])
        
        row = i // 4
        col = i % 4

        plot_scatter(data_clean, '', axs_scatter[row, col])
        generate_consistency_chart(data_clean, dataset[1], axs_bar[row, col])

        # Set the same limits for the x and y axes of all subplots
        axs_scatter[row, col].set_ylim(0, 380)
        axs_bar[row, col].set_xlim(0, 0.06)
        axs_bar[row, col].set_ylim(0, 26)

        for index, scan in enumerate(data):
            print(f"{dataset[0]},{index},{scan[0]:.3f},{scan[1].score}")
        #     os.makedirs("scan_data_megadump/" + Path(dataset[0]).stem, exist_ok=True)
        #     chart = generate_3d_height_map(scan[1])
        #     chart.savefig("scan_data_megadump/" + Path(dataset[0]).stem + "/" + f"{index}_" + f"{scan[0]:.3f}_" + "3d.png")
        #     plt.close(chart)
        #     chart = generate_color_map(scan[1])
        #     chart.savefig("scan_data_megadump/" + Path(dataset[0]).stem + "/" + f"{index}_" + f"{scan[0]:.3f}_" + "color.png")
        #     plt.close(chart)

    # Adjust the spacing between subplots
    fig_scatter.tight_layout()
    fig_bar.tight_layout()

    # fig_scatter.savefig("scan_data_megadump/fig_scatter.png")
    # fig_bar.savefig("scan_data_megadump/fig_bar.png")

    plt.show()

if __name__=="__main__":
    main()
