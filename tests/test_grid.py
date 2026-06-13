from aoigrid import SpatialGrid


def test_query_radius_basic():
    g = SpatialGrid(cell_size=10, dims=2)
    g.insert("a", (0, 0))
    g.insert("b", (5, 0))
    g.insert("c", (100, 100))
    near = set(g.query_radius((0, 0), 10))
    assert "a" in near and "b" in near and "c" not in near


def test_exclude_self():
    g = SpatialGrid(cell_size=10)
    g.insert("me", (0, 0))
    g.insert("you", (1, 0))
    res = g.query_radius((0, 0), 5, exclude="me")
    assert res == ["you"]


def test_nearest_k_sorted():
    g = SpatialGrid(cell_size=5)
    g.insert("close", (1, 0))
    g.insert("mid", (4, 0))
    g.insert("far", (20, 0))
    result = g.nearest((0, 0), 2, exclude=None)
    assert result[0] == "close"
    assert "far" not in result


def test_move_updates_cell():
    g = SpatialGrid(cell_size=10)
    g.insert("x", (0, 0))
    assert "x" in g.query_radius((0, 0), 5)
    g.move("x", (1000, 1000))
    assert "x" not in g.query_radius((0, 0), 5)
    assert "x" in g.query_radius((1000, 1000), 5)


def test_3d():
    g = SpatialGrid(cell_size=10, dims=3)
    g.insert("a", (0, 0, 0))
    g.insert("b", (0, 0, 100))
    near = g.query_radius((0, 0, 0), 10)
    assert "a" in near and "b" not in near


def test_remove():
    g = SpatialGrid(cell_size=10)
    g.insert("a", (0, 0))
    g.remove("a")
    assert len(g) == 0
    assert g.query_radius((0, 0), 5) == []


if __name__ == "__main__":
    for fn in [v for k, v in list(globals().items()) if k.startswith("test_")]:
        fn()
    print("all tests passed")
