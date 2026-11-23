
import pytest

from fdf.parser import MapFormatError, parse_map


def test_parse_simple_map():
    result = parse_map("0 1\n2 3")
    assert result.width == 2
    assert result.height == 2


def test_parse_point_coordinates():
    result = parse_map("5 8\n3 4")
    assert result.points[1][0].x == 0
    assert result.points[1][0].y == 1
    assert result.points[1][0].z == 3


def test_parse_negative_heights():
    result = parse_map("-1 0 2")
    assert result.points[0][0].z == -1


def test_parse_color():
    result = parse_map("0,0xFF0000")
    assert result.points[0][0].color == "#FF0000"


def test_parse_short_color():
    result = parse_map("0,0xF")
    assert result.points[0][0].color == "#00000F"


def test_invalid_height():
    with pytest.raises(MapFormatError):
        parse_map("abc")


def test_invalid_color():
    with pytest.raises(MapFormatError):
        parse_map("0,red")


def test_inconsistent_row_width():
    with pytest.raises(MapFormatError):
        parse_map("0 1\n2")


def test_empty_map():
    with pytest.raises(MapFormatError):
        parse_map("")
