import pickle
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from pa_result import PaResult

with open("testing_adjustments.pkl", "rb") as f:
    data: list[PaResult] = pickle.load(f)

pa_values = list([x[0] for x in data[:10]])

data_clean = list([(x, y.score) for x, y in data])
pprint(list(sorted(data_clean, key=lambda x: x[1])))
x, y = list(zip(*data_clean))
p = np.polyfit(x, y, 3)
plt.plot(pa_values, np.poly1d(p)(pa_values))
plt.scatter(x, y)
plt.plot(pa_values, np.poly1d(p)(pa_values))


from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import gaussian_kde
from collections import Counter


# Calculate the point density
# xy = np.vstack([x,y])
# z = gaussian_kde(xy)(xy)

# fig, ax = plt.subplots()
# ax.set_xlabel("PA Value")
# ax.set_ylabel("Score")
# ax.scatter(x, y, c=z, s=100)
# ax.plot(pa_values, np.poly1d(p)(pa_values))


winning_results = []

for i in range(0, len(data_clean), 10):
    x = i
    individual_scan = list(sorted(data_clean[x:x+10], key=lambda x: x[1]))
    pprint(individual_scan[0])
    winning_results.append(individual_scan[0][0])
    # pprint(data_clean[x:x+10])

counter = Counter(winning_results)
print(counter)
fig, ax = plt.subplots()
ax.set_ylabel("Winning Frequency")
ax.set_xlabel("PA Value")
ax.bar(counter.keys(), counter.values(), width=0.06/10)

from visualization import generate_color_map, generate_3d_height_map
generate_color_map(data[3][1])
generate_3d_height_map(data[3][1])

plt.show()
