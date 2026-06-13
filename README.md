# aoigrid

**A tiny spatial hash grid for Area-of-Interest (AoI) and nearest-neighbor queries. 2D & 3D. Zero dependencies.**

When you have thousands of entities but each one only cares about its *neighbors*, you don't want O(n²) checks. `aoigrid` buckets entities into cells so "who's near me?" and "give me the 50 closest" run in roughly O(local) time.

```python
from aoigrid import SpatialGrid

grid = SpatialGrid(cell_size=50, dims=2)
for i, (x, y) in enumerate(positions):
    grid.insert(i, (x, y))

# who is within 100 units of me?
neighbors = grid.query_radius((px, py), radius=100, exclude=me)

# the 50 closest entities (interest management)
visible = grid.nearest((px, py), k=50)
```

## Why

This is the workhorse behind **interest management**, **crowd rendering**, **collision broad-phase**, **flocking/boids**, and **proximity systems**. A world can hold 5,000+ entities while any single observer only ever processes the ~50 nearest — the difference between a system that scales and one that melts.

- 📦 **Spatial hash grid** — insert / move / remove in ~O(1)
- 🎯 **`query_radius`** — everything within a distance
- 🔍 **`nearest(k)`** — the k closest, closest-first, ring-expanding search
- 🧊 **2D and 3D**
- 🪶 **Pure standard library**, Python 3.8+

## Install

```bash
pip install aoigrid
```

Or copy `aoigrid/grid.py` into your project — no imports beyond the stdlib.

## API

| Method | Purpose |
|---|---|
| `SpatialGrid(cell_size, dims=2)` | New grid. Tune `cell_size` ≈ your typical query radius. |
| `.insert(id, pos)` / `.move(id, pos)` | Place or move an entity. |
| `.remove(id)` | Remove an entity. |
| `.query_radius(pos, radius, exclude=None)` | Ids within radius. |
| `.nearest(pos, k, exclude=None, max_radius=None)` | k closest ids, sorted. |

## Tests

```bash
python tests/test_grid.py    # or: pytest
```

## Contributing

PRs welcome — keep it dependency-free. Ideas: non-uniform grids, k-d tree backend option, batch updates. Open an issue and let's scope it.

## License

MIT © WCN Development Co, LLC

---

*Built and open-sourced by [WCN Development Co, LLC](https://github.com/gphoenix172-droid) — we build large-scale systems and ship the reusable primitives back to the community.*
