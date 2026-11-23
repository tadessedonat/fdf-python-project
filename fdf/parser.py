
from typing import List
from fdf.model import MapData, Point


class FdfError(Exception):
    pass


class MapFormatError(FdfError):
    pass


def parse_map(text: str) -> MapData:
    lines = text.splitlines()
    points: List[List[Point]] = []

    for y, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        row: List[Point] = []
        values = line.split()

        for x, value in enumerate(values, start=1):
            parts = value.split(",")

            if len(parts) > 2:
                raise MapFormatError(
                    f"Invalid point at line {y}, column {x}: {value}"
                )

            try:
                z = int(parts[0])
            except ValueError:
                raise MapFormatError(
                    f"Invalid height at line {y}, column {x}: {value}"
                )

            color = None

            if len(parts) == 2:
                color_text = parts[1]

                if not color_text.lower().startswith("0x"):
                    raise MapFormatError(
                        f"Invalid color at line {y}, column {x}: {color_text}"
                    )

                try:
                    color_number = int(color_text[2:], 16)
                except ValueError:
                    raise MapFormatError(
                        f"Invalid color at line {y}, column {x}: {color_text}"
                    )

                if color_number < 0 or color_number > 0xFFFFFF:
                    raise MapFormatError(
                        f"Color out of range at line {y}, column {x}"
                    )

                color = "#{:06X}".format(color_number)

            point = Point(
                x=x - 1,
                y=len(points),
                z=z,
                color=color
            )
            row.append(point)

        points.append(row)

    if not points:
        raise MapFormatError("Map is empty")

    width = len(points[0])

    for row_number, row in enumerate(points, start=1):
        if len(row) != width:
            raise MapFormatError(
                f"Row {row_number} has an incorrect number of points"
            )

    height = len(points)

    return MapData(
        points=points,
        width=width,
        height=height
    )
