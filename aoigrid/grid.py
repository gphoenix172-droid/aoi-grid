"""
aoigrid.grid — uniform spatial hash grid for neighbor / AoI queries.

Classic, well-understood technique: bucket entities into fixed-size cells,
then answer "neighbors within radius" by only scanning the cells that
overlap the query area. Pure standard library, 2D or 3D.

This is a general-purpose spatial primitive — useful for crowd rendering,
collision broad-phase, flocking, proximity chat, interest management, etc.
"""
from __future__ import annotations

import math
from typing import Dict, Hashable, List, Optional, Tuple


class SpatialGrid:
    """
    A uniform spatial hash grid.

    cell_size: width of each grid cell (tune ~= your typical query radius).
    dims:      2 or 3.
    """

    def __init__(self, cell_size: float, dims: int = 2) -> None:
        if dims not in (2, 3):
            raise ValueError("dims must be 2 or 3")
        if cell_size <= 0:
            raise ValueError("cell_size must be > 0")
        self.cell_size = float(cell_size)
        self.dims = dims
        self._cells: Dict[Tuple[int, ...], Dict[Hashable, Tuple[float, ...]]] = {}
        self._pos: Dict[Hashable, Tuple[float, ...]] = {}

    def _key(self, pos: Tuple[float, ...]) -> Tuple[int, ...]:
        cs = self.cell_size
        return tuple(int(math.floor(c / cs)) for c in pos[: self.dims])

    def insert(self, entity_id: Hashable, pos: Tuple[float, ...]) -> None:
        """Insert or move an entity to a position."""
        if entity_id in self._pos:
            self.remove(entity_id)
        pos = tuple(float(c) for c in pos[: self.dims])
        key = self._key(pos)
        self._cells.setdefault(key, {})[entity_id] = pos
        self._pos[entity_id] = pos

    # convenience alias — inserting an existing id moves it
    move = insert

    def remove(self, entity_id: Hashable) -> None:
        """Remove an entity from the grid."""
        pos = self._pos.pop(entity_id, None)
        if pos is None:
            return
        key = self._key(pos)
        bucket = self._cells.get(key)
        if bucket:
            bucket.pop(entity_id, None)
            if not bucket:
                del self._cells[key]

    def _cell_range(self, pos, radius):
        cs = self.cell_size
        spans = []
        for i in range(self.dims):
            lo = int(math.floor((pos[i] - radius) / cs))
            hi = int(math.floor((pos[i] + radius) / cs))
            spans.append(range(lo, hi + 1))
        return spans

    def query_radius(self, pos: Tuple[float, ...], radius: float,
                     exclude: Optional[Hashable] = None) -> List[Hashable]:
        """Return entity ids within `radius` of `pos` (any-dim Euclidean)."""
        pos = tuple(float(c) for c in pos[: self.dims])
        r2 = radius * radius
        spans = self._cell_range(pos, radius)
        found: List[Hashable] = []

        if self.dims == 2:
            for cx in spans[0]:
                for cy in spans[1]:
                    bucket = self._cells.get((cx, cy))
                    if not bucket:
                        continue
                    for eid, ep in bucket.items():
                        if eid == exclude:
                            continue
                        dx = ep[0] - pos[0]; dy = ep[1] - pos[1]
                        if dx * dx + dy * dy <= r2:
                            found.append(eid)
        else:
            for cx in spans[0]:
                for cy in spans[1]:
                    for cz in spans[2]:
                        bucket = self._cells.get((cx, cy, cz))
                        if not bucket:
                            continue
                        for eid, ep in bucket.items():
                            if eid == exclude:
                                continue
                            dx = ep[0] - pos[0]; dy = ep[1] - pos[1]; dz = ep[2] - pos[2]
                            if dx * dx + dy * dy + dz * dz <= r2:
                                found.append(eid)
        return found

    def nearest(self, pos: Tuple[float, ...], k: int,
                exclude: Optional[Hashable] = None,
                max_radius: Optional[float] = None) -> List[Hashable]:
        """
        Return the k nearest entity ids to `pos`, closest first.

        Expands the search radius outward in cell-sized rings until at least
        k candidates are found (or max_radius is hit), then sorts by distance.
        Ideal for "show me the N closest players/objects" interest management.
        """
        pos = tuple(float(c) for c in pos[: self.dims])
        radius = self.cell_size
        cap = max_radius if max_radius is not None else self.cell_size * 64
        candidates: List[Hashable] = []
        while True:
            candidates = self.query_radius(pos, radius, exclude=exclude)
            if len(candidates) >= k or radius >= cap:
                break
            radius *= 2

        def d2(eid):
            ep = self._pos[eid]
            return sum((ep[i] - pos[i]) ** 2 for i in range(self.dims))

        candidates.sort(key=d2)
        return candidates[:k]

    def __len__(self) -> int:
        return len(self._pos)
