
import math

import pytest

from fdf.parser import parse_map
from fdf.projection import Camera, project_point


def test_project_point():
    x, y = project_point(1, 0, 0, 10, 1)

    assert x == pytest.approx(10 * math.cos(math.radians(30)))
    assert y == pytest.approx(5)


def test_project_point_with_height():
    _, y_without_height = project_point(1, 0, 0, 10, 1)
    _, y_with_height = project_point(1, 0, 2, 10, 1)

    assert y_with_height < y_without_height


def test_camera_transform():
    camera = Camera(10, 1, 100, 100)

    x, y = camera.transform(1, 0, 0)

    assert x == pytest.approx(108.660254)
    assert y == pytest.approx(105)


def test_camera_fit():
    map_data = parse_map("0 0\n0 0")
    camera = Camera.fit(map_data, 800, 600)

    assert camera.scale > 0

    projected = [
        camera.transform(point.x, point.y, point.z)
        for row in map_data.points
        for point in row
    ]

    center_x = (min(p[0] for p in projected) + max(p[0] for p in projected)) / 2
    center_y = (min(p[1] for p in projected) + max(p[1] for p in projected)) / 2

    assert center_x == pytest.approx(400)
    assert center_y == pytest.approx(300)
