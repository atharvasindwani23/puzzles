# 🧩 Puzzles

Interesting math + coding puzzles, worked through the old-fashioned way: state the problem, share the real thought process behind the solution, verify it in code, and — where it helps — build something interactive so you can *feel* the idea instead of just reading it.

Each puzzle lives in its own numbered folder with a self-contained write-up. Start at any folder's `README.md`: you'll find the question first, then the reasoning that cracks it.

## Index

| # | Puzzle | The hook | Difficulty |
|---|--------|----------|:---:|
| [001](./001-100-prisoners/) | **The 100 Prisoners Problem** | The odds look like `(1/2)^100`. They're actually ~31%. | ⭐ |

## Structure

```
puzzles/
├── README.md                    ← you are here (the index)
└── NNN-puzzle-name/
    ├── README.md                ← the problem + full thought process
    ├── simulation.py            ← runnable verification
    └── app/                     ← (optional) interactive demo
```
