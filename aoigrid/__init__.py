"""
aoigrid — a tiny spatial hash grid for Area-of-Interest (AoI) queries.

For games, simulations, and any system where each entity only needs to know
about its nearby neighbors. Insert entities at (x, y) or (x, y, z), then ask
"who is near me?" in roughly O(local) time instead of O(n^2).

Open-sourced by WCN Development Co, LLC. MIT licensed.
https://github.com/gphoenix172-droid/aoi-grid
"""
from .grid import SpatialGrid

__version__ = "0.1.0"
__all__ = ["SpatialGrid"]
