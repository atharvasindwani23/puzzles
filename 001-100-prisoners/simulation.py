"""
The 100 Prisoners Problem — simulation.

We compare two strategies and watch the ~31% survival rate appear out of
thin air. The point isn't just to get the number; it's to *see* that the
failures all pile onto a single event: "was there a cycle longer than 50?"

Run:  python3 simulation.py
"""

import random
from collections import Counter


def trial_random(n, k):
    """Everyone opens k random boxes. Independent coin flips.

    Returns True if ALL prisoners find their own number.
    """
    boxes = list(range(n))
    random.shuffle(boxes)  # boxes[i] = the number inside box i
    for prisoner in range(n):
        # Open k distinct random boxes and hope our number is there.
        opened = random.sample(range(n), k)
        if prisoner not in (boxes[b] for b in opened):
            return False
    return True


def trial_cycle(n, k):
    """Everyone follows the cycle strategy: start at your own box, then let
    the number you find point you to the next box.

    Returns (all_survived, longest_cycle_length) so we can inspect WHY a
    trial failed, not just whether it did.
    """
    boxes = list(range(n))
    random.shuffle(boxes)

    # The whole group's fate depends only on the longest cycle in `boxes`.
    # Find every cycle length by walking the permutation once.
    seen = [False] * n
    longest = 0
    for start in range(n):
        if seen[start]:
            continue
        length = 0
        node = start
        while not seen[node]:
            seen[node] = True
            node = boxes[node]  # the number we found tells us the next box
            length += 1
        longest = max(longest, length)

    return longest <= k, longest


def run(n=100, k=50, trials=100_000):
    print(f"n={n} prisoners, each may open k={k} boxes, {trials:,} trials\n")

    # --- Naive random strategy ---
    random_wins = sum(trial_random(n, k) for _ in range(trials))
    print(f"Random strategy   : {random_wins:>7,} / {trials:,} survived "
          f"({random_wins / trials:.6%})")
    print(f"  theory ~ (1/2)^{n} ≈ {0.5 ** n:.2e}\n")

    # --- Cycle-following strategy ---
    cycle_wins = 0
    longest_hist = Counter()
    for _ in range(trials):
        survived, longest = trial_cycle(n, k)
        cycle_wins += survived
        longest_hist[longest] += 1
    print(f"Cycle strategy    : {cycle_wins:>7,} / {trials:,} survived "
          f"({cycle_wins / trials:.6%})")

    # Exact theory: 1 - (H_n - H_k) = 1 - sum(1/L for L in k+1..n)
    tail = sum(1.0 / L for L in range(k + 1, n + 1))
    print(f"  exact theory 1 - (1/{k+1} + ... + 1/{n}) = {1 - tail:.6%}\n")

    # --- WHY did the cycle trials fail? Show the longest-cycle distribution ---
    print("Longest-cycle length — where the failures live (cycle strategy):")
    survive_mass = sum(c for L, c in longest_hist.items() if L <= k)
    fail_mass = sum(c for L, c in longest_hist.items() if L > k)
    print(f"  longest cycle <= {k}  (ALL survive) : {survive_mass:>7,} "
          f"({survive_mass / trials:.2%})")
    print(f"  longest cycle >  {k}  (group dies)  : {fail_mass:>7,} "
          f"({fail_mass / trials:.2%})")
    print("\n  Every single failure is one event: a cycle too long to finish.")


if __name__ == "__main__":
    run()
