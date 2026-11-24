
from fdf.model import MapData, Point


class FdfError(Exception):
    pass


class MapFormatError(FdfError):
    pass


def parse_map(text: str) -> MapData:
    lines = text.splitlines()

    while lines and not lines[-1].strip():
        lines.pop()

    points: list[list[Point]] = []
    source_lines: list[int] = []

    for y, line in enumerate(lines, start=1):
        if not line.strip():
            raise MapFormatError(f"Empty row at line {y}")

        row: list[Point] = []
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
                ) from None

            color = None

            if len(parts) == 2:
                color_text = parts[1]

                if not color_text.lower().startswith("0x"):
                    raise MapFormatError(
                        f"Invalid color at line {y}, column {x}: {color_text}"
                    )

                try:
                    color_number = int(color_text, 0)
                except ValueError:
                    raise MapFormatError(
                        f"Invalid color at line {y}, column {x}: {color_text}"
                    ) from None

                if color_number > 0xFFFFFF:
                    raise MapFormatError(
                        f"Color out of range at line {y}, column {x}"
                    )

                color = f"#{color_number:06X}"

            point = Point(
                x=x - 1,
                y=len(points),
                z=z,
                color=color
            )
            row.append(point)

        points.append(row)
        source_lines.append(y)

    if not points:
        raise MapFormatError("Map is empty")

    width = len(points[0])

    for row_number, row in enumerate(points):
        if len(row) != width:
            line_number = source_lines[row_number]
            column_number = min(len(row), width) + 1

            raise MapFormatError(
                f"Incorrect row width at line {line_number}, "
                f"column {column_number}"
            )

    return MapData(
        points=points,
        width=width,
        height=len(points)
    )
