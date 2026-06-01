"""Coffee, Then Conversions - find the timing rhythm behind closed deals."""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(27)
N = 20000

hour = rng.integers(8, 19, N)
dow = rng.integers(0, 5, N)
rep_skill = rng.normal(0, 1, N)
deal_size = rng.gamma(2, 1, N)

# the rhythm: mid morning and early afternoon close best, midweek peaks
hour_effect = np.exp(-((hour - 10.5) ** 2) / 6) + 0.8 * np.exp(-((hour - 14) ** 2) / 5)
dow_effect = np.array([0.8, 1.0, 1.1, 1.0, 0.7])[dow]
p = 0.10 + 0.18 * hour_effect * dow_effect + 0.04 * rep_skill - 0.01 * deal_size
p = np.clip(p, 0.02, 0.95)
closed = rng.random(N) < p

df = pd.DataFrame({"hour": hour, "dow": dow, "closed": closed})
grid = df.pivot_table(index="dow", columns="hour", values="closed", aggfunc="mean")
best = grid.stack().idxmax()
lift = grid.max().max() / grid.min().min() - 1

print(f"Best window: day {best[0]} at {best[1]}:00")
print(f"Close rate lift from worst to best window: {lift*100:.0f}%")

os.makedirs("outputs", exist_ok=True)
plt.figure(figsize=(9, 4.5))
plt.imshow(grid.values, aspect="auto", cmap="YlOrRd")
plt.colorbar(label="close rate")
plt.yticks(range(5), ["Mon", "Tue", "Wed", "Thu", "Fri"])
plt.xticks(range(grid.shape[1]), grid.columns)
plt.xlabel("hour of day")
plt.title("Coffee, then conversions: the close rate heatmap")
plt.tight_layout()
plt.savefig("outputs/timing_of_closing.png", dpi=120)
print("Saved outputs/timing_of_closing.png")
