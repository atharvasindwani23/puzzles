"""Generate the figure for the README: the distribution of the LONGEST cycle
length in a random permutation of 100. Everything at or below 50 means the
whole group survives; the tail past 50 is where every failure lives.

Run:  python3 make_figure.py   ->   longest_cycle.png
"""

import random
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N, K, TRIALS = 100, 50, 300_000

hist = Counter()
for _ in range(TRIALS):
    boxes = list(range(N))
    random.shuffle(boxes)
    seen = [False] * N
    longest = 0
    for start in range(N):
        if seen[start]:
            continue
        length, node = 0, start
        while not seen[node]:
            seen[node] = True
            node = boxes[node]
            length += 1
        longest = max(longest, length)
    hist[longest] += 1

xs = list(range(1, N + 1))
ys = [hist.get(x, 0) / TRIALS for x in xs]

# palette matched to the web app
NAVY, TEAL, RED, DIM = "#0d1120", "#5ec8c0", "#e86a6a", "#7f8aa3"

fig, ax = plt.subplots(figsize=(9, 4.6), dpi=130)
fig.patch.set_facecolor(NAVY)
ax.set_facecolor(NAVY)

colors = [TEAL if x <= K else RED for x in xs]
ax.bar(xs, ys, color=colors, width=0.9)

surv = sum(ys[:K])       # longest <= 50
die = sum(ys[K:])        # longest  > 50
ax.axvline(K + 0.5, color=DIM, lw=1, ls="--")

ax.text(26, max(ys) * 0.92, f"longest cycle ≤ 50\nALL SURVIVE\n≈ {surv:.0%}",
        color=TEAL, ha="center", va="top", fontsize=11, family="monospace")
ax.text(76, max(ys) * 0.92, f"longest cycle > 50\ngroup dies\n≈ {die:.0%}",
        color=RED, ha="center", va="top", fontsize=11, family="monospace")

ax.set_title("Longest cycle in a random shuffle of 100 boxes",
             color="#e9edf2", fontsize=13, family="monospace", pad=12)
ax.set_xlabel("length of the longest cycle", color=DIM, family="monospace")
ax.set_ylabel("probability", color=DIM, family="monospace")
ax.tick_params(colors=DIM)
for s in ax.spines.values():
    s.set_color("#232a3d")
ax.set_xlim(0, N + 1)

fig.tight_layout()
fig.savefig("longest_cycle.png", facecolor=NAVY, bbox_inches="tight")
print(f"saved longest_cycle.png  (survive={surv:.4f}, die={die:.4f})")
