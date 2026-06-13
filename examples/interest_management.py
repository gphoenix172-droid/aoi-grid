"""
Example: 5,000 entities in a world; each frame, find the ~50 nearest to a
player so you only sync/render those. This is the core of interest management.
"""
import random
from aoigrid import SpatialGrid

grid = SpatialGrid(cell_size=50, dims=2)
for i in range(5000):
    grid.insert(i, (random.uniform(0, 5000), random.uniform(0, 5000)))

player_pos = (2500, 2500)
visible = grid.nearest(player_pos, k=50)
print(f"world has {len(grid)} entities")
print(f"player only needs to know about {len(visible)} of them")
print("nearest ids:", visible[:10], "...")
